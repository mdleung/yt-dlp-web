// Alpine.js application for YT-DLP Web Interface
document.addEventListener('alpine:init', () => {
  Alpine.data('ytdlpApp', () => ({
    url: '',
    downloadType: 'video',
    playlist: false,
    downloadId: null,
    isDownloading: false,
    progress: {
      status: 'idle',
      percent: 0,
      speed: '',
      eta: '',
      size: '',
      message: ''
    },
    logs: [],
    error: null,
    
    // Initialize the application
    init() {
      // Nothing to initialize on load
    },
    
    // Start a download
    startDownload() {
      if (!this.url) {
        this.error = 'Please enter a valid URL';
        return;
      }
      
      this.error = null;
      this.isDownloading = true;
      this.progress = {
        status: 'starting',
        percent: 0,
        speed: '',
        eta: '',
        size: '',
        message: 'Starting download...'
      };
      this.logs = [];
      
      // Show progress container
      document.getElementById('progress-container').style.display = 'block';
      
      // Send download request to backend
      fetch('/api/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: this.url,
          download_type: this.downloadType,
          playlist: this.playlist
        })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        this.downloadId = data.download_id;
        this.startProgressStream();
      })
      .catch(error => {
        this.error = `Error starting download: ${error.message}`;
        this.isDownloading = false;
      });
    },
    
    // Start the progress event stream
    startProgressStream() {
      if (!this.downloadId) return;
      
      const eventSource = new EventSource(`/api/progress/${this.downloadId}`);
      
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.status === 'not_found') {
          this.error = 'Download not found';
          this.isDownloading = false;
          eventSource.close();
          return;
        }
        
        this.progress = data;
        
        // Update progress bar
        document.getElementById('progress').style.width = `${data.percent}%`;
        
        // Add message to logs if it's not already there
        if (data.message && !this.logs.includes(data.message)) {
          this.logs.push(data.message);
          this.scrollLogsToBottom();
        }
        
        // Check if download is completed or errored
        if (data.status === 'completed' || data.status === 'error') {
          this.isDownloading = false;
          eventSource.close();
          
          // Fetch complete logs
          this.fetchLogs();
        }
      };
      
      eventSource.onerror = () => {
        this.error = 'Error in progress stream';
        this.isDownloading = false;
        eventSource.close();
      };
    },
    
    // Fetch complete logs for a download
    fetchLogs() {
      if (!this.downloadId) return;
      
      fetch(`/api/logs/${this.downloadId}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          this.logs = data.logs;
          this.scrollLogsToBottom();
        })
        .catch(error => {
          console.error('Error fetching logs:', error);
        });
    },
    
    // Scroll logs container to bottom
    scrollLogsToBottom() {
      setTimeout(() => {
        const logElement = document.getElementById('log');
        if (logElement) {
          logElement.scrollTop = logElement.scrollHeight;
        }
      }, 50);
    },
    
    // Reset the form
    resetForm() {
      this.url = '';
      this.downloadType = 'video';
      this.playlist = false;
      this.downloadId = null;
      this.isDownloading = false;
      this.progress = {
        status: 'idle',
        percent: 0,
        speed: '',
        eta: '',
        size: '',
        message: ''
      };
      this.logs = [];
      this.error = null;
      
      // Hide progress container
      document.getElementById('progress-container').style.display = 'none';
    }
  }));
});
