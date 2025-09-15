import logging
import subprocess
from pathlib import Path
import yt_dlp
import whisper

# Logging configuration
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)

DOWNLOADS_DIR = Path("downloads")
TRANSCRIPT_FILE = Path("transcript.txt")


def download_youtube_audio(url: str, output_path: Path = DOWNLOADS_DIR) -> Path:
    """Download audio from YouTube video using yt-dlp."""
    output_path.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    
    logging.info(f"Downloaded video: {filename}")
    return Path(filename)


def convert_to_mp3(input_file: Path) -> Path:
    """Convert downloaded audio file to MP3 using ffmpeg."""
    output_file = input_file.with_suffix(".mp3")
    try:
        subprocess.run(
            ["ffmpeg", "-i", str(input_file), "-q:a", "0", "-map", "a", str(output_file)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logging.info(f"Converted to MP3: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg error: {e}")
        raise


def transcribe_audio(audio_file: Path, model_name: str = "base") -> str:
    """Transcribe audio using Whisper."""
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_file), language="en")
    transcript = result["text"]

    TRANSCRIPT_FILE.write_text(transcript, encoding="utf-8")
    logging.info(f"Transcription saved to → {TRANSCRIPT_FILE}")
    return transcript


def main():
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        logging.error("No valid URL provided.")
        return

    video_file = download_youtube_audio(url)
    audio_file = convert_to_mp3(video_file)
    transcript = transcribe_audio(audio_file)

    print("\n--- TRANSCRIPTION RESULT ---\n")
    print(transcript)


if __name__ == "__main__":
    main()
