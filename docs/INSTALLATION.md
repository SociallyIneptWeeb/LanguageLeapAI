# Installation of Services and Dependencies

## Prerequisites

So you want to try out **LanguageLeapAI** huh? 
Do note that running WhisperAI and Voicevox on your local machine is not recommended as a significant amount of RAM and GPU power is required for the program to run efficiently.
If possible, you should run these 2 on another server either on your local network or on the cloud.


## Installing Dependencies

### Cloning this repository

Run this command to clone this entire repository.

```git clone https://github.com/SociallyIneptWeeb/LanguageLeapAI```

Run the following command in the root folder to install the required python dependencies.

```pip install -r requirements.txt```


## Installing Services


### Docker

If you are using Google Colab notebooks to run Whisper AI and Voicevox, you can skip installing Docker Compose.

If you are planning on running the docker containers, you will have to ensure that you have Docker Compose installed.
You may follow these instructions [here](https://docs.docker.com/desktop/install/windows-install/) to install Docker Compose.

### Voicemeeter Banana

In order to proper route and separate audio between applications, your system audio, and python, we will be also be installing Voicemeeter Banana.
You can download and install Voicemeeter from their website [here](https://vb-audio.com/Voicemeeter/banana.htm).

### Virtual Audio Cable

As the number of virtual cables provided by Voicemeeter Banana is not enough, we will also be installing an extra one [here](https://vb-audio.com/Cable/).
Download and Install VB-CABLE Driver by extracting all files and Run Setup Program in administrator mode. Reboot after installation.

After completing this step, you may move on to the next: Setting up [audio routing](AUDIO.md) using Voicemeeter Banana.
