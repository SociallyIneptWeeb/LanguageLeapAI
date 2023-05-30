import speech_recognition as sr

import wave
from os import getenv
from pathlib import Path
from time import sleep

import deepl
import googletrans
import keyboard
import pyaudio
import requests
from dotenv import load_dotenv

from modules.asr import speech_to_text
from modules.tts import speak

load_dotenv()

USE_DEEPL = getenv('USE_DEEPL', 'False').lower() in ('true', '1', 't')
DEEPL_AUTH_KEY = getenv('DEEPL_AUTH_KEY')
TARGET_LANGUAGE = getenv('TARGET_LANGUAGE_CODE')

MIC_NAME = getenv('MICROPHONE_INPUT_NAME')
def get_mic_index(starting_name):
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if microphone_name.startswith(starting_name):
            print(f'MICROPHONE_INPUT found: {microphone_name} at index {i}')
            return i
    raise ValueError(f'MICROPHONE_INPUT not found starting with: {starting_name}')
MIC_ID = get_mic_index(MIC_NAME)

#just to check if it's found i have no clue what i'm doing
APP_OUTPUT_NAME = getenv('AUX_OUTPUT_NAME')
def get_mic_index(starting_name):
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if microphone_name.startswith(starting_name):
            print(f'AUX_OUTPUT found: {microphone_name} at index {i}')
            return i
    raise ValueError(f'AUX_OUTPUT not found starting with: {starting_name}')
APP_OUTPUT_ID = get_mic_index(APP_OUTPUT_NAME)



RECORD_KEY = getenv('MIC_RECORD_KEY')
LOGGING = getenv('LOGGING', 'False').lower() in ('true', '1', 't')
MIC_AUDIO_PATH = Path(__file__).resolve().parent / r'audio/mic.wav'
CHUNK = 1024
FORMAT = pyaudio.paInt16


def on_press_key(_):
    global frames, recording, stream
    if not recording:
        frames = []
        recording = True
        stream = p.open(format=FORMAT,
                        channels=MIC_CHANNELS,
                        rate=MIC_SAMPLING_RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=MIC_ID)


def on_release_key(_):
    global recording, stream
    recording = False
    stream.stop_stream()
    stream.close()
    stream = None

    # if empty audio file
    if not frames:
        print('No audio file to transcribe detected.')
        return

    # write microphone audio to file
    wf = wave.open(str(MIC_AUDIO_PATH), 'wb')
    wf.setnchannels(MIC_CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(MIC_SAMPLING_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # transcribe audio
    try:
        eng_speech = speech_to_text(MIC_AUDIO_PATH, 'transcribe', 'en')
    except requests.exceptions.JSONDecodeError:
        print('Too many requests to process at once')
        return

    if eng_speech:

        if USE_DEEPL:
            translated_speech = translator.translate_text(eng_speech, target_lang=TARGET_LANGUAGE)
        else:
            translated_speech = translator.translate(eng_speech, dest=TARGET_LANGUAGE).text

        if LOGGING:
            print(f'English: {eng_speech}')
            print(f'Translated: {translated_speech}')

        speak(translated_speech, TARGET_LANGUAGE)

    else:
        print('No speech detected.')


if __name__ == '__main__':
    p = pyaudio.PyAudio()

    # get channels and sampling rate of mic
    mic_info = p.get_device_info_by_index(MIC_ID)
    MIC_CHANNELS = mic_info['maxInputChannels']
    MIC_SAMPLING_RATE = int(mic_info['defaultSampleRate'])

    frames = []
    recording = False
    stream = None

    # Set DeepL or Google Translator
    if USE_DEEPL:
        translator = deepl.Translator(DEEPL_AUTH_KEY)
    else:
        translator = googletrans.Translator()

    keyboard.on_press_key(RECORD_KEY, on_press_key)
    keyboard.on_release_key(RECORD_KEY, on_release_key)

    try:
        while True:
            if recording and stream:
                data = stream.read(CHUNK)
                frames.append(data)
            else:
                sleep(0.5)

    except KeyboardInterrupt:
        print('Closing voice translator.')
