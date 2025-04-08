# YT-DLP Web Interface

A lightweight self-hosted web application front-end for [yt-dlp](https://github.com/yt-dlp/yt-dlp), providing an intuitive interface for downloading videos and audio from various platforms.

## Features

- Clean, intuitive web interface for yt-dlp
- Download options:
  - Best-quality video
  - Audio only (MP3 format)
  - Playlist support
- Real-time download progress display
- Fully local operation (no cloud dependencies)
- Cross-platform compatibility (Linux/macOS/Windows)
- Responsive design for all device sizes

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Alpine.js + HTML/CSS
- **Real-time Updates**: Server-Sent Events (SSE)

## Requirements

- Python 3.6+
- yt-dlp
- Flask and Flask-CORS

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/yt-dlp-web.git
   cd yt-dlp-web
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Access the web interface at:
   ```
   http://localhost:5001
   ```

## Usage

1. Enter a video or playlist URL in the input field
2. Select your preferred download options:
   - Video (best quality) or Audio only
   - Download entire playlist (if applicable)
3. Click "Download" to start the process
4. Monitor the download progress in real-time
5. Find downloaded files in the `downloads` directory

## Project Structure

```
yt-dlp-web/
├── app.py                 # Flask backend application
├── static/                # Frontend static files
│   ├── index.html         # Main HTML interface
│   └── app.js             # Alpine.js application code
├── downloads/             # Downloaded files directory
├── requirements.txt       # Project dependencies
└── documentation.md       # Detailed technical documentation
```

## Why This Tech Stack?

This application uses a lightweight tech stack optimized for:

1. **Minimal Resource Usage**: Flask and Alpine.js have small footprints
2. **No Cloud Dependencies**: Fully local operation
3. **Cross-Platform Compatibility**: Works on all major operating systems
4. **Simple Deployment**: No complex build process
5. **Real-Time Updates**: SSE for efficient progress reporting

For more details, see the [technical documentation](documentation.md).

## License

MIT

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful command-line downloader
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework
