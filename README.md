# Webjam - Distilling Jams to the Web

## What is this?

Artists have sketchbooks, writers have notebooks, but what do musicians have? ~~Jambooks~~ Webjam of course!

Webjam - is a shoddy amalgamation of Python files which aims to capture your musical ramblings in
a rough format, prioritizing ease-of-use over fidelity.

## How it works

1. Plug in to the device which will run this code
1. Launch the app ```python webjam.py``` which will then connect to Slack
1. Send the ```!onstage``` command to the monitored Slack channel. This starts the recording.
1. Send the ```!offstage``` command to the monitored Slack channel when you're finished. This
converts the recording to an MP3 and uploads it to the Slack channel.
1. Savor the fruits of your labor

## Warning

Do not trust my Python

## Dependencies

* [Pyfiglet](https://github.com/pwaller/pyfiglet) (Fancy ASCII intro) - pip install pyfiglet
* [Slackclient](https://github.com/slackapi/python-slackclient) (Slack integration) - pip install slackclient
* [Sounddevice](https://github.com/spatialaudio/python-sounddevice) (Sound recording) - pip install sounddevice
* [Soundfile](https://github.com/bastibe/SoundFile) (Sound recording) - pip install soundfile
* [Numpy](https://github.com/numpy/numpy) (Sound recording) - pip install numpy
* [Requests](https://github.com/kennethreitz/requests) (Slack integration) - pip install requests
* [Pydub](https://github.com/jiaaro/pydub) (MP3 Conversion) - pip install pydub
* [ffmpeg](https://ffmpeg.org/) (MP3 Conversion) - varies by OS

## Configuration

This application looks for a config.ini file in the current directory which should contain the
following information:

```
[slack]
token = {your slack authentication token}
channel = {the slack channel ID}
```
