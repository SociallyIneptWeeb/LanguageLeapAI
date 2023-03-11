# Audio Routing

Follow the steps below to:
1. Configure your system to use Voicemeeter Banana as its main I/O audio device
2. Direct your system audio and application audio to your speakers/headphones
3. Isolate an application's audio from the rest of your system for Whisper to conduct ASR on

## System settings
Change your default playback device. Go to Control Panel -> Hardware and Sound and under Sound, go to Change system sounds.

![](screenshots/control_panel.png?raw=true)

Set VoiceMeeter Input as your default playback device.

![](screenshots/default_playback.png?raw=true)

After doing this, you may not hear any audio from your system. This is intended, and we will be directing the system audio into your speakers/headphones in the next step.

## Voicemeeter Banana settings

Run Voicemeeter Banana. At the top right area where it says hardware out, click A1 and select your speakers/headphones. Wherever you want the desktop sounds to go, so you can hear them. 
There is WDM, MME and KS. Generally speaking choose WDM because this has a lower latency than MME.

![](screenshots/a1_hardware_out.png?raw=true)


To the left of Hardware Out section, there is the Virtual input section which shows Voicemeeter Banana's in-built virtual cables, VAIO and AUX.
Select A1 for the VAIO virtual cable. This VAIO cable represents VoiceMeeter Input/Output. 
By selecting VoiceMeeter Input as your default playback device earlier, any desktop audio will be played into this cable.
By selecting A1, you are sending your desktop audio via this cable into hardware out A1 (speakers/headphones). You should be able to hear your desktop audio now.

![](screenshots/virtual_input_sect.png?raw=true)

We will be using the AUX cable for any application audio output that we want Whisper to translate. Select A1 so that we can hear the application audio as well in our speakers/headphones.
Select B2 so that the application audio will be passed into VoiceMeeter Aux Output which will be recorded by [subtitler.py](../src/subtitler.py) and passed to Whisper.


## Application settings

For the application whose audio you want to translate, e.g. Apex, Valorant, Discord, Google Chrome, set the audio output device to VoiceMeeter Aux Input (VB-Audio VoiceMeeter AUX VAIO).
This sends the application's audio into the AUX cable.
Also set the application's audio input device to CABLE Output (VB-Audio Virtual Cable). This cable is where the TTS audio will be played into.

![](screenshots/app_io_devices.png?raw=true)

For applications like Google Chrome, you may also configure their application's audio I/O device via your computer's Volume mixer settings.

![](screenshots/chrome_audio_devices.png?raw=true)

For full-screen applications like Apex Legends, set the Display Mode to Borderless Window so that subtitles can be displayed over it.

![](screenshots/borderless_window.png?raw=true)


### Other useful application settings

You may also turn down the dialogue volume and other settings which may interfere with what Whisper attempts to translate.
You can adjust this to the point where WhisperAI's accuracy is not affected by other audio sources and your user experience is not affected as well.

![](screenshots/app_volume_levels.png?raw=true)

After setting up the audio routing, we can finally move on to the last step of the setup: [Writing your Environment file](ENV.md).
