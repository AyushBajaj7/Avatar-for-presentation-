# Easy AI Speaker Avatar System

A complete system for creating AI-powered speaker avatars from PowerPoint presentations.

## Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# Windows
start.bat

# Or manually
python download.py  # Install dependencies once
python run.py       # Run the system
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install python-pptx Pillow opencv-python pyttsx3 tqdm numpy flask flask-cors google-generativeai PyPDF2 pdf2image

# Run the system
python run.py
```

## Files

- `download.py` - Installs all required dependencies (run once)
- `run.py` - Main application (runs after dependencies are installed)
- `start.bat` - Windows batch file for easy startup
- `frontend/` - Web interface files

## Features

- ✅ **Progress Tracking**: Detailed terminal output with emojis and slide-by-slide status
- ✅ **TTS Timeout Protection**: 30-second timeout prevents hanging
- ✅ **FFmpeg Compatibility**: Handles odd image dimensions automatically
- ✅ **Retry Logic**: Automatic retries for failed operations
- ✅ **Fallback Video Creation**: Creates static videos when Wav2Lip is unavailable
- ✅ **Resumable Processing**: Skips already completed slides

## Usage

1. **First Time Setup**:
   ```bash
   python download.py
   ```

2. **Run the System**:
   ```bash
   python run.py
   ```

3. **Access Web Interface**: Open http://localhost:5000

4. **Upload Files**: Upload your PowerPoint presentation and face image

5. **Monitor Progress**: Watch the terminal for detailed progress updates

## Terminal Output

The system now provides detailed progress tracking:

```
🎭 PROCESSING SLIDE 4/4 - Animating face...
🔄 STATUS UPDATE: 68% - Animating face for slide 4/4
✅ FACE ANIMATED FOR SLIDE 4/4 - Moving to next slide
```

## Troubleshooting

- **Missing Dependencies**: Run `python download.py`
- **FFmpeg Errors**: The system automatically handles image dimension issues
- **TTS Hanging**: 30-second timeout prevents infinite hanging
- **Video Generation**: Falls back to static videos if Wav2Lip is unavailable

## System Requirements

- Python 3.7+
- FFmpeg (for video processing)
- Windows/Linux/macOS