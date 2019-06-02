from spinner import spin
import configparser
import threading
import time
import requests
import slack
import shutil
import sys
import recording

connected = False
# time of first connect
start = time.time()
# time in seconds before crapping out
timeout = 2

on_air = False


def spin_check():
    if connected:
        print('PLUGGED IN')
        return False
    elif time.time() - start > timeout:
        print('Bummer, could not connect')
        sys.exit(-1)
    return True


def is_on_air():
    return on_air


def on_record():
    global on_air
    on_air = True
    global filename
    filename = time.strftime("%m-%d-%Y_%H%M") + ".wav"
    t = threading.Thread(target=recording.record, args=(filename, is_on_air,))
    t.start()


def on_stop_record():
    global on_air
    on_air = False

    mp3_filename = recording.convert(filename)

    print('Uploading to Slack channel ', end='')
    t = threading.Thread(target=spin, args=(spin_check,))
    t.start()

    my_file = {
      'file': (mp3_filename, open(mp3_filename, 'rb'), 'wav')
    }

    payload = {
        "channels": [channel_id],
        'initial_comment': '...and there it is',
        "filename": mp3_filename,
        'title': 'Latest Jam',
        "token": token,
    }

    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    print('DELIVERED')


@slack.RTMClient.run_on(event='hello')
def on_connect(**payload):
    global connected
    connected = True
    web_client = payload['web_client']
    web_client.chat_postMessage(
        channel='GK6TLC48P',
        icon_emoji=':metal:',
        text='Jambot is ready for tasty licks'
    )


@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    data = payload['data']
    channel_id = data['channel']
    web_client = payload['web_client']
    if '!onstage' in data['text']:
        if on_air:
            web_client.chat_postMessage(
                channel=channel_id,
                icon_emoji=':metal:',
                text='Don\'t worry bro, the recording has already started'
            )
        else:
            web_client.chat_postMessage(
                channel=channel_id,
                icon_emoji=':metal:',
                text='Let\'s rock! I\'m recording as we speak.'
            )

            on_record()
    elif '!offstage' in data['text']:
        if on_air:
            web_client.chat_postMessage(
                channel=channel_id,
                icon_emoji=':metal:',
                text='Nicely done. I\'m preparing that hot mix for consumption!'
            )

            on_stop_record()
        else:
            web_client.chat_postMessage(
                channel=channel_id,
                icon_emoji=':metal:',
                text='Was I supposed to be recording? Whoops...'
            )
    elif '!disk' in data['text']:
        total, used, free = shutil.disk_usage(".")
        web_client.chat_postMessage(
            channel=channel_id,
            icon_emoji=':metal:',
            text='Let me check on that disk space. {:.2f} % used, {:.1f} gigs left.'.format(used / total, free / 1024 / 1024 / 1024)
        )
    elif '!cleanup' in data['text']:
        removed = recording.cleanup()
        web_client.chat_postMessage(
            channel=channel_id,
            icon_emoji=':metal:',
            text='Let me clean that up for you. {} file(s) removed.'.format(removed)
        )
    elif '!shutdown' in data['text']:
        web_client.chat_postMessage(
            channel=channel_id,
            icon_emoji=':metal:',
            text='Yeah, I should get some rest.'
        )
        sys.exit(0)


def init():
    config = configparser.ConfigParser()
    config.read('config.ini')
    global token
    token = config['slack']['token']
    global channel_id
    channel_id = config['slack']['channel']

    print('Plugging into the Slack channel ', end='')
    t = threading.Thread(target=spin, args=(spin_check,))
    t.start()
    rtm_client = slack.RTMClient(token=token)
    rtm_client.start()
