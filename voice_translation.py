import sounddevice as sd
import ffmpeg
import requests
import json
import os
import openai
from openai import OpenAI
import keyboard
from pydub import AudioSegment
from pydub.playback import play

# Chain of Action
# Enter Output Language
# Hold enter to talk
# recording of input is transcribed to text --> whisper-1
# text is translated to specified language --> gpt-3.5 - turbo
# Specified language is read by whisper-1,, I dont know if thats possible
# Load environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize variables
client = OpenAI()
chat_history = []
output_file_path = "output.wav"

print("\n# Welcome to your AI-powered voice translator #\n")

output_language = input("Please enter desired output language: ")
# Function definitions

def start_recording():
    print("Recording started...")
    recording = sd.rec(samplerate=44100, channels=2, blocking=False)
    return recording


def stop_recording_and_process(recording):
    sd.stop()
    print("Recording stopped, processing audio...\n")
    write_file(recording, output_file_path)
    transcribe()

def write_file(recording, file_path):
    recording = (recording * 32767).astype('int16')
    wav_file = AudioSegment(recording.tobytes(), frame_rate=44100, sample_width=2, channels=2)
    wav_file.export(file_path, format="wav")

def transcribe(file_path):
    with open(file_path, "rb") as audio_file:
        raw_transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )
        transcript = raw_transcript.get('text', '')
    return transcript
    
def translate(transcript, output_language):
    prompt = f"Translate the following text to '{output_language}': {transcript}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Your job is to accurately translate the input text to the specfified output language. Your main priority is to maintain meaning, tone, and context with high accuracy. Do not add anythin outside of that."},
            {"role": "user", "content": prompt}
        ],
        # this could be too short but want to ensure low cost
        max_tokens=1500,
        n=1,
        stop=None,
        # temp param controls the randomness of the output. A lower temperature results in more predictable translations. 0.5 seems appropriate when trying to translate accurately
        temperature=0.5,
    )
    # parsing and setting the response output to translation
    translation = response.choices[0].message.content.strip()
    return translation

def streamed_audio(translation):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "model": "tts-1",  # Corrected to string
        "input": translation,
        "voice": "echo",   # Corrected to string
        "response_format": "mp3"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        play(audio)
    except Exception as e:
        print(f"An error occurred in audio streaming: {e}")


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
        
        # if enter pressed, and recording
            # while enter is held, continue
            # if enter is let go of
            #   call stop_recording_and_process
            #   use that audio file, call write file to save it, 
            # call transcribe to turn audio to text, 
            # call translate, passing in the transcription, 
            # then call streamed_audio


        elif keyboard.is_pressed('q'):
            print("\n You have ended your session \n")
            break