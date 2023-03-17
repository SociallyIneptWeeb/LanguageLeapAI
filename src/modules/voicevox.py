from os import getenv
from pathlib import Path
from threading import Thread
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from modules.audio_to_device import play_voice
from modules.util import *
load_dotenv()

# Audio devices
SPEAKERS_INPUT_ID = castInt(getenv('VOICEMEETER_INPUT_ID'))
APP_INPUT_ID = castInt(getenv('CABLE_INPUT_ID'))

# Voicevox settings
BASE_URL = getenv('VOICEVOX_BASE_URL')
VOICE_ID = castInt(getenv('VOICE_ID'))
SPEED_SCALE = castFloat(getenv('SPEED_SCALE'))
VOLUME_SCALE = castFloat(getenv('VOLUME_SCALE'))
INTONATION_SCALE = castFloat(getenv('INTONATION_SCALE'))
PRE_PHONEME_LENGTH = castFloat(getenv('PRE_PHONEME_LENGTH'))
POST_PHONEME_LENGTH = castFloat(getenv('POST_PHONEME_LENGTH'))

TTS_WAV_PATH = Path(__file__).resolve().parent.parent / r'audio\tts.wav'


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

    with open(TTS_WAV_PATH, 'wb') as outfile:
        outfile.write(r.content)

    # play voice to app mic input and speakers/headphones
    threads = [Thread(target=play_voice, args=[APP_INPUT_ID]), Thread(target=play_voice, args=[SPEAKERS_INPUT_ID])]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == '__main__':
    # test if voicevox is up and running
    print('Voicevox attempting to speak now...')
    speak_jp('むかしあるところに、ジャックという男の子がいました。ジャックはお母さんと一緒に住んでいました。')
