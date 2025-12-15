from flask import Flask, render_template, request, jsonify
import random
import requests

app = Flask(
    __name__,
    template_folder="language_lab/templates",
    static_folder="language_lab/static"
)

# ---------------- Sample word bank ----------------
word_bank = {
    "jr_kg": {"easy": ["cat", "dog"], "medium": ["fish", "bird"], "hard": ["tiger", "elephant"]},
    "sr_kg": {"easy": ["apple", "ball"], "medium": ["chair", "table"], "hard": ["giraffe", "monkey"]},
    "1": {"easy": ["sun", "moon"], "medium": ["house", "tree"], "hard": ["computer", "bicycle"]}
}

# ---------------- Sample sentences ----------------
sentence_bank = {
    "1": {
        "easy": ["I like cats.", "The sun is bright."],
        "medium": ["My house has a big garden.", "She is reading a book."],
        "hard": ["The computer is very fast.", "We went to the zoo yesterday."]
    }
}

# ---------------- Pages ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<page>")
def pages(page):
    return render_template(page)

# ---------------- APIs ----------------
@app.route("/get_word")
def get_word():
    grade = request.args.get("grade")
    level = request.args.get("level")
    words = word_bank.get(grade, {}).get(level, ["hello"])
    return jsonify({"word": random.choice(words)})

@app.route("/get_sentence")
def get_sentence():
    grade = request.args.get("grade")
    level = request.args.get("level")
    sentences = sentence_bank.get(grade, {}).get(level, ["Hello world."])
    return jsonify({"sentence": random.choice(sentences)})

@app.route("/check_sentence", methods=["POST"])
def check_sentence():
    sentence = request.form.get("sentence", "")

    response = requests.post(
        "https://api.languagetool.org/v2/check",
        data={"text": sentence, "language": "en-US"},
        timeout=10
    )

    result = response.json()
    corrected = sentence
    matches = result.get("matches", [])
    matches.sort(key=lambda x: x["offset"], reverse=True)

    for m in matches:
        if m.get("replacements"):
            corrected = (
                corrected[:m["offset"]] +
                m["replacements"][0]["value"] +
                corrected[m["offset"] + m["length"]:]
            )

    return jsonify({"corrected": corrected})

