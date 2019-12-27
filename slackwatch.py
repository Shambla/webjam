from spinner import spin
import datetime as dt
import configparser
import threading
import time
import requests
import slack
import shutil
import sys
import audio

# whether or not the application has connected to Slack
connected = False
# whether or not the application is actively recording
on_air = False


def post_message(web_client, message):
    """
    Posts the provided message to the default Slack channel

    :param web_client: the Slack web client
    :param message: the message to post
    :return: nothing
    """
    web_client.chat_postMessage(
        channel=channel_id,
        icon_emoji=':metal:',
        text=message
    )


def on_record():
    """
    Triggers the recording process. This will start the audio recording of a
    file in a separate thread.

    :return: nothing
    """
    global on_air
    on_air = True
    global filename
    filename = time.strftime("%m-%d-%Y_%H%M") + ".wav"
    t = threading.Thread(target=audio.record, args=(filename, lambda: on_air))
    t.start()


def on_stop_record():
    """
    Stops the recording process. This will end the ongoing audio recording,
    convert the recording to an MP3 file, and upload the file to Slack.

    :return: nothing
    """
    global on_air
    on_air = False
    uploaded = False

    # seems to be a race condition if we immediately convert, give it a sec
    time.sleep(3)

    mp3_filename = audio.convert(filename)

    print('Uploading to Slack channel ', end='')
    t = threading.Thread(target=spin, args=(lambda: uploaded, 'SERVED ON THE WEB',))
    t.start()

    my_file = {
      'file': (mp3_filename, open(mp3_filename, 'rb'), 'wav')
    }

    hour = dt.datetime.now().hour
    title = dt.datetime.today().strftime('%A')

    if hour > 4 and hour < 12:
        title += ' Morning '
    elif hour >= 12 and hour < 17:
        title += ' Afternoon '
    elif hour >= 17 and hour < 20:
        title += ' Evening '
    else:
        title += ' Night '
    title += 'Jam'

    payload = {
        "channels": [channel_id],
        'initial_comment': '...and here it is',
        "filename": mp3_filename,
        'title': title,
        "token": token,
    }

    requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
    uploaded = True


@slack.RTMClient.run_on(event='hello')
def on_connect(**payload):
    """
    Triggered upon connection to Slack. Sends a notification message.

    :param payload: the Slack payload
    :return: nothing
    """
    global connected
    connected = True
    post_message(payload['web_client'], 'Jambot is ready for tasty licks!')
    print('\a')


@slack.RTMClient.run_on(event='message')
def on_message(**payload):
    """
    Triggered upon Slack messages from users. Determines if the message was a
    recognized command and performs the requested operation.

    :param payload: the Slack payload
    :return: nothing
    """
    user = payload['data'].get('username')
    message = payload['data']['text'].lower()
    webclient = payload['web_client']

    # IFTTT sends message in separate field
    if user is not None and 'IFTTT' in user:
        print('in here!')
        message = payload['data']['attachments'][0]['pretext'].lower()

    # start the recording
    if 'onstage' in message:
        if on_air:
            post_message(webclient, "Don't worry bro, the recording has already started!")
        else:
            post_message(webclient, "Let's rock! I'm recording as we speak using the " + audio.active_device())
            print('\a')
            on_record()
    # stop the recording
    elif 'offstage' in message:
        if on_air:
            post_message(webclient, "Nicely done! I'm preparing that hot mix for consumption...")
            print('\a')
            on_stop_record()
        else:
            post_message(webclient, "Was I supposed to be recording? Cuz I have NOT been recording.")
    # sends disk usage statistics
    elif 'disk' in message:
        total, used, free = shutil.disk_usage(".")
        post_message(webclient, 'Let me check on that disk space. {:.2f} % used, {:.1f} gigs left.'.format(used / total, free / 1024 / 1024 / 1024))
    # sends device information
    elif 'devices' in message:
        post_message(webclient, 'Look at all these options:\n```' + audio.list_devices() + '```')
    # removes old audio files
    elif 'cleanup' in message:
        removed = audio.cleanup()
        post_message(webclient, "Let me clean that up for you. {} file(s) removed.".format(removed))
    # exits the application
    elif 'shutdown' in message:
        post_message(webclient, "Yeah, I should get some rest.")
        sys.exit(0)


def init():
    """
    Initializes the Slack connection.

    :return: nothing
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    global token
    token = config['slack']['token']
    global channel_id
    channel_id = config['slack']['channel']

    print('Plugging into the Slack channel ', end='')
    t = threading.Thread(target=spin, args=(lambda: not connected, 'PLUGGED IN',))
    t.start()
    rtm_client = slack.RTMClient(token=token)
    rtm_client.start()
