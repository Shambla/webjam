from spinner import spin
import sounddevice as sd
import soundfile as sf
import queue
import sys
import threading
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
