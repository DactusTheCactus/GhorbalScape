# utils.py

import json
import os
from config import SCORES_FILE

def load_scores():
    try:
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_score(score):
    scores = load_scores()
    scores.append({"score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep top 10 scores
    
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)
