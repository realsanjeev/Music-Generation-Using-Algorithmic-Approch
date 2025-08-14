from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

# Specific folders
IMAGE_DIR = DATA_DIR / "images"
OUTPUT_DIR = DATA_DIR / "outputs"
LOG_DIR = DATA_DIR / "logs"

# Create folders if they don’t exist
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Constants
SAMPLE_RATE = 22050
DEFAULT_SCALE = [220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 415.30]

