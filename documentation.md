# YT-DLP Web Interface - Technical Documentation

## Project Overview
This project is a lightweight self-hosted web application front-end for yt-dlp, providing an intuitive interface for users to download videos and audio from various platforms. The application runs entirely locally without cloud dependencies and is designed to be cross-platform compatible.

## Tech Stack

### Backend
- **Flask**: A lightweight Python web framework
  - Handles HTTP requests and serves the web interface
  - Manages yt-dlp subprocess execution
  - Provides real-time progress updates via Server-Sent Events (SSE)

### Frontend
- **Alpine.js**: A minimal JavaScript framework (< 15KB)
  - Provides reactive UI components
  - Handles form submission and validation
  - Manages application state
- **HTML/CSS**: Clean, responsive interface
  - Mobile-friendly design
  - Minimal dependencies

### Communication
- **Server-Sent Events (SSE)**: For real-time progress updates
  - Lightweight one-way communication from server to client
  - Native browser support without additional libraries

## Features
- Input field for video or playlist URL
- Download options:
  - Best-quality video
  - Audio only
  - Playlist support (with video or audio toggle)
- Real-time download progress display
- Detailed log output
- Responsive design for all device sizes

## Implementation Details

### Backend Implementation
The Flask backend handles:
1. Serving the static frontend files
2. Processing download requests
3. Running yt-dlp as a subprocess
4. Parsing progress information
5. Streaming real-time updates to the client

Key components:
- `/api/download` endpoint for initiating downloads
- `/api/progress/<download_id>` endpoint for SSE progress streaming
- `/api/logs/<download_id>` endpoint for retrieving complete logs
- `/api/downloads` endpoint for listing downloaded files

### Frontend Implementation
The Alpine.js frontend provides:
1. Form for URL input and download options
2. Real-time progress bar and status updates
3. Log display with automatic scrolling
4. Error handling and user feedback

### Cross-Platform Compatibility
The application is designed to work across:
- Linux
- macOS
- Windows

Requirements:
- Python 3.6+
- yt-dlp installed
- Modern web browser

## Justification for Tech Stack

### Why Flask?
- **Lightweight**: Minimal overhead and resource usage
- **Python-based**: Same language as yt-dlp for seamless integration
- **Simple**: Easy to set up and maintain
- **Cross-platform**: Works on all major operating systems
- **Built-in development server**: Quick to start and test

### Why Alpine.js?
- **Minimal size**: Only ~15KB minified and gzipped
- **No build step**: Works directly in HTML without compilation
- **Declarative syntax**: Simple to understand and maintain
- **Browser-native**: No complex dependencies
- **Progressive enhancement**: Works well with existing HTML/CSS

### Why Server-Sent Events?
- **Lightweight**: Minimal overhead compared to WebSockets
- **One-way communication**: Perfect for progress updates
- **Native browser support**: No additional libraries required
- **Automatic reconnection**: Built-in reliability

## Installation and Usage

### Prerequisites
- Python 3.6+
- yt-dlp installed (`pip install yt-dlp`)
- Flask and Flask-CORS (`pip install flask flask-cors`)

### Setup
1. Clone the repository or download the files
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Access the web interface at: `http://localhost:5001`

### Usage
1. Enter a video or playlist URL
2. Select download options (video/audio, playlist)
3. Click "Download" to start the process
4. Monitor progress in real-time
5. Access downloaded files in the `downloads` directory

## Project Structure
```
yt-dlp-web/
├── app.py                 # Flask backend application
├── static/                # Frontend static files
│   ├── index.html         # Main HTML interface
│   └── app.js             # Alpine.js application code
└── downloads/             # Downloaded files directory
```

## Conclusion
This application provides a clean, intuitive web interface for yt-dlp while maintaining the lightweight and cross-platform requirements. The chosen tech stack (Flask + Alpine.js + SSE) offers the best balance of simplicity, performance, and features for a self-hosted application without cloud dependencies.
