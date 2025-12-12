from flask import Flask, request, jsonify, render_template
import difflib
import os
import random
import wave
from vosk import Model, KaldiRecognizer
import json

app = Flask(__name__)

# Load Vosk model
model_path = os.path.join(os.getcwd(), "model")
model = Model(model_path)

# Sentence bank
sentences = [
    "the sun rises in the east",
    "she sells seashells by the seashore",
    "reading books improves knowledge"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_sentence", methods=["GET"])
def get_sentence():
    sentence = random.choice(sentences)
    return jsonify({"sentence": sentence})

@app.route("/evaluate", methods=["POST"])
def evaluate():
    audio_file = request.files["audio"]
    audio_path = "student.wav"
    audio_file.save(audio_path)

    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    text_result = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            text_result += rec.Result()

    text_result += rec.FinalResult()
    spoken = json.loads(text_result).get("text", "")

    correct_sentence = request.form.get("correct_sentence").lower()
    score = difflib.SequenceMatcher(None, correct_sentence, spoken.lower()).ratio() * 100
    result = "✅ Pass" if score >= 70 else "❌ Try Again"

    return jsonify({
        "spoken": spoken,
        "score": round(score,2),
        "result": result,
        "correct_sentence": correct_sentence
    })

if __name__ == "__main__":
    app.run(debug=True)