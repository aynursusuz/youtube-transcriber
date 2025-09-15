import logging
import subprocess
import shutil
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


def check_ffmpeg():
    """Check if ffmpeg is available."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg not found. Please install FFmpeg and add it to PATH.")


def download_youtube_audio(url: str, output_path: Path = DOWNLOADS_DIR) -> Path:
    """Download audio from YouTube video using yt-dlp."""
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded_file = None
    
    def download_hook(d):
        nonlocal downloaded_file
        if d['status'] == 'finished':
            downloaded_file = d['filename']
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [download_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if not downloaded_file or not Path(downloaded_file).exists():
            raise RuntimeError("Download failed or file not found")
            
        logging.info(f"Downloaded video: {downloaded_file}")
        return Path(downloaded_file)
        
    except Exception as e:
        logging.error(f"Download error: {e}")
        raise


def convert_to_mp3(input_file: Path) -> Path:
    """Convert downloaded audio file to MP3 using ffmpeg."""
    check_ffmpeg()
    
    output_file = input_file.with_suffix(".mp3")
    
    if input_file.suffix.lower() == '.mp3':
        logging.info("File is already MP3, skipping conversion")
        return input_file
    
    try:
        subprocess.run(
            [
                "ffmpeg", "-i", str(input_file), 
                "-q:a", "0", "-map", "a", 
                "-y", 
                str(output_file)
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logging.info(f"Converted to MP3: {output_file}")
        
        if output_file != input_file:
            input_file.unlink()
            logging.info(f"Removed original file: {input_file}")
        
        return output_file
        
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg conversion failed: {e}")
        if e.stderr:
            logging.error(f"FFmpeg stderr: {e.stderr.decode()}")
        raise


def transcribe_audio(audio_file: Path, model_name: str = "base") -> str:
    """Transcribe audio using Whisper."""
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    
    try:
        logging.info(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        
        logging.info("Starting transcription...")
        # language parametresi kaldırıldı, Whisper otomatik algılar
        result = model.transcribe(str(audio_file))
        transcript = result["text"].strip()

        if transcript:
            TRANSCRIPT_FILE.write_text(transcript, encoding="utf-8")
            logging.info(f"Transcription saved to → {TRANSCRIPT_FILE}")
        else:
            logging.warning("Empty transcription result")
            
        return transcript
        
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        raise


def validate_youtube_url(url: str) -> bool:
    """Basic YouTube URL validation."""
    youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com']
    return any(domain in url.lower() for domain in youtube_domains)


def main():
    try:
        url = input("Enter the YouTube video URL: ").strip()
        if not url:
            logging.error("No URL provided.")
            return
        
        if not validate_youtube_url(url):
            logging.error("Invalid YouTube URL.")
            return

        logging.info("Starting YouTube audio download and transcription...")
        
        video_file = download_youtube_audio(url)
        audio_file = convert_to_mp3(video_file)
        transcript = transcribe_audio(audio_file)

        if transcript:
            print("\n" + "="*50)
            print("TRANSCRIPTION RESULT")
            print("="*50)
            print(transcript)
            print("="*50)
        else:
            print("No transcription could be generated.")
            
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    except Exception as e:
        logging.error(f"Process failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
