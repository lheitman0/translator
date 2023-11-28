import sounddevice as sd
import ffmpeg
import requests
import json
import os
import openai
import keyboard
from pydub import AudioSegment
from pydub.playback import play

# Chain of Action
# Enter Output Language
# Hold enter to talk
# recording of input is transcribed to text --> whisper-1
# text is translated to specified language
# 
# Load environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize variables
chat_history = []
output_file_path = "output.wav"

print("\n# Welcome to your AI-powered voice translator #\n")

# Function definitions

def start_recording():
    global recording
    recording = sd.rec(int(44100 * 5), samplerate=44100, channels=2)
    sd.wait()
    print("Recording... Press Enter to stop")

def stop_recording_and_process():
    sd.stop()
    print("Recording stopped, processing audio...")
    write_file(recording, output_file_path)
    transcribe_and_chat()

def write_file(recording, file_path):
    recording = (recording * 32767).astype('int16')
    wav_file = AudioSegment(recording.tobytes(), frame_rate=44100, sample_width=2, channels=2)
    wav_file.export(file_path, format="wav")

def streamed_audio(input_text, model="tts-1", voice="echo"):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {secret_key}"
    }
    data = {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": "mp3"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    play(audio)

def transcribe_and_chat():
    # Implement transcription and chat logic here
    # Use the OpenAI API for transcription and chat
    pass

# Main interaction loop
def main_loop():
    print("Hold Enter while speaking, let go to stop. Press 'q' to quit.")
    recording = False

    while True:
        if keyboard.is_pressed('Enter') and not recording:
            start_recording()
            recording = True
            while keyboard.is_pressed('Enter'):
                pass  # Wait for key release

        elif keyboard.is_pressed('Enter') and recording:
            stop_recording_and_process()
            recording = False
            while keyboard.is_pressed('Enter'):
                pass  # Wait for key release

        elif keyboard.is_pressed('q'):
            print("\n You have ended your session \n")
            break