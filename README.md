# YouTube Audio Transcriber

This Python application downloads audio from YouTube videos, converts it to MP3, and then transcribes it using the OpenAI Whisper model. The transcription result is saved in a file named `transcript.txt`.

## Features

- Download audio from YouTube videos using `yt-dlp`  
- Convert audio to MP3 using FFmpeg  
- Transcribe audio with Whisper using automatic language detection  
- Save transcription to `transcript.txt`  
- Simple and clean command-line interface

## Requirements

- Python 3.10+  
- FFmpeg (must be in system PATH)  
- Python packages:  
  ```bash
  pip install yt-dlp whisper torch "numpy<2"

- Note: NumPy version 2.x may cause compatibility issues. Use numpy<2.

##Installation

- Clone the repository or download the main.py file.

- Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

- Install required packages:

```bash
pip install yt-dlp whisper torch "numpy<2"
```

## Usage
- Run the application:

```bash
python main.py
```

- Enter the YouTube video URL.

- After the process completes:

- The MP3 file will be in the downloads/ folder

- The transcription will be in the transcript.txt file

## Notes
- FFmpeg must be installed; otherwise, MP3 conversion will fail.
- Transcription of long videos may take some time.
- Whisper automatically detects the language if no language parameter is provided.

License
MIT License

```sql
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.