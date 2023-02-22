from os import getenv
from pathlib import Path
from threading import Thread
from urllib.parse import urlencode

import requests
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv('VOICEVOX_BASE_URL')
SPEAKERS_INPUT_ID = int(getenv('VOICEMEETER_INPUT_ID'))
APP_INPUT_ID = int(getenv('CABLE_INPUT_ID'))
VOICEVOX_WAV_PATH = Path(__file__).resolve().parent.parent / r'audio\voicevox.wav'


def play_voice(device_id):
    data, fs = sf.read(VOICEVOX_WAV_PATH, dtype='float32')
    sd.play(data, fs, device=device_id)
    sd.wait()


def speak_jp(sentence):
    # generate initial query
    speaker_id = '20'
    params_encoded = urlencode({'text': sentence, 'speaker': speaker_id})
    r = requests.post(f'{BASE_URL}/audio_query?{params_encoded}')
    voicevox_query = r.json()
    voicevox_query['speedScale'] = 1
    voicevox_query['volumeScale'] = 4.0
    voicevox_query['intonationScale'] = 1.5
    voicevox_query['prePhonemeLength'] = 1.0
    voicevox_query['postPhonemeLength'] = 1.0

    # synthesize voice as wav file
    params_encoded = urlencode({'speaker': speaker_id})
    r = requests.post(f'{BASE_URL}/synthesis?{params_encoded}', json=voicevox_query)

    with open(VOICEVOX_WAV_PATH, 'wb') as outfile:
        outfile.write(r.content)

    # play voice to app mic input and speakers/headphones
    threads = [Thread(target=play_voice, args=[APP_INPUT_ID]), Thread(target=play_voice, args=[SPEAKERS_INPUT_ID])]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == '__main__':
    # test if voicevox is up and running
    speak_jp('皆さん、ビデオに「いいね！」を残して、私のチャンネルを購読するのを忘れないでください。')
