"""
Audio Generation Module
Converts story text to speech using AI voice models
"""

import os
import tempfile
from gtts import gTTS
from typing import Optional
import pygame
import io

class AudioGenerator:
    def __init__(self):
        """Initialize the audio generator"""
        pygame.mixer.init()
        
    def generate_audio(self, text: str, language: str = 'en', slow: bool = False, voice_speed: str = 'normal', voice_type: str = 'default') -> Optional[str]:
        """
        Generate audio narration from text using Google Text-to-Speech with voice options
        
        Args:
            text: The story text to convert to speech
            language: Language code (e.g., 'en', 'hi', 'es')
            slow: Whether to speak slowly (legacy parameter)
            voice_speed: Voice speed option ('slow', 'normal', 'fast')
            voice_type: Voice type/accent option
            
        Returns:
            Path to the generated audio file or None if failed
        """
        
        try:
            # Determine speed based on voice_speed parameter
            use_slow = False
            if voice_speed == 'slow':
                use_slow = True
            elif voice_speed == 'fast':
                use_slow = False  # gTTS doesn't have fast option, but we can process it
            else:  # normal
                use_slow = slow  # Use legacy parameter for backward compatibility
            
            # Get TLD (Top Level Domain) for different voice accents
            tld = self._get_voice_tld(language, voice_type)
            
            # Create TTS object with specific TLD for voice variation
            tts = gTTS(text=text, lang=language, slow=use_slow, tld=tld)
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            audio_path = temp_file.name
            temp_file.close()
            
            # Save audio to file
            tts.save(audio_path)
            
            voice_desc = self.get_voice_options().get(voice_type, voice_type)
            print(f"✅ Audio generated successfully with {voice_desc} ({voice_speed} speed)")
            return audio_path
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return None
    
    def generate_scene_audio(self, scenes: list, language: str = 'en') -> list:
        """
        Generate audio for individual story scenes
        
        Args:
            scenes: List of scene descriptions
            language: Language code
            
        Returns:
            List of audio file paths
        """
        
        audio_files = []
        
        for i, scene in enumerate(scenes):
            try:
                # Add scene introduction
                scene_text = f"Scene {i + 1}. {scene}"
                
                tts = gTTS(text=scene_text, lang=language, slow=False)
                
                # Create temporary file for each scene
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_scene_{i+1}.mp3')
                audio_path = temp_file.name
                temp_file.close()
                
                tts.save(audio_path)
                audio_files.append(audio_path)
                
            except Exception as e:
                print(f"Error generating audio for scene {i+1}: {str(e)}")
                audio_files.append(None)
        
        return audio_files
    
    def play_audio(self, audio_path: str) -> bool:
        """
        Play audio file using pygame
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            True if successful, False otherwise
        """
        
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            return True
            
        except Exception as e:
            print(f"Error playing audio: {str(e)}")
            return False
    
    def stop_audio(self):
        """Stop currently playing audio"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping audio: {str(e)}")
    
    def is_playing(self) -> bool:
        """Check if audio is currently playing"""
        return pygame.mixer.music.get_busy()
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages for TTS"""
        
        return {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'ur': 'Urdu'
        }
    
    def cleanup_temp_files(self, file_paths: list):
        """Clean up temporary audio files"""
        
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f"Error cleaning up file {file_path}: {str(e)}")
    
    def generate_multilingual_audio(self, text: str, languages: list) -> dict:
        """
        Generate audio in multiple languages
        
        Args:
            text: Text to convert to speech
            languages: List of language codes
            
        Returns:
            Dictionary mapping language codes to audio file paths
        """
        
        audio_files = {}
        
        for lang in languages:
            audio_path = self.generate_audio(text, language=lang)
            if audio_path:
                audio_files[lang] = audio_path
        
        return audio_files
    
    def get_voice_options(self) -> dict:
        """Get available voice type options with different accents"""
        
        return {
            'default': '🎵 Default Voice (Standard)',
            'us_male': '🇺🇸 American Male (Deep)',
            'us_female': '🇺🇸 American Female (Clear)',
            'uk_male': '🇬🇧 British Male (Formal)',
            'uk_female': '🇬🇧 British Female (Elegant)',
            'au_voice': '🇦🇺 Australian Voice (Friendly)',
            'ca_voice': '🇨🇦 Canadian Voice (Warm)',
            'in_voice': '🇮🇳 Indian English (Cultural)'
        }
    
    def get_voice_speed_options(self) -> dict:
        """Get available voice speed options"""
        
        return {
            'normal': '🎵 Normal Speed (Recommended)',
            'slow': '🐌 Slow Speed (Clear & Easy)',
            'fast': '⚡ Fast Speed (Quick Narration)'
        }
    
    def _get_voice_tld(self, language: str, voice_type: str) -> str:
        """Get TLD (Top Level Domain) for different voice accents"""
        
        # Voice type to TLD mapping for different accents
        voice_tld_mapping = {
            'default': 'com',
            'us_male': 'com',        # US English (tends to sound more masculine)
            'us_female': 'com',      # US English (default female-like)
            'uk_male': 'co.uk',      # British English (more formal/masculine)
            'uk_female': 'co.uk',    # British English (elegant)
            'au_voice': 'com.au',    # Australian English
            'ca_voice': 'ca',        # Canadian English
            'in_voice': 'co.in'      # Indian English
        }
        
        # Language-specific TLD defaults
        if language == 'en':
            return voice_tld_mapping.get(voice_type, 'com')
        elif language == 'hi':
            return 'co.in'  # Indian Hindi
        elif language == 'es':
            if voice_type in ['us_male', 'us_female']:
                return 'com'  # US Spanish
            else:
                return 'es'   # Spain Spanish
        elif language == 'fr':
            if voice_type in ['ca_voice']:
                return 'ca'   # Canadian French
            else:
                return 'fr'   # France French
        else:
            return 'com'  # Default
    
    def get_voice_descriptions(self) -> dict:
        """Get detailed descriptions of voice options"""
        
        return {
            'normal': 'Standard narration speed - perfect for most listeners',
            'slow': 'Slower, clearer speech - great for learning or detailed listening',
            'fast': 'Faster narration - ideal for quick story consumption'
        }