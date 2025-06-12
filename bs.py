import os
import json
import gzip
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Define the correct file path
file_path = "btt.json"
gz_file_path = f"{file_path}.gz"

def load_verse_data():
    """Loads verse data from JSON or GZ file and handles errors cleanly."""
    target_file = gz_file_path if os.path.exists(gz_file_path) else file_path
    
    try:
        open_func = gzip.open if target_file.endswith(".gz") else open
        with open_func(target_file, "rt", encoding="utf-8") as f:
            verse_data = json.load(f)
            if not verse_data:
                raise ValueError("JSON file loaded but contains no data.")
            return verse_data
    except Exception as e:
        print(f"❌ ERROR loading {target_file}: {e}")
        return []  # Return empty list if loading fails

verse_data = load_verse_data()
print(f"✅ Loaded {len(verse_data)} verses from {file_path if verse_data else 'NONE'}")

@app.route('/')
def get_random_verse():
    """Returns a random verse or an error if data is missing."""
    if not verse_data:
        return jsonify({"error": "Verse data not loaded. Check server logs."}), 500
    return jsonify(random.choice(verse_data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
