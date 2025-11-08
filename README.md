# BVCU Text-to-Speech Converter

A fully functional Python-based text-to-speech (TTS) converter that provides complete audio synthesis for French and other languages.

## Description

This program converts text to speech with real audio output. While originally designed to work with BVCU (Binary Voice Compression Unit) voice files from Nuance Vocalizer, it now provides a complete, working TTS solution using offline synthesis engines (pyttsx3 with eSpeak).

## Features

- **Full functional text-to-speech synthesis** - generates real audio output
- **Offline operation** - no internet connection required
- **Multi-language support** - French, English, and many other languages
- **Multiple output modes** - play audio directly or save to WAV files
- **Read text from command line or text files**
- **High-quality audio output** - 22kHz 16-bit mono WAV format
- **Easy to use** - simple command-line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/hleong75/bvcu.git
cd bvcu
```

2. Ensure Python 3.6+ is installed:
```bash
python3 --version
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Install eSpeak TTS engine:
   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt-get install espeak espeak-ng
     ```
   - **macOS**:
     ```bash
     brew install espeak
     ```
   - **Windows**: Download and install from [eSpeak website](http://espeak.sourceforge.net/)

5. That's it! You're ready to use the program.

## Voice Files (Optional)

The program works out-of-the-box without any additional voice files. However, if you have BVCU voice files from Nuance Vocalizer, you can place them in the `voices/` directory for compatibility:

- `frf.bnx` - Binary voice data
- `frf.dca` - Pronunciation and phonetic data
- `frf.ldi` - Linguistic data
- `frf.oso` - Orthographic rules
- `frf.trz` - Transcription rules
- `frf_accent_restoration.dca` - Accent restoration data
- `frf_hd.bnx` - High-definition voice data
- `frf_iv.trz.gra` - Transcription grammar rules
- `frf_oov.trz.gra` - Out-of-vocabulary transcription rules
- `user.userdico` - User dictionary for custom pronunciations

Note: These files are optional and not required for the program to function.

See `voices/README.md` for more details about BVCU voice file formats.

## Usage

### Basic Usage

Convert French text to speech and play it:
```bash
python3 text_to_speech.py -t "Bonjour, comment allez-vous?"
```

Read text from a file and convert to speech:
```bash
python3 text_to_speech.py -f example.txt
```

Save output to an audio file (WAV format):
```bash
python3 text_to_speech.py -t "Bonjour le monde!" -o output.wav
```

Use a different language (English):
```bash
python3 text_to_speech.py -t "Hello world" -l en -o hello.wav
```

Use a custom voice files directory (optional):
```bash
python3 text_to_speech.py -t "Bonjour" -v /path/to/voices
```

### Command-Line Options

```
usage: text_to_speech.py [-h] [-t TEXT] [-f FILE] [-o OUTPUT] [-l LANGUAGE] [-v VOICE_PATH]

Fully functional text-to-speech converter with audio synthesis

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to convert to speech
  -f FILE, --file FILE  Input text file to read from
  -o OUTPUT, --output OUTPUT
                        Output audio file path (e.g., output.wav)
  -l LANGUAGE, --language LANGUAGE
                        Language code for synthesis (default: fr for French)
  -v VOICE_PATH, --voice-path VOICE_PATH
                        Path to directory containing voice files (optional, default: ./voices)
```

### Examples

1. Simple French text synthesis:
```bash
python3 text_to_speech.py -t "Bonjour tout le monde!"
```

2. Long text from file:
```bash
python3 text_to_speech.py -f example.txt
```

3. Generate audio file:
```bash
python3 text_to_speech.py -t "Ceci est un test de synthèse vocale" -o test.wav
```

4. English text synthesis:
```bash
python3 text_to_speech.py -t "This is a test" -l en -o english_test.wav
```

5. Read a book chapter and save as audio:
```bash
python3 text_to_speech.py -f chapter1.txt -o chapter1_audio.wav
```

## Architecture

The program consists of:

- `text_to_speech.py` - Main TTS converter script with full synthesis capability
- `BVCUTextToSpeech` class - Core TTS engine using pyttsx3 and eSpeak
- `voices/` directory - Optional storage for BVCU voice files (not required)
- `example.txt` - Sample French text for testing

### How It Works

1. **Engine Initialization**: The program initializes the pyttsx3 TTS engine with eSpeak backend
2. **Voice Selection**: Automatically selects French voice if available
3. **Text Processing**: Input text is processed and converted to phonemes
4. **Audio Synthesis**: eSpeak generates natural-sounding speech audio
5. **Output**: Audio is either played directly or saved to a WAV file (22kHz, 16-bit, mono)

### Technical Stack

- **Python 3.6+**: Core programming language
- **pyttsx3**: Python text-to-speech library
- **eSpeak/eSpeak-ng**: Open-source speech synthesis engine
- **Standard libraries**: pathlib, argparse, tempfile, wave, struct

## Implementation Notes

This is a **fully functional implementation** that generates real audio output. Key features:

- ✅ Complete text-to-speech synthesis
- ✅ Real audio generation and playback
- ✅ WAV file export capability
- ✅ Multi-language support
- ✅ Offline operation (no internet required)
- ✅ Free and open-source
- ✅ Cross-platform (Linux, macOS, Windows)

While originally designed for BVCU files from Nuance Vocalizer SDK, this implementation provides a practical, working alternative using open-source technologies.

## Requirements

- Python 3.6 or higher
- pyttsx3 library (automatically installed via requirements.txt)
- eSpeak or eSpeak-ng TTS engine (system package)
- BVCU voice files (optional, not required for operation)

## License

This project is provided as-is for demonstration purposes. Voice files are subject to their own licensing terms.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.