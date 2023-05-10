from os import getenv
from pathlib import Path

import requests
from dotenv import load_dotenv
import deepl
import googletrans

load_dotenv()

BASE_URL = getenv('WHISPER_BASE_URL')
MAIN_LANGUAGE = getenv('MAIN_LANGUAGE_CODE')
USE_DEEPL = getenv('USE_DEEPL', 'False').lower() in ('true', '1', 't')
DEEPL_AUTH_KEY = getenv('DEEPL_AUTH_KEY')
REQUEST_TIMEOUT = int(getenv('REQUEST_TIMEOUT'))
SAMPLE_JP_FILEPATH = Path(__file__).resolve().parent.parent / r'audio\samples\japanese_speech_sample.wav'
SAMPLE_EN_FILEPATH = Path(__file__).resolve().parent.parent / r'audio\samples\english_speech_sample.wav'


def speech_to_text(filepath, task, language):
    # Set DeepL or Google Translator
    if USE_DEEPL:
        translator = deepl.Translator(DEEPL_AUTH_KEY)
    else:
        translator = googletrans.Translator()

    try:
        if MAIN_LANGUAGE == "en" or task == "transcribe":
            # If the MAIN_LANGUAGE is english whisper is able to do the translating for us
            # If the task is 'transcribe' we don't need to translate it to the MAIN_LANGUAGE
            # There are only two use cases for transcribe:
            # One is the sample test
            # The other one is used in 'voice_translator.py' and it get's translated to the target language anyway
            with open(filepath, 'rb') as infile:
                files = {'audio_file': infile}
                r = requests.post(f'{BASE_URL}/asr?task={task}&language={language}&output=json',
                                  files=files,
                                  timeout=REQUEST_TIMEOUT)
                if r.status_code == 404:
                    print(
                        'Unable to reach Whisper, ensure that it is running, or the WHISPER_BASE_URL variable is set correctly')
                    return None
                else:
                    return r.json()['text'].strip()
        else:
            # If MAIN_LANGUAGE isn't english Whisper can't translate the text to the desired Language (Whisper always translates to english)
            if task == "translate":
                with open(filepath, 'rb') as infile:
                    files = {'audio_file': infile}
                    r = requests.post(f'{BASE_URL}/asr?task={"transcribe"}&language={language}&output=json',
                                      files=files,
                                      timeout=REQUEST_TIMEOUT)
                if r.status_code == 404:
                    print(
                        'Unable to reach Whisper, ensure that it is running, or the WHISPER_BASE_URL variable is set correctly')
                    return None
                else:
                    speech = r.json()['text'].strip()
                    if USE_DEEPL:
                        translated_speech = translator.translate_text(speech, target_lang=MAIN_LANGUAGE)
                    else:
                        translated_speech = translator.translate(speech, dest=MAIN_LANGUAGE).text
                    return translated_speech

    except requests.exceptions.Timeout:
        print('Request timeout')
        return None

    except Exception as e:
        print(f'An unknown error has occurred: {e}')
        return None


if __name__ == '__main__':
    # test if whisper is up and running
    print('Testing Whisper on English speech sample.')
    print(f'Actual audio: Oh. Honestly, I could not be bothered to play this game to full completion.'
          f'The narrator is obnoxious and unfunny, with his humor and dialogue proving to be more irritating than '
          f"entertaining.\nWhisper audio: {speech_to_text(SAMPLE_EN_FILEPATH, 'transcribe', 'en')}\n")

    print('Testing Whisper on Japanese speech sample.')
    print(f'Actual translation: How is this dress? It suits you very well.\n'
          f"Whisper translation: {speech_to_text(SAMPLE_JP_FILEPATH, 'translate', 'ja')}")
