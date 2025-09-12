# AI Speaker Avatar System - Clean Version

A streamlined AI-powered system that creates animated speaker avatars for PowerPoint presentations with proper lip-sync.

## 🎯 What It Does

- **Extracts text** from PowerPoint (.pptx) files
- **Generates natural speech** using AI text-to-speech
- **Creates animated avatars** with lip-sync using Wav2Lip
- **Composes final videos** with PowerPoint slides as backgrounds
- **Properly positions avatars** for clear lip-sync visibility

## 🚀 Quick Start

### For New Presentations:
1. **Clean the system**: `python setup_new_presentation.py` or `clean_system.bat`
2. **Add your files**:
   - PowerPoint file (.pptx) → `ppt_input/`
   - Face image (.png/.jpg) → `face_images/`
3. **Run the system**: `python backend_final_fixed.py`

### Or use the batch file:
```bash
run_backend.bat
```

## 📁 Project Structure

```
├── backend_only_fixed.py     # Main system runner (ONE COMMAND)
├── working_main.py           # Core AI processing engine
├── final_video_composer.py   # Video composition with slide backgrounds
├── slide_renderer.py         # PowerPoint slide rendering
├── tts_fallback.py          # Text-to-speech system
├── config.json              # Configuration settings
├── requirements.txt         # Python dependencies
├── ppt_input/               # Put your .pptx files here
├── face_images/             # Put face images here (.png/.jpg)
├── output/                  # Final videos appear here
├── audio/                   # Generated audio files
├── video/                   # Animated avatar videos
├── slide_images/            # Rendered slide images
└── Wav2Lip/                 # AI lip-sync model
```

## 📋 Requirements

- Python 3.12+
- PowerPoint file (.pptx) in `ppt_input/`
- Face image (.png/.jpg) in `face_images/`

## 🎬 Output

- **Final Video**: `output/final_presentation_with_slides.mp4`
- **Quality**: 1920x1080 Full HD
- **Features**: AI avatar + PowerPoint slides + synchronized narration

## 🔧 Key Improvements

- ✅ **Better Avatar Positioning**: Larger size (640x640) and better placement
- ✅ **Improved Lip-Sync**: Enhanced face detection and padding
- ✅ **Clean Codebase**: Removed all unnecessary files
- ✅ **One Command**: Simple `python backend_only_fixed.py`
- ✅ **Storage Optimized**: Minimal file footprint

## 🎯 Usage

1. **Add your files**:
   - PowerPoint file → `ppt_input/`
   - Face image → `face_images/`

2. **Run the system**:
   ```bash
   python backend_only_fixed.py
   ```

3. **Get your video**: Check `output/final_presentation_with_slides.mp4`

## 📊 System Status

- ✅ AI Processing: SUCCESS
- ✅ Slide Rendering: SUCCESS  
- ✅ Video Composition: SUCCESS
- ✅ Output Files: ALL GENERATED

**Your AI Speaker Avatar System is ready! 🎉**