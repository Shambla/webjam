import os
from spinner import spin
import sounddevice as sd
import soundfile as sf
import queue
import threading
from pydub import AudioSegment
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def record(filename, on_air_callback):
    """
    Records an audio file based on the default input device

    :param filename: the name of the audio file
    :param on_air_callback: callback that should return True until recording should stop
    :return: nothing
    """
    device_info = sd.query_devices(None, 'input')
    samplerate = int(device_info['default_samplerate'])
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    print('Recording the goodness ', end='')
    t = threading.Thread(target=spin, args=(on_air_callback, 'RECORDED'))
    t.start()

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=1, subtype=None) as file:
        with sd.InputStream(samplerate=samplerate, channels=1, device=None, callback=callback):
            while on_air_callback():
                file.write(q.get())


def convert(filename):
    """
    Converts the provided WAV file into an MP3

    :param filename: the name of the WAV file
    :return: the name of the MP3 file
    """
    converting = True

    print('Converting to MP3 ', end='')
    t = threading.Thread(target=spin, args=(lambda: converting, 'CONVERTED',))
    t.start()

    mp3_filename = filename.replace(".wav", ".mp3")
    AudioSegment.from_file(filename).export(mp3_filename, format="mp3", bitrate="128k")

    converting = False
    return mp3_filename


def cleanup():
    """
    Removes WAV/MP3 files in the current directory

    :return: the number of files removed
    """
    count = 0
    for file in os.listdir("."):
        if file.endswith(".wav") or file.endswith(".mp3"):
            print('Removing ' + file)
            os.remove(file)
            count += 1

    print('Removed {} file(s)'.format(count))

    return count
