import speech_recognition as sr

from os import getenv
from pathlib import Path
from threading import Thread
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from modules.audio_to_device import play_voice

load_dotenv()




# Audio devices
MIC_NAME = getenv('VOICEMEETER_INPUT_NAME')
def get_mic_index(starting_name):
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if microphone_name.startswith(starting_name):
            print(f'VOICEMEETER_INPUT found: {microphone_name} at index {i}')
            return i
    raise ValueError(f'VOICEMEETER_INPUT not found starting with: {starting_name}')
SPEAKERS_INPUT_ID = get_mic_index(MIC_NAME)

MIC_NAME = getenv('CABLE_INPUT_NAME')
def get_mic_index(starting_name):
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        if microphone_name.startswith(starting_name):
            print(f'CABLE_INPUT found: {microphone_name} at index {i}')
            return i
    raise ValueError(f'CABLE_INPUT not found starting with: {starting_name}')
APP_INPUT_ID = get_mic_index(MIC_NAME)



# Voicevox settings
BASE_URL = getenv('VOICEVOX_BASE_URL')
VOICE_ID = int(getenv('VOICE_ID'))
SPEED_SCALE = float(getenv('SPEED_SCALE'))
VOLUME_SCALE = float(getenv('VOLUME_SCALE'))
INTONATION_SCALE = float(getenv('INTONATION_SCALE'))
PRE_PHONEME_LENGTH = float(getenv('PRE_PHONEME_LENGTH'))
POST_PHONEME_LENGTH = float(getenv('POST_PHONEME_LENGTH'))

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
