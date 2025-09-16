#!/usr/bin/env python3
"""
Download Wav2Lip model weights
==============================
This script downloads the required Wav2Lip model weights.
"""

import os
import requests
import gdown
from pathlib import Path

def download_wav2lip_model():
    """Download Wav2Lip GAN model weights"""
    
    # Create checkpoints directory if it doesn't exist
    checkpoints_dir = Path("Wav2Lip/checkpoints")
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    
    # Wav2Lip GAN model Google Drive ID
    # From: https://drive.google.com/file/d/15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk/view?usp=share_link
    model_id = "15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk"
    output_path = checkpoints_dir / "wav2lip_gan.pth"
    
    print("🔽 Downloading Wav2Lip GAN model weights...")
    print(f"   Source: Google Drive ID {model_id}")
    print(f"   Destination: {output_path}")
    
    try:
        # Download using gdown
        gdown.download(f"https://drive.google.com/uc?id={model_id}", str(output_path), quiet=False)
        
        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"✅ SUCCESS: Downloaded Wav2Lip GAN model to {output_path}")
            print(f"   File size: {output_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("❌ ERROR: Downloaded file is empty or doesn't exist")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to download model: {e}")
        print("\n🔧 Manual download instructions:")
        print("1. Go to: https://drive.google.com/file/d/15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk/view?usp=share_link")
        print("2. Download the file")
        print(f"3. Place it in: {output_path}")
        return False

def download_face_detection_model():
    """Download face detection model weights"""
    
    # Create face detection directory
    face_detection_dir = Path("Wav2Lip/face_detection/detection/sfd")
    face_detection_dir.mkdir(parents=True, exist_ok=True)
    
    # Face detection model URL
    model_url = "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"
    output_path = face_detection_dir / "s3fd.pth"
    
    print("\n🔽 Downloading face detection model weights...")
    print(f"   Source: {model_url}")
    print(f"   Destination: {output_path}")
    
    try:
        response = requests.get(model_url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"✅ SUCCESS: Downloaded face detection model to {output_path}")
            print(f"   File size: {output_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print("❌ ERROR: Downloaded file is empty or doesn't exist")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: Failed to download face detection model: {e}")
        return False

def main():
    """Download all required Wav2Lip models"""
    print("🤖 Wav2Lip Model Downloader")
    print("=" * 40)
    
    # Install gdown if not available
    try:
        import gdown
    except ImportError:
        print("📦 Installing gdown...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown
    
    success_count = 0
    
    # Download Wav2Lip GAN model
    if download_wav2lip_model():
        success_count += 1
    
    # Download face detection model
    if download_face_detection_model():
        success_count += 1
    
    print("\n" + "=" * 40)
    if success_count == 2:
        print("🎉 All models downloaded successfully!")
        print("Wav2Lip should now work properly.")
    else:
        print(f"⚠️  {success_count}/2 models downloaded successfully.")
        print("Some models failed to download. Check the errors above.")

if __name__ == "__main__":
    main()
