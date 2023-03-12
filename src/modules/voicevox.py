from os import getenv
from pathlib import Path
from threading import Thread
from urllib.parse import urlencode

import requests
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
import keyboard

load_dotenv()

# Audio devices
SPEAKERS_INPUT_ID = int(getenv('VOICEMEETER_INPUT_ID'))
APP_INPUT_ID = int(getenv('CABLE_INPUT_ID'))

# Keyboard
INGAME_PUSH_TO_TALK_KEY = getenv('INGAME_PUSH_TO_TALK_KEY')

# Voicevox settings
BASE_URL = getenv('VOICEVOX_BASE_URL')
VOICE_ID = int(getenv('VOICE_ID'))
SPEED_SCALE = float(getenv('SPEED_SCALE'))
VOLUME_SCALE = float(getenv('VOLUME_SCALE'))
INTONATION_SCALE = float(getenv('INTONATION_SCALE'))
PRE_PHONEME_LENGTH = float(getenv('PRE_PHONEME_LENGTH'))
POST_PHONEME_LENGTH = float(getenv('POST_PHONEME_LENGTH'))
VOICEVOX_WAV_PATH = Path(__file__).resolve().parent.parent / r'audio\voicevox.wav'


def play_voice(device_id):
    data, fs = sf.read(VOICEVOX_WAV_PATH, dtype='float32')

    if INGAME_PUSH_TO_TALK_KEY:
        keyboard.press(INGAME_PUSH_TO_TALK_KEY)

    sd.play(data, fs, device=device_id)
    sd.wait()

    if INGAME_PUSH_TO_TALK_KEY:
        keyboard.release(INGAME_PUSH_TO_TALK_KEY)


def speak_jp(sentence):
    # generate initial query
    params_encoded = urlencode({'text': sentence, 'speaker': VOICE_ID})
    r = requests.post(f'{BASE_URL}/audio_query?{params_encoded}')

    if r.status_code == 404:
        print('Unable to reach Voicevox, ensure that it is running, or the VOICEVOX_BASE_URL variable is set correctly')
        return

    voicevox_query = r.json()
    voicevox_query['speedScale'] = SPEED_SCALE
    voicevox_query['volumeScale'] = VOLUME_SCALE
    voicevox_query['intonationScale'] = INTONATION_SCALE
    voicevox_query['prePhonemeLength'] = PRE_PHONEME_LENGTH
    voicevox_query['postPhonemeLength'] = POST_PHONEME_LENGTH

    # synthesize voice as wav file
    params_encoded = urlencode({'speaker': VOICE_ID})
    r = requests.post(f'{BASE_URL}/synthesis?{params_encoded}', json=voicevox_query)

    with open(VOICEVOX_WAV_PATH, 'wb') as outfile:
        outfile.write(r.content)

    # play voice to app mic input and speakers/headphones
    threads = [Thread(target=play_voice, args=[APP_INPUT_ID]), Thread(target=play_voice, args=[SPEAKERS_INPUT_ID])]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == '__main__':
    # test if voicevox is up and running
    print('Voicevox attempting to speak now...')
    speak_jp('むかしあるところに、ジャックという男の子がいました。ジャックはお母さんと一緒に住んでいました。')
