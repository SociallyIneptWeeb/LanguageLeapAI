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

from modules.asr import transcribe
from modules.tts import speak
from modules.translator import Translator

load_dotenv()

TARGET_LANGUAGE = getenv('TARGET_LANGUAGE_CODE')
SOURCE_LANGUAGE = getenv('SOURCE_LANGUAGE_CODE')
MIC_ID = int(getenv('MICROPHONE_ID'))
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
        source_speech = transcribe(MIC_AUDIO_PATH)
    except requests.exceptions.JSONDecodeError:
        print('Too many requests to process at once')
        return

    if source_speech:

        translator.set_text(source_speech)
        translated_speech = translator.translate()
        
        if LOGGING:
            print(f'SOURCE: {source_speech}')
            print(f'TARGET: {translated_speech}')

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

    # Init Translator
    translator = Translator(source=SOURCE_LANGUAGE, target=TARGET_LANGUAGE)

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
