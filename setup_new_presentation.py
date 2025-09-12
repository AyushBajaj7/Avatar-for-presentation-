# Setup New Presentation - Clean System
# Prepares the system for a new PowerPoint file

import os
import shutil
from pathlib import Path

def setup_new_presentation():
    """Clean and setup system for new presentation"""
    print("🧹 CLEANING SYSTEM FOR NEW PRESENTATION")
    print("=" * 50)
    
    # Clean all generated files
    directories_to_clean = ['audio', 'video', 'output', 'slide_images', 'temp']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"  ✅ Removed: {file}")
    
    # Clean logs
    log_files = [f for f in os.listdir('.') if f.endswith('.log')]
    for log_file in log_files:
        os.remove(log_file)
        print(f"  ✅ Removed: {log_file}")
    
    # Clean old PowerPoint files
    ppt_files = [f for f in os.listdir('ppt_input') if f.endswith('.pptx')]
    for ppt_file in ppt_files:
        os.remove(os.path.join('ppt_input', ppt_file))
        print(f"  ✅ Removed: {ppt_file}")
    
    print("\n📁 SYSTEM READY FOR NEW PRESENTATION")
    print("=" * 50)
    print("✅ All generated files cleaned")
    print("✅ System reset and ready")
    print("\n📋 NEXT STEPS:")
    print("1. Add your new PowerPoint file (.pptx) to: ppt_input/")
    print("2. Add your face image (.png/.jpg) to: face_images/")
    print("3. Run: python backend_final_fixed.py")
    print("\n🎯 Your system is clean and ready!")

if __name__ == "__main__":
    setup_new_presentation()
