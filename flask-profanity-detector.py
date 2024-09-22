import os
from flask import Flask, request, jsonify
import re
from typing import Dict, List

NLTK_AVAILABLE = False
try:
    import nltk
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
    nltk.download('punkt', quiet=True)
except ImportError:
    print("NLTK is not installed. Running without stemming. For better results, install NLTK: pip install nltk")

class ProfanityDetector:
    # ... (rest of the ProfanityDetector class remains the same)

app = Flask(__name__)
detector = ProfanityDetector()

@app.route('/check_profanity', methods=['POST'])
def check_profanity():
    # ... (route handler remains the same)

@app.errorhandler(Exception)
def handle_exception(e):
    # ... (error handler remains the same)

# Remove the if __name__ == '__main__': block from here
