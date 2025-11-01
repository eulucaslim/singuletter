from dotenv import load_dotenv
from typing import Final
import logging
import os

load_dotenv()

# Configure basic logging (optional, but good for quick starts)
logging.basicConfig(level=logging.INFO, format=(
    '%(asctime)s - %(levelname)s - %(message)s')
)
# Get a logger instance
logger = logging.getLogger(__name__)

# Envs
API_PORT: Final[int] = int(os.getenv("API_PORT", 8001))
GEMINI_API_KEY: Final[str] = os.getenv("GEMINI_API_KEY")