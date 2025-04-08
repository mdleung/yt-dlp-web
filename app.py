from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS
import subprocess
import threading
import time
import re
import os
import json
import shlex
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# Store active downloads and their progress
downloads = {}
download_logs = {}

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sanitize_filename(filename):
    """Sanitize filename to prevent command injection"""
    return re.sub(r'[^\w\-\.]', '_', filename)

def parse_progress(line):
    """Parse progress information from yt-dlp output"""
    progress_data = {
        'status': 'processing',
        'percent': 0,
        'speed': '',
        'eta': '',
        'size': '',
        'message': line
    }
    
    # Download progress pattern
    if '[download]' in line:
        # Extract percentage
        percent_match = re.search(r'(\d+\.\d+)%', line)
        if percent_match:
            progress_data['percent'] = float(percent_match.group(1))
        
        # Extract speed
        speed_match = re.search(r'at\s+([^\s]+)', line)
        if speed_match:
            progress_data['speed'] = speed_match.group(1)
        
        # Extract ETA
        eta_match = re.search(r'ETA\s+([^\s]+)', line)
        if eta_match:
            progress_data['eta'] = eta_match.group(1)
        
        # Extract size
        size_match = re.search(r'of\s+~?\s*([^\s]+)', line)
        if size_match:
            progress_data['size'] = size_match.group(1)
    
    # Check for completion
    elif 'has already been downloaded' in line or 'Destination:' in line:
        progress_data['status'] = 'completed'
        progress_data['percent'] = 100
    
    return progress_data

def run_yt_dlp(download_id, url, options):
    """Run yt-dlp with the given options and update progress"""
    downloads[download_id] = {
        'status': 'starting',
        'percent': 0,
        'speed': '',
        'eta': '',
        'size': '',
        'message': 'Starting download...'
    }
    download_logs[download_id] = []
    
    # Create download directory if it doesn't exist
    download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    os.makedirs(download_dir, exist_ok=True)
    
    # Build command based on options
    cmd = ['yt-dlp']
    
    # Add format option based on download type
    if options.get('download_type') == 'audio':
        cmd.extend(['-x', '--audio-format', 'mp3'])
    else:  # video
        cmd.extend(['-f', 'bestvideo+bestaudio', '--merge-output-format', 'mp4'])
    
    # Add playlist option if needed
    if not options.get('playlist', False):
        cmd.append('--no-playlist')
    
    # Add progress output formatting
    cmd.extend(['--newline', '--progress'])
    
    # Add output template
    timestamp = get_timestamp()
    output_template = f'downloads/{timestamp}_%(title)s.%(ext)s'
    cmd.extend(['-o', output_template])
    
    # Add URL
    cmd.append(url)
    
    # Start the process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Read output line by line and update progress
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        if line:
            download_logs[download_id].append(line)
            progress_data = parse_progress(line)
            downloads[download_id].update(progress_data)
    
    # Process completed
    process.stdout.close()
    return_code = process.wait()
    
    if return_code == 0:
        downloads[download_id]['status'] = 'completed'
        downloads[download_id]['percent'] = 100
        downloads[download_id]['message'] = 'Download completed successfully!'
    else:
        downloads[download_id]['status'] = 'error'
        downloads[download_id]['message'] = f'Download failed with return code {return_code}'
    
    # Keep download info for 1 hour
    def cleanup():
        time.sleep(3600)  # 1 hour
        if download_id in downloads:
            del downloads[download_id]
        if download_id in download_logs:
            del download_logs[download_id]
    
    cleanup_thread = threading.Thread(target=cleanup)
    cleanup_thread.daemon = True
    cleanup_thread.start()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/download', methods=['POST'])
def start_download():
    data = request.json
    url = data.get('url')
    options = {
        'download_type': data.get('download_type', 'video'),
        'playlist': data.get('playlist', False)
    }
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Generate a unique download ID
    download_id = f"{int(time.time())}"
    
    # Start download in a separate thread
    thread = threading.Thread(
        target=run_yt_dlp,
        args=(download_id, url, options)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'download_id': download_id})

@app.route('/api/progress/<download_id>')
def progress_stream(download_id):
    def generate():
        last_status = None
        
        while True:
            if download_id not in downloads:
                yield f"data: {json.dumps({'status': 'not_found'})}\n\n"
                break
            
            current_status = downloads[download_id].copy()
            
            # Only send updates when there's a change
            if current_status != last_status:
                yield f"data: {json.dumps(current_status)}\n\n"
                last_status = current_status.copy()
            
            # If download is completed or errored, send one final update and stop
            if current_status['status'] in ['completed', 'error']:
                yield f"data: {json.dumps(current_status)}\n\n"
                break
            
            time.sleep(0.5)
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/logs/<download_id>')
def get_logs(download_id):
    if download_id not in download_logs:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify({'logs': download_logs[download_id]})

@app.route('/api/downloads')
def list_downloads():
    download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
    if not os.path.exists(download_dir):
        return jsonify({'files': []})
    
    files = []
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        if os.path.isfile(file_path):
            files.append({
                'name': filename,
                'size': os.path.getsize(file_path),
                'modified': os.path.getmtime(file_path)
            })
    
    return jsonify({'files': files})

if __name__ == '__main__':
    # Create static folder if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), exist_ok=True)
    
    # Create downloads folder if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads'), exist_ok=True)
    
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
