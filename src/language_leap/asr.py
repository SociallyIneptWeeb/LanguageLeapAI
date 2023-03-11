from logging import getLogger
from os import getenv
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

from language_leap.environment import REQUEST_TIMEOUT

logger = getLogger(__name__)


SAMPLE_JP_FILEPATH = Path(__file__).resolve() / \
    'audio/samples/japanese_speech_sample.wav'
SAMPLE_EN_FILEPATH = Path(__file__).resolve() / \
    'audio/samples/english_speech_sample.wav'


def _request_text(file_path: Path, language: str = 'en') -> Optional[str]:
    """
    Request text from Whisper API.

    Parameters:
        file_path (Path): Path to audio file.
        language (str): Language of audio file.

    Returns:
        Optional[str]: Transcribed text or None if request timed out.
    """
    # TODO: This function can replace 'transcribe' and 'translate' functions.

    with file_path.open('rb') as infile:
        try:
            response = requests.post(
                f'{BASE_URL}/asr?task=translate&language={language}&output=json',
                files={
                    'audio_file': infile
                },
                timeout=REQUEST_TIMEOUT
            )
        except requests.exceptions.Timeout:
            logger.error('Request timeout')
            return None

    text = r.json().get('text', '').strip()

    if not ('text' in _text):
        logger.error(
            f'Response from /asr?task=translate&language={language}&output=json '
            'has given an empty string or could not be found.'
        )
        return ''

    logger.debug(f'Response from /asr?task=transcribe response: {_text}')
    return text


def transcribe(file_path: Path) -> str:
    return _request_text(file_path)


def translate(file_path, language) -> Optional[str]:
    text = _request_text(file_path, language)
    # remove most hallucinations
    if text.lower().startswith('thank you for'):
        return None

    return text


if __name__ == '__main__':
    # test if whisper is up and running
    logger.info('Testing Whisper on English speech sample.')
    logger.info(f'Actual audio: Oh. Honestly, I could not be bothered to play this game to full completion.'
                f'The narrator is obnoxious and unfunny, with his humor and dialogue proving to be more irritating than '
                f'entertaining.\nWhisper audio: {transcribe(SAMPLE_EN_FILEPATH)}\n')

    logger.info('Testing Whisper on Japanese speech sample.')
    logger.info(f'Actual translation: How is this dress? It suits you very well.\n'
                f"Whisper translation: {translate(SAMPLE_JP_FILEPATH, 'ja')}")
