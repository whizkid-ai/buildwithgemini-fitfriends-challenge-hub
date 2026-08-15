"""Pytest configuration and environment initialization."""

import os
from dotenv import load_dotenv

# Load .env file automatically for pytest runs
load_dotenv()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-6e9778b27cff")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
