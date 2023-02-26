# Writing your .env file

First, copy [.env.sample](../.env.sample) to .env by running the following command.

```cp .env.sample .env```

Now open .env in a text editor of your choice and update the variables. Below is a more detailed description of each environment variable

## Logging 

This variable can be set to either _True_ or _False_. Set to _True_ if you would like to see more detailed logging from the terminal when running the python scripts.
Set to _False_ if you want to disable logging.

## Services Urls 

These are the base urls for the Whisper and Voicevox services. You can leave it as localhost if you are running these on your local machine.
If you are running them using Google Colab or on a different port number, be sure to update these variables with the appropriate urls and ports.

## DeepL Authentication Key

The DEEPL_AUTH_KEY variable where you paste your DeepL authentication key. Sign up for a free plan [here](https://www.deepl.com/pro-api?cta=header-pro-api).
Then go to this [link](https://www.deepl.com/account/summary), scroll down to the `Authentication Key for DeepL API` section to copy your API key.

The TARGET_LANGUAGE_CODE variable is where you paste the language code of your desired language to translate. 
Use [this website](https://www.andiamo.co.uk/resources/iso-language-codes) to select the correct language code according to ISO 639-1 


## Push to talk key

The key to hold down when you want your voice to be recorded and translated. E.g. MIC_RECORD_KEY=t if you want to hold down the 't' key.

## Audio Device Ids

Here is where you will enter the IDs for the various audio devices that the program will be using.
This is required for python to know which audio device to listen from or play audio to.
Run [get_audio_device_ids.py](../src/modules/get_audio_device_ids.py) in order to obtain the id for your audio devices.
The output from running this command may be truncated but do your best to select the correct id for the audio device.

## Voicevox Settings

Choose which speaker to use from Voicevox by updating VOICE_ID. 
Send a curl request to get a list of all speaker IDs and their corresponding speakers.
Replace <VOICEVOX_BASE_URL> with the url that Voicevox is hosted at.

```curl <VOICEVOX_BASE_URL>/speakers```

Feel free to adjust the scaling of the speaker's volume, speed or intonation as well.

## Subtitle Settings

RECORD_TIMEOUT is the max number of seconds for [Audio Subtitler](../src/subtitler.py) to listen for before passing the audio to Whisper.

PHRASE_TIMEOUT is the max number of seconds between subtitles before starting a new one.

REQUEST_TIMEOUT is the max number of seconds to wait for a translation response from Whisper before dropping the request.
This is useful if you do not want old subtitles that took too long to process to overwrite current ones.

OFFSET_X and OFFSET_Y is the number of pixels from the bottom middle of the screen for subtitles to be displayed.

SUBTITLE_FONT_SIZE and SUBTITLE_COLOR is self explanatory.

SUBTITLE_BG_COLOR is the background color of your subtitles

SACRIFICIAL_COLOR is the color that will be considered transparent. This is for the subtitles to appear without python's tkinter window showing up and blocking the screen.

SACRIFICIAL_COLOR can be set to the same color as SUBTITLE_BG_COLOR so that subtitles will not have a background color.
SUBTITLE_COLOR shouldn't be set to the same color as SACRIFICIAL_COLOR as this will cause your subtitles to be invisible.


## Finish

You are finally done setting up your environment variables. To start running **LanguageLeapAI**, go to [usage](../README.md#Usage).
