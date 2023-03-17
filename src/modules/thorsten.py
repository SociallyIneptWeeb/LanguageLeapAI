from os import getenv
from pathlib import Path
from threading import Thread

import requests
from dotenv import load_dotenv

from modules.audio_to_device import play_voice

load_dotenv()

# Audio devices
SPEAKERS_INPUT_ID = int(getenv('VOICEMEETER_INPUT_ID'))
APP_INPUT_ID = int(getenv('CABLE_INPUT_ID'))


# Voicevox settings
TTS_WAV_PATH = Path(__file__).resolve().parent.parent / r'audio\tts.wav'


def speak_de(sentence):
    # generate initial query
    params = {'text': sentence}
    r = requests.get('http://localhost:50021/api/tts', params=params)

    if r.status_code == 404:
        print('Unable to reach Thorsten, ensure that it is running.')
        return

    with open(TTS_WAV_PATH, 'wb') as outfile:
        outfile.write(r.content)

    # play voice to app mic input and speakers/headphones
    threads = [Thread(target=play_voice, args=[APP_INPUT_ID]), Thread(target=play_voice, args=[SPEAKERS_INPUT_ID])]
    [t.start() for t in threads]
    [t.join() for t in threads]


if __name__ == '__main__':
    # test if voicevox is up and running
    print('Thorsten attempting to speak now...')
    speak_de('Es war einmal ein Junge namens Jack. Jack lebte bei seiner Mutter.')
