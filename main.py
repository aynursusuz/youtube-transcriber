import logging
from pathlib import Path
from pydub import AudioSegment
import whisper
import pandas as pd
from datasets import Dataset, Audio
from huggingface_hub import login

# -------------------------
# Constants
# -------------------------
CHUNKS_DIR = Path("chunks")
TRANSCRIPTS_DIR = Path("chunks")
PARQUET_FILE = Path("youtube_dataset.parquet")
LINE_WIDTH = 80
MODEL_NAME = "large"

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)

# -------------------------
# Helper functions
# -------------------------
def transcribe_audio(audio_file: Path, model):
    result = model.transcribe(str(audio_file))
    return result["text"].strip()


def wrap_text(text: str, width: int = LINE_WIDTH):
    import textwrap
    return "\n".join(textwrap.wrap(text, width=width))


def create_dataset(chunks_dir: Path, transcripts_dir: Path):
    """
    Create a Hugging Face Dataset with audio and transcript columns.
    """
    data = []
    for chunk_file in sorted(chunks_dir.glob("*.mp3")):
        transcript_file = transcripts_dir / f"{chunk_file.stem}.txt"
        if transcript_file.exists():
            with open(transcript_file, "r", encoding="utf-8") as f:
                text = f.read()
            data.append({
                "audio": str(chunk_file.resolve()),  # datasets Audio type expects path
                "transcript": text
            })

    ds = Dataset.from_list(data)
    ds = ds.cast_column("audio", Audio(sampling_rate=16000))  # Convert path -> Audio
    return ds


def push_to_huggingface(ds, repo_id: str, token: str):
    """
    Push Dataset to Hugging Face Hub
    """
    login(token=token)
    ds.push_to_hub(repo_id)
    logging.info(f"Pushed dataset to Hugging Face Hub: {repo_id}")


# -------------------------
# Main
# -------------------------
def main():
    # Load Whisper model
    model = whisper.load_model(MODEL_NAME)

    # Create Hugging Face Dataset
    ds = create_dataset(CHUNKS_DIR, TRANSCRIPTS_DIR)

    # Push to Hugging Face
    HF_TOKEN = "hf_token"  # Replace with your Hugging Face token
    REPO_ID = "Aynursusuz/yt-test"  # Replace with your repo path
    push_to_huggingface(ds, REPO_ID, HF_TOKEN)


if __name__ == "__main__":
    main()

