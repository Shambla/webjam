# Webjam - Distilling Jams to the Web

## What is this?

Artists have sketchbooks, writers have notebooks, but what do musicians have? Webjam of course!

Webjam is a shoddy amalgamation of Python files which aims to capture your musical ramblings in
a rough format, prioritizing ease-of-use over fidelity.

## How it works

1. Plug in to the device which will run this code
1. Send the ```!onstage``` command to the monitored slack channel. This starts the recording.
1. Send the ```!offstage``` command to the monitored slack channel when you're finished. This
converts the recording to an MP3 and uploads it to the slack channel.
1. Savor the fruits of your labor

## Warning

Do not trust my Python

## Dependencies

* Pyfiglet - pip install pyfiglet
* Slackclient - pip install slackclient
* Soundclient - pip install sounddevice
* Soundfile - pip install soundfile
* Numpy - pip install numpy
* Requests - pip install requests
* Pydub - pip install pydub
* ffmpeg - varies by OS

## Configuration

This application looks for a config.ini file in the current directory which should contain the
following information:

[slack]
token = {your slack authentication token}
channel = {the slack channel ID}
