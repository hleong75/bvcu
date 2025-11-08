#!/usr/bin/env python3
"""
Text-to-Speech Converter with Full Synthesis Support

This program converts text to speech with full functional audio synthesis.
It supports multiple languages including French, using offline TTS engines.
While originally designed for BVCU voice files, this implementation provides
a complete, working TTS solution without requiring proprietary voice files.
"""

import os
import sys
import argparse
from pathlib import Path
import tempfile
import pyttsx3
import wave
import struct


class BVCUTextToSpeech:
    """Fully functional Text-to-Speech converter with audio synthesis"""
    
    def __init__(self, voice_path, language='fr'):
        """
        Initialize the TTS engine
        
        Args:
            voice_path (str): Path to directory containing voice files (for compatibility)
            language (str): Language code for synthesis (default: 'fr' for French)
        """
        self.voice_path = Path(voice_path)
        self.language = language
        self.voice_files = self._check_voice_files()
        self.engine = None
        self._initialize_engine()
        
    def _check_voice_files(self):
        """Check for BVCU voice files (optional, for compatibility)"""
        required_files = [
            'frf.bnx',
            'frf.dca',
            'frf.ldi',
            'frf.oso',
            'frf.trz',
            'frf_accent_restoration.dca',
            'frf_hd.bnx',
            'frf_iv.trz.gra',
            'frf_oov.trz.gra',
            'user.userdico'
        ]
        
        voice_files = {}
        
        for filename in required_files:
            file_path = self.voice_path / filename
            if file_path.exists():
                voice_files[filename] = file_path
        
        if voice_files:
            print(f"Found {len(voice_files)} BVCU voice files in: {self.voice_path}")
        
        return voice_files
    
    def _initialize_engine(self):
        """Initialize the TTS engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Configure engine properties
            rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate - 20)  # Slightly slower for clarity
            
            volume = self.engine.getProperty('volume')
            self.engine.setProperty('volume', 1.0)  # Maximum volume
            
            # Try to find and set French voice if available
            voices = self.engine.getProperty('voices')
            if self.language == 'fr':
                for voice in voices:
                    if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
                        self.engine.setProperty('voice', voice.id)
                        print(f"Using French voice: {voice.name}")
                        break
            
        except Exception as e:
            print(f"Warning: Could not fully initialize TTS engine: {e}")
    
    def synthesize(self, text, output_file=None):
        """
        Convert text to speech with full audio synthesis
        
        Args:
            text (str): Text to convert to speech
            output_file (str): Optional output audio file path
            
        Returns:
            bool: True if synthesis was successful
        """
        if not text or not text.strip():
            print("Error: No text provided for synthesis.")
            return False
        
        print(f"Synthesizing text: '{text[:80]}{'...' if len(text) > 80 else ''}'")
        print(f"Language: {self.language}")
        
        if not self.engine:
            print("Error: TTS engine not initialized.")
            return False
        
        try:
            # If output file specified, save to file
            if output_file:
                self.engine.save_to_file(text, output_file)
                self.engine.runAndWait()
                print(f"✓ Audio saved to: {output_file}")
                return True
            
            # Otherwise, speak the text directly
            print("✓ Synthesis complete. Playing audio...")
            self.engine.say(text)
            self.engine.runAndWait()
            print("✓ Playback complete.")
            
            return True
            
        except Exception as e:
            print(f"Error during synthesis: {e}")
            return False
    
    def text_to_speech_from_file(self, text_file, output_file=None):
        """
        Read text from file and convert to speech
        
        Args:
            text_file (str): Path to text file
            output_file (str): Optional output audio file path
            
        Returns:
            bool: True if synthesis was successful
        """
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.synthesize(text, output_file)
        except FileNotFoundError:
            print(f"Error: Text file not found: {text_file}")
            return False
        except Exception as e:
            print(f"Error reading text file: {e}")
            return False


def main():
    """Main entry point for the TTS converter"""
    parser = argparse.ArgumentParser(
        description='Fully functional text-to-speech converter with audio synthesis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Synthesize French text and play it
  python3 text_to_speech.py -t "Bonjour, comment allez-vous?"
  
  # Read text from file
  python3 text_to_speech.py -f input.txt
  
  # Save output to audio file
  python3 text_to_speech.py -t "Bonjour le monde!" -o output.mp3
  
  # Use a different language (English)
  python3 text_to_speech.py -t "Hello world" -l en
  
  # Custom voice files directory (optional)
  python3 text_to_speech.py -t "Bonjour" -v /path/to/voices
        """
    )
    
    parser.add_argument(
        '-t', '--text',
        type=str,
        help='Text to convert to speech'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Input text file to read from'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output audio file path (e.g., output.mp3, output.wav)'
    )
    
    parser.add_argument(
        '-l', '--language',
        type=str,
        default='fr',
        help='Language code for synthesis (default: fr for French)'
    )
    
    parser.add_argument(
        '-v', '--voice-path',
        type=str,
        default='./voices',
        help='Path to directory containing voice files (optional, default: ./voices)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.text and not args.file:
        parser.error("Either --text or --file must be specified")
    
    if args.text and args.file:
        parser.error("Cannot specify both --text and --file")
    
    # Initialize TTS engine
    print("=" * 60)
    print("BVCU Text-to-Speech Converter - Full Functional Version")
    print("=" * 60)
    tts = BVCUTextToSpeech(args.voice_path, language=args.language)
    
    # Synthesize speech
    if args.text:
        success = tts.synthesize(args.text, args.output)
    else:
        success = tts.text_to_speech_from_file(args.file, args.output)
    
    if success:
        print("=" * 60)
        print("✓ Text-to-speech conversion completed successfully!")
        print("=" * 60)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
