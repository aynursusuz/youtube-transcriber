import os
import logging
import subprocess
from pytube import YouTube
import whisper
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

def sanitize_filename(name: str) -> str:
    """Dosya adından sorunlu karakterleri temizle"""
    safe = "".join(c if c.isalnum() or c in (" ", ".", "_") else "_" for c in name)
    return safe.strip().replace(" ", "_")

def download_video(url: str) -> str:
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = sanitize_filename(yt.title) + ".mp4"
    output_path = DOWNLOAD_DIR / filename
    stream.download(output_path=str(output_path))
    logging.info(f"Downloaded video: {output_path}")
    return str(output_path)

def extract_audio(video_file: str) -> str:
    """Videodan mp3 çıkarır"""
    audio_file = video_file.replace(".mp4", ".mp3")
    cmd = ["ffmpeg", "-y", "-i", video_file, "-vn", "-acodec", "mp3", audio_file]
    subprocess.run(cmd, check=True)
    logging.info(f"Extracted audio: {audio_file}")
    return audio_file

def transcribe_audio(audio_file: str) -> str:
    """Whisper ile sesi yazıya çevir"""
    model = whisper.load_model("small")  # küçük model hızlıdır, gpu kullanır
    result = model.transcribe(audio_file)
    text_file = audio_file.replace(".mp3", ".txt")
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    logging.info(f"Transcript saved: {text_file}")
    return text_file

def main():
    url = input("Enter the YouTube video URL: ").strip()
    if not url:
        logging.error("No valid URL provided.")
        return
    
    video_file = download_video(url)
    audio_file = extract_audio(video_file)
    transcript_file = transcribe_audio(audio_file)
    print(f"Transcript hazır: {transcript_file}")

if __name__ == "__main__":
    main()
