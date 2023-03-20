from datetime import datetime, timedelta
from io import BytesIO
from os import getenv
from pathlib import Path
from queue import Queue
from threading import Thread
from time import sleep

import requests
import speech_recognition as sr

from .asr import speech_to_text

APP_OUTPUT_ID = int(getenv('AUX_OUTPUT_ID'))
RECORD_TIMEOUT = int(getenv('RECORD_TIMEOUT'))
PHRASE_TIMEOUT = int(getenv('PHRASE_TIMEOUT'))
INPUT_LANGUAGE = getenv('TARGET_LANGUAGE_CODE')
LOGGING = getenv("LOGGING", 'False').lower() in ('true', '1', 't')
APP_AUDIO_WAV_PATH = Path(__file__).resolve().parent.parent / r'audio\app_audio.wav'


def request_thread(queue, phrase_time, now):
    try:
        translation = speech_to_text(APP_AUDIO_WAV_PATH, 'translate', INPUT_LANGUAGE)
    except requests.exceptions.JSONDecodeError:
        # Whisper is not thread-safe, see https://github.com/openai/whisper/discussions/296
        # However, if we do not want a single request to block future audio, just catch the error
        print('Too many requests to process at once')
        return

    if translation:
        queue.put(translation)
        # logging if needed
        if LOGGING:
            delay = (datetime.utcnow() - now).total_seconds()
            if phrase_time:
                print(f'Previous time: {phrase_time.time().strftime("%H:%M:%S")}, Now: {now.time().strftime("%H:%M:%S")}, Delay: {delay}, Translation: {translation}')
            else:
                print(f'Now: {now.time()}, Delay: {delay}, Translation: {translation}')


def translate_audio(translation_queue):
    data_queue = Queue()

    # We use SpeechRecognizer to record our audio because it can detect when speech ends.
    recorder = sr.Recognizer()
    # dynamic energy compensation lowers the energy threshold to a point where SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    # listen to app audio output (voice-chat)
    audio_output = sr.Microphone(device_index=APP_OUTPUT_ID)

    def record_callback(_, audio):
        # Threaded callback function to push audio data to queue when recordings finish.
        raw_data = audio.get_raw_data()
        data_queue.put(raw_data)

    # Create a background thread that will pass us raw audio bytes.
    recorder.listen_in_background(audio_output, record_callback, phrase_time_limit=RECORD_TIMEOUT)

    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()

    while True:
        now = datetime.utcnow()

        if not data_queue.empty():
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            prev_phrase_time = phrase_time
            if phrase_time and now - phrase_time > timedelta(seconds=PHRASE_TIMEOUT):
                last_sample = bytes()
            # This is the last time we received new audio data from the queue.
            phrase_time = now

            # Concatenate our current audio data with the latest audio data.
            while not data_queue.empty():
                data = data_queue.get()
                last_sample += data

            # Write audio data to the wav file as bytes.
            audio_data = sr.AudioData(last_sample, audio_output.SAMPLE_RATE, audio_output.SAMPLE_WIDTH)
            wav_data = BytesIO(audio_data.get_wav_data())
            with open(APP_AUDIO_WAV_PATH, 'w+b') as f:
                f.write(wav_data.read())

            # translate japanese audio to english and push to translation queue in thread
            # TODO: Add a Mutex to ensure request is not to Whisper simultaneously??
            Thread(target=request_thread, args=[translation_queue, prev_phrase_time, now], daemon=True).start()

        else:
            # Infinite loops are bad for processors, must sleep.
            sleep(0.5)
