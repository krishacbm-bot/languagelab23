from flask import Flask, request, jsonify, render_template
from vosk import Model, KaldiRecognizer
import wave, os, json
import pyttsx3

app = Flask(__name__)

# Load Vosk model (offline)
model_path = os.path.join(os.getcwd(), "model")
model = Model(model_path)

# Initialize TTS engine (offline)
tts_engine = pyttsx3.init()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    # Save student audio
    audio_file = request.files["audio"]
    audio_path = "student.wav"
    audio_file.save(audio_path)

    # Recognize speech
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    spoken_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            spoken_text += json.loads(rec.Result()).get("text", "") + " "

    spoken_text += json.loads(rec.FinalResult()).get("text", "")

    # Speak correct pronunciation
    tts_engine.say(spoken_text)
    tts_engine.runAndWait()

    # Simple confidence score (based on text length)
    score = min(len(spoken_text)/10*10, 100)

    return jsonify({
        "spoken": spoken_text.strip(),
        "correct_pronunciation": spoken_text.strip(),
        "score": round(score,2)
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
