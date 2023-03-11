from os import getenv

from dotenv import load_dotenv

load_dotenv()

BASE_URL = getenv('WHISPER_BASE_URL')
REQUEST_TIMEOUT = int(getenv('REQUEST_TIMEOUT'))

APP_OUTPUT_ID = int(getenv('AUX_OUTPUT_ID'))
RECORD_TIMEOUT = int(getenv('RECORD_TIMEOUT'))
PHRASE_TIMEOUT = int(getenv('PHRASE_TIMEOUT'))
INPUT_LANGUAGE = getenv('TARGET_LANGUAGE_CODE')
LOGGING = getenv("LOGGING", 'False').lower() in (
    'true', '1', 't'
)  # TODO: Should be called DEBUG


OFFSET_X = int(getenv('OFFSET_X'))
OFFSET_Y = int(getenv('OFFSET_Y'))
SUBTITLE_FONT_SIZE = int(getenv('SUBTITLE_FONT_SIZE'))
SUBTITLE_COLOR = getenv('SUBTITLE_COLOR')
SUBTITLE_BG_COLOR = getenv('SUBTITLE_BG_COLOR')
SACRIFICIAL_COLOR = getenv('SACRIFICIAL_COLOR')


DEEPL_AUTH_KEY = getenv('DEEPL_AUTH_KEY')
TARGET_LANGUAGE = getenv('TARGET_LANGUAGE_CODE')
MIC_ID = int(getenv('MICROPHONE_ID'))
RECORD_KEY = getenv('MIC_RECORD_KEY')


USE_DEEPL = getenv('USE_DEEPL', 'False').lower() in ('true', '1', 't')
