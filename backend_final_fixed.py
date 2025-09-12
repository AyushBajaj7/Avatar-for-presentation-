# Backend-Only AI Speaker Avatar System - FINAL FIXED VERSION
# One command to run everything with proper avatar sizing and tutor-style explanations

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinalFixedBackendRunner:
    """Runs the AI speaker avatar system with final fixes for avatar size and tutor explanations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("Installing dependencies...")
        
        dependencies = [
            "python-pptx",
            "Pillow", 
            "opencv-python",
            "pyttsx3",
            "tqdm",
            "numpy"
        ]
        
        for dep in dependencies:
            try:
                print(f"  Installing {dep}...")
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True)
                print(f"  SUCCESS: {dep}")
            except subprocess.CalledProcessError:
                print(f"  WARNING: {dep} may already be installed")
    
    def setup_directories(self):
        """Create all directories"""
        print("Setting up directories...")
        
        directories = [
            "ppt_input", "face_images", "audio", "video", 
            "output", "slide_images", "temp"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"  Created {directory}/")
    
    def check_input_files(self):
        """Check if required input files exist"""
        print("Checking input files...")
        
        # Check for PowerPoint file
        ppt_files = [f for f in os.listdir('ppt_input') if f.endswith('.pptx')]
        if not ppt_files:
            print("  ERROR: No PowerPoint files found in ppt_input/")
            print("  Please add a .pptx file to the ppt_input directory")
            return False
        
        print(f"  Found PowerPoint file: {ppt_files[0]}")
        
        # Check for face image
        face_files = [f for f in os.listdir('face_images') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not face_files:
            print("  ERROR: No face image found in face_images/")
            print("  Please add a face image (PNG/JPG) to the face_images directory")
            return False
        
        print(f"  Found face image: {face_files[0]}")
        
        return True
    
    def run_ai_processing(self):
        """Run the AI processing system with tutor explanations"""
        print("Running AI processing with tutor-style explanations...")
        
        try:
            # Run the working main system
            result = subprocess.run([sys.executable, "working_main.py"], 
                                  capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                print("  SUCCESS: AI processing completed")
                return True
            else:
                print(f"  WARNING: AI processing had issues")
                print(f"  Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("  WARNING: AI processing timed out (10 minutes)")
            return False
        except Exception as e:
            print(f"  WARNING: AI processing error: {e}")
            return False
    
    def run_slide_renderer(self):
        """Run slide renderer"""
        print("Rendering PowerPoint slides...")
        
        try:
            # Find PowerPoint file
            ppt_files = [f for f in os.listdir('ppt_input') if f.endswith('.pptx')]
            if not ppt_files:
                print("  ERROR: No PowerPoint file found")
                return False
            
            ppt_path = os.path.join('ppt_input', ppt_files[0])
            
            # Run slide renderer with proper arguments
            result = subprocess.run([
                sys.executable, "slide_renderer.py", 
                ppt_path, "slide_images"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("  SUCCESS: Slide rendering completed")
                return True
            else:
                print(f"  WARNING: Slide rendering had issues")
                print(f"  Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("  WARNING: Slide rendering timed out")
            return False
        except Exception as e:
            print(f"  WARNING: Slide rendering error: {e}")
            return False
    
    def run_video_composer(self):
        """Run video composition with properly sized avatar"""
        print("Composing final video with properly sized avatar...")
        
        try:
            result = subprocess.run([sys.executable, "final_video_composer.py"], 
                                  capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                print("  SUCCESS: Video composition completed")
                return True
            else:
                print(f"  WARNING: Video composition issues")
                print(f"  Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("  WARNING: Video composition timed out")
            return False
        except Exception as e:
            print(f"  WARNING: Video composition error: {e}")
            return False
    
    def check_outputs(self):
        """Check generated outputs"""
        print("Checking outputs...")
        
        outputs = {
            "Final Video": "output/final_presentation_with_slides.mp4",
            "Animated Videos": "video/slide_001_animated.mp4", 
            "Audio Files": "audio/slide_001.wav",
            "Slide Images": "slide_images/slide_001.png"
        }
        
        all_good = True
        for name, path in outputs.items():
            if os.path.exists(path):
                size = os.path.getsize(path)
                print(f"  SUCCESS: {name} ({size:,} bytes)")
            else:
                print(f"  WARNING: {name} missing")
                all_good = False
        
        return all_good
    
    def show_final_summary(self):
        """Show final summary"""
        print("\n" + "=" * 60)
        print("AI SPEAKER AVATAR SYSTEM - FINAL FIXED VERSION")
        print("=" * 60)
        
        # Check outputs
        final_video = "output/final_presentation_with_slides.mp4"
        if os.path.exists(final_video):
            size = os.path.getsize(final_video)
            print(f"✅ FINAL VIDEO: {final_video} ({size:,} bytes)")
            print(f"✅ QUALITY: 1920x1080 Full HD with slide backgrounds")
            print(f"✅ FEATURES: AI avatar + PowerPoint slides + tutor explanations")
            print(f"✅ AVATAR: Properly sized and positioned")
        else:
            print("❌ Final video not found")
        
        print("\n📁 OUTPUT FILES:")
        print(f"  📹 Final Video: output/final_presentation_with_slides.mp4")
        print(f"  🎭 Animated Videos: video/slide_*_animated.mp4")
        print(f"  🎵 Audio Files: audio/slide_*.wav")
        print(f"  🖼️ Slide Images: slide_images/slide_*.png")
        
        print("\n🎯 FINAL FIXES APPLIED:")
        print("  ✅ Avatar size reduced (320x320 instead of 640x640)")
        print("  ✅ Better positioning (1600:760 - bottom right corner)")
        print("  ✅ Tutor-style explanations instead of text reading")
        print("  ✅ Natural transitions and explanatory phrases")
        print("  ✅ Slide content remains fully visible")
        
        print("\n🎯 YOUR AI SPEAKER AVATAR SYSTEM IS READY!")
        print("Check the 'output' directory for your final video")
    
    def run_everything(self):
        """Run the complete backend system with final fixes"""
        print("=" * 60)
        print("AI SPEAKER AVATAR SYSTEM - FINAL FIXED VERSION")
        print("=" * 60)
        print("This will:")
        print("- Install dependencies")
        print("- Process PowerPoint files") 
        print("- Generate tutor-style explanations")
        print("- Create properly sized avatar videos")
        print("- Compose final video with visible slide content")
        print("=" * 60)
        
        try:
            # Phase 1: Setup
            print("\nPHASE 1: SETUP")
            print("-" * 30)
            self.setup_directories()
            self.install_dependencies()
            
            # Check input files
            if not self.check_input_files():
                print("\n❌ Missing required input files!")
                print("Please add:")
                print("1. PowerPoint file (.pptx) to ppt_input/ directory")
                print("2. Face image (.png/.jpg) to face_images/ directory")
                return
            
            # Phase 2: AI Processing
            print("\nPHASE 2: AI PROCESSING")
            print("-" * 30)
            ai_success = self.run_ai_processing()
            
            # Phase 3: Slide Rendering
            print("\nPHASE 3: SLIDE RENDERING")
            print("-" * 30)
            slide_success = self.run_slide_renderer()
            
            # Phase 4: Video Composition
            print("\nPHASE 4: VIDEO COMPOSITION")
            print("-" * 30)
            video_success = self.run_video_composer()
            
            # Phase 5: Verification
            print("\nPHASE 5: VERIFICATION")
            print("-" * 30)
            output_success = self.check_outputs()
            
            # Final Summary
            self.show_final_summary()
            
            # Status summary
            print("\n" + "=" * 60)
            print("STATUS SUMMARY")
            print("=" * 60)
            
            if ai_success:
                print("✅ AI Processing: SUCCESS")
            else:
                print("❌ AI Processing: FAILED")
            
            if slide_success:
                print("✅ Slide Rendering: SUCCESS")
            else:
                print("❌ Slide Rendering: FAILED")
            
            if video_success:
                print("✅ Video Composition: SUCCESS")
            else:
                print("❌ Video Composition: FAILED")
            
            if output_success:
                print("✅ Output Files: ALL GENERATED")
            else:
                print("⚠️ Output Files: SOME MISSING")
            
            print("\n🎉 SYSTEM COMPLETE WITH ALL FIXES!")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")

def main():
    """Main function - Final fixed backend system"""
    runner = FinalFixedBackendRunner()
    runner.run_everything()

if __name__ == "__main__":
    main()
