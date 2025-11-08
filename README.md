# BVCU Text-to-Speech Converter

A Python-based text-to-speech (TTS) converter that uses BVCU (Binary Voice Compression Unit) voice files for French language synthesis.

## Description

This program converts text to speech using BVCU voice files, which are part of the Nuance Vocalizer or compatible TTS engine voice packages. It supports French language synthesis using the frf (French) voice files.

## Features

- Convert text to speech using BVCU voice files
- Support for French language (frf) voice files
- Read text from command line or text files
- Optional audio file output
- Extensible architecture for additional languages

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

3. Place your BVCU voice files in the `voices/` directory (see [Voice Files](#voice-files) section)

## Voice Files

The program requires the following BVCU voice files in the `voices/` directory:

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

See `voices/README.md` for more details about voice file formats and obtaining them.

## Usage

### Basic Usage

Convert text directly:
```bash
python3 text_to_speech.py -t "Bonjour, comment allez-vous?"
```

Read text from a file:
```bash
python3 text_to_speech.py -f input.txt
```

Save output to an audio file:
```bash
python3 text_to_speech.py -t "Bonjour le monde!" -o output.wav
```

Use a custom voice files directory:
```bash
python3 text_to_speech.py -t "Bonjour" -v /path/to/voices
```

### Command-Line Options

```
usage: text_to_speech.py [-h] [-t TEXT] [-f FILE] [-o OUTPUT] [-v VOICE_PATH]

Convert text to speech using BVCU voice files

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to convert to speech
  -f FILE, --file FILE  Input text file to read from
  -o OUTPUT, --output OUTPUT
                        Output audio file path (e.g., output.wav)
  -v VOICE_PATH, --voice-path VOICE_PATH
                        Path to directory containing BVCU voice files (default: ./voices)
```

### Examples

1. Simple text synthesis:
```bash
python3 text_to_speech.py -t "Bonjour!"
```

2. Long text from file:
```bash
echo "Ceci est un exemple de synthèse vocale en français." > example.txt
python3 text_to_speech.py -f example.txt
```

3. Generate audio file:
```bash
python3 text_to_speech.py -t "Au revoir" -o goodbye.wav
```

## Architecture

The program consists of:

- `text_to_speech.py` - Main TTS converter script
- `BVCUTextToSpeech` class - Core TTS engine that loads and uses BVCU voice files
- `voices/` directory - Storage for BVCU voice files

### How It Works

1. **Voice Loading**: The program loads BVCU voice files from the specified directory
2. **Text Processing**: Input text is processed for linguistic analysis
3. **Synthesis**: Text is converted to speech using the voice data
4. **Output**: Audio is played or saved to a file

## Implementation Notes

This is a demonstration implementation that shows the structure for working with BVCU files. Full synthesis requires:

- Nuance Vocalizer SDK or compatible TTS engine
- Proper licensing for BVCU voice files
- Audio processing libraries (e.g., for WAV file generation)

For production use, integrate with a proper TTS engine that supports BVCU format.

## Requirements

- Python 3.6 or higher
- BVCU voice files (must be obtained separately)
- Nuance Vocalizer SDK (for full synthesis capability)

## License

This project is provided as-is for demonstration purposes. Voice files are subject to their own licensing terms.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.