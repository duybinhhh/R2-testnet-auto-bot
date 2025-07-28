from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Constants
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ADDRESS = os.getenv("ADDRESS")
