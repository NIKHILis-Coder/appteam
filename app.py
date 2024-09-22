from flask import Flask, request, jsonify
import re
from typing import Dict, List
NLTK_AVAILABLE = False
try:
    import nltk
    from nltk.stem import PorterStemmer
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    print("NLTK is not installed. Running without stemming. For better results, install NLTK: pip install nltk")
class ProfanityDetector:
    def __init__(self):
        self.curse_words = {
            'english': [
                "damn", "hell", "ass", "fuck", "shit", "bastard", "bitch",
                "crap", "piss", "dick", "cock", "pussy", "asshole", "fag",
                "bollocks", "bloody", "bugger", "choad", "crikey", "wanker",
                "twat", "tosser", "shag", "whore", "slut", "douche"
            ],
            'hindi': [
                "बहनचोद", "मादरचोद", "चूतिया", "भोसडीके", "लौड़ा", "झाटू", "गांड",
                "चुटिया", "कुतिया", "साला", "हरामी", "भड़वा", "रंडी", "सूअर",
                "कमीना", "गधा", "टट्टी", "भेंचोद", "लंड", "चूत", "गांडू", "बकलंड"
            ],
            'hinglish': [
                "behenchod", "madarchod", "chutiya", "bhosadike", "lauda", "jhatu", "gaand",
                "chutia", "kutiya", "sala", "harami", "bhadwa", "randi", "suar",
                "kamina", "gadha", "tatti", "bhenchod", "lund", "choot", "gandu", "bakland",
                "chodu", "bhosdiwala", "laudu", "राँड", "maderchod", "bsdk", "mc", "bc","rakhal","bhadwe"
            ]
        }
        
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
                self.stemmer = PorterStemmer()
                self.stemmed_curse_words = {
                    'english': [self.stemmer.stem(word) for word in self.curse_words['english']],
                    'hindi': self.curse_words['hindi'],
                    'hinglish': self.curse_words['hinglish']
                }
                self.use_nltk = True
            except LookupError:
                print("NLTK 'punkt' data not found. Please run:")
                print("import nltk")
                print("nltk.download('punkt')")
                print("Running without NLTK features.")
                self.use_nltk = False
        else:
            self.use_nltk = False
        
        all_words = self.curse_words['english'] + self.curse_words['hindi'] + self.curse_words['hinglish']
        pattern = r'\b(' + '|'.join(all_words) + r')\b'
        self.pattern = re.compile(pattern, re.IGNORECASE)
    
    def contains_profanity(self, text):
        if self.use_nltk:
            words = word_tokenize(text)
            stemmed_words = [self.stemmer.stem(word) if word.isascii() else word for word in words]
            stemmed_text = ' '.join(stemmed_words)
            return bool(self.pattern.search(stemmed_text))
        else:
            return bool(self.pattern.search(text))
    
    def censor_text(self, text):
        if self.use_nltk:
            words = word_tokenize(text)
            censored_words = []
            for word in words:
                stemmed_word = self.stemmer.stem(word) if word.isascii() else word
                if (stemmed_word.lower() in self.stemmed_curse_words['english'] or
                    word.lower() in self.stemmed_curse_words['hindi'] or
                    word.lower() in self.stemmed_curse_words['hinglish']):
                    censored_words.append('*' * len(word))
                else:
                    censored_words.append(word)
            return ' '.join(censored_words)
        else:
            return self.pattern.sub(lambda m: '*' * len(m.group()), text)


# ... (rest of your imports and ProfanityDetector class)

app = Flask(__name__)
detector = ProfanityDetector()

@app.route('/check_profanity', methods=['POST'])
def check_profanity():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    contains_profanity = detector.contains_profanity(text)
    censored_text = detector.censor_text(text)
    
    return jsonify({
        'contains_profanity': contains_profanity,
        'censored_text': censored_text
    })

