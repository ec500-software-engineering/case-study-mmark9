#!/bin/python3

import enum
import speech_recognition as sr
from mastodon import Mastodon

CLIENT_ID = u'4219af9d5aec9ef7efd87e475578d7f23bd3d72b8f0a33e010dd683d2b3e8c83'
CLIENT_SECRET = u'27ded5682ba079c4149b0f86b2f416cc139c657c95446687d9b0e63dc510122c'
ACCESS_TOKEN = u'857ae13377fe15d98c3c6a67e5600591d89756010f7865ff14ef545656923a76'
SERVER_BASER_URL = 'http://localhost:3000'


class Commands(enum.Enum):
    TOOT = 'toot'
    FOLLOW = 'follow'
    UNFOLLOW = 'unfollow'


def register_app():
    client_id, client_secret = Mastodon.create_app(
        'test-app',
        ['read',
         'write',
         'follow',
         'push'],
        api_base_url=SERVER_BASER_URL
    )
    print('client id = {} and client secret = {}'.format(
        client_id,
        client_secret
    ))


def post_toot(toot_msg, mastodon_client):
    print('Tooting "{}"'.format(toot_msg))
    res = mastodon_client.toot(toot_msg)
    print(res)


def follow_a_user(name, mastodon_client):
    user_dicts = mastodon_client.account_search(name)
    if len(user_dicts) > 0:
        print('Following user {}:{}..'.format(
            user_dicts[0]['username'],
            user_dicts[0]['url']
        ))
        res = mastodon_client.account_follow(user_dicts[0]['id'])
        print(res)
    else:
        print('Could not find user with name "{}"'.format(name))


def unfollow_a_user(name, mastodon_client):
    user_dicts = mastodon_client.account_search(name)
    if len(user_dicts) > 0:
        print('Unfollowing user {}:{}..'.format(
            user_dicts[0]['username'],
            user_dicts[0]['url']
        ))
        res = mastodon_client.account_unfollow(user_dicts[0]['id'])
        print(res)
    else:
        print('Could not find user with name "{}"'.format(name))


def process_speech(speech_str, mastodon_client):
    try:
        index = speech_str.index('toots')
        toot_msg = speech_str[index+6:]
        post_toot(toot_msg, mastodon_client)
        return
    except ValueError:
        pass
    try:
        index = speech_str.index('toot')
        toot_msg = speech_str[index+5:]
        post_toot(toot_msg, mastodon_client)
        return
    except ValueError:
        pass
    try:
        index = speech_str.index('unfollow')
        target_name = speech_str[index+9:]
        unfollow_a_user(target_name, mastodon_client)
        return
    except ValueError:
        pass
    try:
        index = speech_str.index('follow')
        target_name = speech_str[index+7:]
        follow_a_user(target_name, mastodon_client)
        return
    except ValueError:
        pass
    print('Error, command not recognized')


def main():
    r = sr.Recognizer()
    print('Initializing mastodon client....')
    mastodon_client = Mastodon(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=ACCESS_TOKEN,
        api_base_url=SERVER_BASER_URL
    )

    my_account = mastodon_client.account_verify_credentials()
    print('Preparing microphone....')
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print('Say a command..')
            audio = r.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )
            print('Sending audio sample to google recognition service...')
            try:
                speech = r.recognize_google(audio)
                print(speech)
                print('Processing speech')
                process_speech(speech, mastodon_client)
            except sr.UnknownValueError:
                pass


if __name__ == '__main__':
    main()
