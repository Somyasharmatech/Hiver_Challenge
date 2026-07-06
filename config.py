import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# App Configuration
APP_NAME = "AI Email Response Intelligence"
APP_DESCRIPTION = "Generate professional customer support replies and automatically evaluate response quality using advanced NLP metrics."

# Model Configuration
GEMINI_MODEL_NAME = "gemini-1.5-flash"  # Using 1.5 flash for speed and reliability, can be changed to 1.5 pro
MAX_WORDS = 150
MIN_WORDS = 60

# Thresholds
CONFIDENCE_THRESHOLD = 85.0
EXCELLENT_SCORE_THRESHOLD = 90.0
NEEDS_REVIEW_SCORE_THRESHOLD = 70.0
