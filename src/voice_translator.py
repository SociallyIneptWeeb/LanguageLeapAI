import wave
from os import getenv
from time import sleep

import deepl
import keyboard
import pyaudio
import requests
from dotenv import load_dotenv

from modules.asr import transcribe
from modules.tts import speak

load_dotenv()

DEEPL_AUTH_KEY = getenv('DEEPL_AUTH_KEY')
TARGET_LANGUAGE = getenv('TARGET_LANGUAGE_CODE')
MIC_ID = int(getenv('MICROPHONE_ID'))
RECORD_KEY = getenv('MIC_RECORD_KEY')
LOGGING = getenv("LOGGING", 'False').lower() in ('true', '1', 't')
MIC_AUDIO_PATH = r'audio/mic.wav'
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

    # write microphone audio to file
    wf = wave.open(MIC_AUDIO_PATH, 'wb')
    wf.setnchannels(MIC_CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(MIC_SAMPLING_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # transcribe audio
    try:
        eng_speech = transcribe(MIC_AUDIO_PATH)
    except requests.exceptions.JSONDecodeError:
        print('No audio file to transcribe detected.')
        return

    if eng_speech:
        jp_speech = translator.translate_text(eng_speech, target_lang=TARGET_LANGUAGE)
        if LOGGING:
            print(f'English: {eng_speech}')
            print(f'Japanese: {jp_speech}')
        speak(jp_speech, TARGET_LANGUAGE)
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
    translator = deepl.Translator(DEEPL_AUTH_KEY)
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
