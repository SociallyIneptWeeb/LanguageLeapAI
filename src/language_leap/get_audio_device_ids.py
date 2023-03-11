import speech_recognition as sr


if __name__ == '__main__':
    for mic_id, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        print(f'{mic_id}: {mic_name}')
