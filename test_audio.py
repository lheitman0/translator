import sounddevice as sd
import ffmpeg
import io
import requests
import json
import os
import numpy as np
from openai import OpenAI
from pynput import keyboard
from pydub import AudioSegment
from pydub.playback import play

# Chain of Action
# Enter Output Language
# Hold enter to talk
# recording of
# input is transcribed to text --> whisper-1
# text is translated to specified language --> gpt-3.5 - turbo
# Specified language is read by whisper-1,, I dont know if thats possible
# Load environment variables
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

# Initialize variables
client = OpenAI()
chat_history = []
output_file_path = "output.wav"

def start_recording(duration=5):
    try:
        print("Recording for {} seconds...".format(duration))
        recording = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
        sd.wait()
        return recording
    except Exception as e:
        print(f"An error occurred during recording: {e} ")
        return None

def stop_recording_and_process(recording):
    try:
        sd.stop()
        print("Recording stopped, processing audio...\n")
        write_file(recording, output_file_path)
        transcription = transcribe(output_file_path)
        return transcription
    except Exception as e:
        print(f"An error occurred during recording: {e} ")
        return None
    
def write_file(recording, file_path):
    if recording is None or not isinstance(recording, np.ndarray):
        print("Invalid or no audio data to process")
        return 0

    try:
        recording = (recording * 32767).astype('int16')
        wav_file = AudioSegment(recording.tobytes(), frame_rate=44100, sample_width=2, channels=1)  # Adjust channels if needed
        wav_file.export(file_path, format="wav")
        return 1
    except Exception as e:
        print(f"An error occurred while writing the audio file: {e}")
        return 0