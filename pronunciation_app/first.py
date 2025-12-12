import tkinter as tk
from tkinter import scrolledtext
import vosk
import sounddevice as sd
import queue
import json
import pyttsx3
import threading


# -----------------------
# Setup Offline Speech-to-Text (Vosk)
# -----------------------
model = vosk.Model("model")  # Path to your downloaded Vosk offline model
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# -----------------------
# Text-to-Speech Engine
# -----------------------
engine = pyttsx3.init()

# -----------------------
# Function to process speech
# -----------------------
def process_speech():
    rec = vosk.KaldiRecognizer(model, 16000)
    recognized_text = ""

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        status_label.config(text="🎤 Listening... Speak freely!")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                recognized_text = result.get("text", "")
                break

    status_label.config(text="✅ Listening finished")
    display_text(recognized_text)

# -----------------------
# Function to display text and play audio
# -----------------------
def display_text(text):
    text_display.config(state=tk.NORMAL)
    text_display.delete(1.0, tk.END)
    
    # Display recognized words
    words = text.split()
    for word in words:
        text_display.insert(tk.END, word + " ")
    
    text_display.config(state=tk.DISABLED)
    
    # Speak all recognized words
    for word in words:
        engine.say(word)
    engine.runAndWait()
    

# -----------------------
# GUI Setup
# -----------------------
root = tk.Tk()
root.title("Offline Free Speech Pronunciation App")
root.geometry("650x400")

title_label = tk.Label(root, text="🗣 Speak Freely & Hear Correct Pronunciation", font=("Arial", 14))
title_label.pack(pady=10)

text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10, font=("Arial", 12))
text_display.pack(pady=10)
text_display.config(state=tk.DISABLED)

status_label = tk.Label(root, text="Click 'Start' to speak", font=("Arial", 12))
status_label.pack(pady=10)

def start_thread():
    threading.Thread(target=process_speech, daemon=True).start()

start_button = tk.Button(root, text="🎙 Start", font=("Arial", 12), command=start_thread)
start_button.pack(pady=10)

root.mainloop()
