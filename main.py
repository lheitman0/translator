import sounddevice as sd
import ffmpeg
import requests
import json
import os
import numpy as np
import openai
from openai import OpenAI
from pynput import keyboard
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

# output_language = input("Please enter desired output language: ")
# Function definitions

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

# def write_file(recording, file_path):
#     if recording is None:
#         print("there is no audio file to process")
#         return 0
#     recording = (recording * 32767).astype('int16')
#     wav_file = AudioSegment(recording.tobytes(), frame_rate=44100, sample_width=2, channels=1)
#     wav_file.export(file_path, format="wav")
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

def transcribe(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            raw_transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="text"
            )
            # Directly use raw_transcript as it's already in text format
            return raw_transcript
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""

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
        "model": "tts-1",
        "input": translation,
        "voice": "echo",
        "response_format": "mp3"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        play(audio)
    except Exception as e:
        print(f"An error occurred in audio streaming: {e}")


def on_press(key):
    global recording, recording_data
    if key == keyboard.Key.enter and not recording:
        recording_data = start_recording()  # Start recording
        recording = True  # Set the flag to indicate recording is in progress

def on_release(key):
    global recording, recording_data
    if key == keyboard.Key.enter and recording:
        recording = False  # Reset the recording flag
        if recording_data is None:
            print("Recording failed. No data to process.")
        else:
            processed_data = stop_recording_and_process(recording_data)
            try:
                write_file(processed_data, output_file_path)
            except Exception as e:
                print(f"there was an error in write file on release: {e}")
            transcription = transcribe(output_file_path)
            translation = translate(transcription, output_language)
            try:
                streamed_audio(translation)
            except Exception as e:
                print(f"there was an error in write file on release: {e}")

    if key == keyboard.Key.esc:
        return False


# Main interaction loop
def main_loop():
    global recording, output_language
    recording = False
    print("\n# Welcome to your AI-powered voice translator #\n")
    output_language = input("Please enter desired output language: ")
    print("Press Enter to start and stop recording. Press 'Esc' to quit.")

    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    main_loop()