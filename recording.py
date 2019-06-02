import os
from spinner import spin
import sounddevice as sd
import soundfile as sf
import queue
import sys
import time
import threading
from pydub import AudioSegment
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def record(filename, on_air_callback):
    device_info = sd.query_devices(None, 'input')
    samplerate = int(device_info['default_samplerate'])
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    print('Recording the goodness ', end='')
    t = threading.Thread(target=spin, args=(on_air_callback,))
    t.start()

    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=1, subtype=None) as file:
        with sd.InputStream(samplerate=samplerate, channels=1, device=None, callback=callback):
            while on_air_callback():
                file.write(q.get())

    print('WE GOING PLATINUM')


def convert(filename):
    converting = True

    def mp3_callback():
        return converting

    print('Converting to MP3 ', end='')
    time.sleep(5)
    t = threading.Thread(target=spin, args=(mp3_callback,))
    t.start()

    mp3_filename = filename.replace(".wav", ".mp3")
    AudioSegment.from_file(filename).export(mp3_filename, format="mp3", bitrate="128k")

    converting = False
    return mp3_filename


def cleanup():
    count = 0
    for file in os.listdir("."):
        if file.endswith(".wav") or file.endswith(".mp3"):
            print('Removing ' + file)
            os.remove(file)
            count += 1

    print('Removed {} file(s)'.format(count))

    return count
