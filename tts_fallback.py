# Fallback TTS System
# This module provides a fallback TTS implementation using pyttsx3
# when Coqui TTS is not available or fails

import os
import logging
from typing import Optional, Dict

class FallbackTTS:
    """Fallback TTS using pyttsx3 for when Coqui TTS is not available"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.engine = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the pyttsx3 TTS engine"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to set a female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.engine.setProperty('rate', int(200 * self.config.get('speed', 1.0)))
            self.engine.setProperty('volume', 0.9)
            
            self.logger.info("✅ Fallback TTS (pyttsx3) initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize fallback TTS: {e}")
            self.engine = None
    
    def is_available(self) -> bool:
        """Check if TTS is available"""
        return self.engine is not None
    
    def generate_audio(self, text: str, output_path: str) -> bool:
        """Generate audio from text"""
        if not self.engine:
            self.logger.error("Fallback TTS not initialized")
            return False
        
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generate audio
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            # Verify file was created
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                self.logger.info(f"✅ Generated audio: {output_path}")
                return True
            else:
                self.logger.error(f"❌ Audio file not created or empty: {output_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error generating audio: {e}")
            return False
    
    def cleanup(self):
        """Cleanup TTS engine"""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
            self.engine = None

class TTSManager:
    """TTS Manager that tries Coqui TTS first, falls back to pyttsx3"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.coqui_tts = None
        self.fallback_tts = None
        self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize TTS systems"""
        # Try Coqui TTS first
        try:
            from TTS.api import TTS
            self.coqui_tts = TTS(model_name=self.config.get('model', 'tts_models/en/ljspeech/tacotron2-DDC'))
            self.logger.info("✅ Coqui TTS initialized successfully")
            return
        except Exception as e:
            self.logger.warning(f"⚠️ Coqui TTS not available: {e}")
        
        # Fall back to pyttsx3
        self.fallback_tts = FallbackTTS(self.config)
        if self.fallback_tts.is_available():
            self.logger.info("✅ Using fallback TTS (pyttsx3)")
        else:
            self.logger.error("❌ No TTS system available")
    
    def is_available(self) -> bool:
        """Check if any TTS system is available"""
        return self.coqui_tts is not None or (self.fallback_tts and self.fallback_tts.is_available())
    
    def generate_audio(self, text: str, output_path: str) -> bool:
        """Generate audio using available TTS system"""
        if self.coqui_tts:
            try:
                self.coqui_tts.tts_to_file(text=text, file_path=output_path)
                self.logger.info(f"✅ Generated audio with Coqui TTS: {output_path}")
                return True
            except Exception as e:
                self.logger.warning(f"⚠️ Coqui TTS failed: {e}, trying fallback")
        
        if self.fallback_tts and self.fallback_tts.is_available():
            return self.fallback_tts.generate_audio(text, output_path)
        
        self.logger.error("❌ No working TTS system available")
        return False
    
    def cleanup(self):
        """Cleanup TTS systems"""
        if self.fallback_tts:
            self.fallback_tts.cleanup()
        self.coqui_tts = None
        self.fallback_tts = None
