import sys
import os

# Add the backend directory to Python path so it can find app.py and gemini_ai.py
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_dir)

# Expose the Flask app for Vercel
from app import app
