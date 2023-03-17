from os import getenv
from pathlib import Path

import keyboard
import sounddevice as sd
import soundfile as sf

TTS_WAV_PATH = Path(__file__).resolve().parent.parent / r'audio\tts.wav'
INGAME_PUSH_TO_TALK_KEY = getenv('INGAME_PUSH_TO_TALK_KEY')


def play_voice(device_id):

    if INGAME_PUSH_TO_TALK_KEY:
        keyboard.press(INGAME_PUSH_TO_TALK_KEY)

    try:    
        data, fs = sf.read(TTS_WAV_PATH, dtype='float32')
        #in case someone don't use VoiceMeeter and want to skip    
        if device_id:
            sd.play(data, fs, device=device_id)
            sd.wait()
        else:
            print("your device id is not set")
    except sd.PortAudioError as e:
        print("Please check your device ID ,Error occurred while opening output stream: ", e)
    except Exception as e:
        print("Error occurred while playing sound: ", e)

    if INGAME_PUSH_TO_TALK_KEY:
        keyboard.release(INGAME_PUSH_TO_TALK_KEY)
