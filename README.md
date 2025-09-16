# YouTube Transcriber 🎙️
A simple tool to download audio from YouTube videos and transcribe it using Whisper.

---

## Install
```bash
uv venv --python 3.10
uv pip install -e .
```

## Usage
```python
from pathlib import Path
from main import download_youtube_audio, convert_to_mp3, transcribe_audio

url = "https://www.youtube.com/watch?v=2ePf9rue1Ao"

video_file = download_youtube_audio(url)
audio_file = convert_to_mp3(video_file)
transcript = transcribe_audio(audio_file)

print(transcript)
```
##  Acknowledgements
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Whisper](https://github.com/openai/whisper)
- [FFmpeg](https://ffmpeg.org/)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

