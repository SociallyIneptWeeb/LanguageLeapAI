from os import getenv
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv('WHISPER_BASE_URL')
REQUEST_TIMEOUT = int(getenv('REQUEST_TIMEOUT'))
SAMPLE_JP_FILEPATH = Path(__file__).resolve().parent.parent / r'audio\samples\japanese_speech_sample.wav'
SAMPLE_EN_FILEPATH = Path(__file__).resolve().parent.parent / r'audio\samples\english_speech_sample.wav'


def speech_to_text(filepath, task, language):
    try:
        with open(filepath, 'rb') as infile:
            files = {'audio_file': infile}
            r = requests.post(f'{BASE_URL}/asr?task={task}&language={language}&output=json',
                              files=files,
                              timeout=REQUEST_TIMEOUT)

        if r.status_code == 404:
            print('Unable to reach Whisper, ensure that it is running, or the WHISPER_BASE_URL variable is set correctly')
            return None

    except requests.exceptions.Timeout:
        print('Request timeout')
        return None

    except Exception as e:
        print(f'An unknown error has occurred: {e}')
        return None

    return r.json()['text'].strip()


if __name__ == '__main__':
    # test if whisper is up and running
    print('Testing Whisper on English speech sample.')
    print(f'Actual audio: Oh. Honestly, I could not be bothered to play this game to full completion.'
          f'The narrator is obnoxious and unfunny, with his humor and dialogue proving to be more irritating than '
          f"entertaining.\nWhisper audio: {speech_to_text(SAMPLE_EN_FILEPATH, 'transcribe', 'en')}\n")

    print('Testing Whisper on Japanese speech sample.')
    print(f'Actual translation: How is this dress? It suits you very well.\n'
          f"Whisper translation: {speech_to_text(SAMPLE_JP_FILEPATH, 'translate', 'ja')}")
