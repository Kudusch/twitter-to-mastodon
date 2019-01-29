#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config as config
from utilities import *
from mastodon import Mastodon
import tweepy
from pprint import pprint

mastodon = Mastodon(
    access_token = config.mastodon_tokens['access_token'],
    api_base_url = config.mastodon_tokens['api_base_url']
)

consumer_key = config.twitter_tokens['consumer_key']
consumer_secret = config.twitter_tokens['consumer_secret']
access_token = config.twitter_tokens['access_token']
access_secret = config.twitter_tokens['access_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

class UserListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            toot_dict = getTootDict(status._json)
            pprint(toot_dict)
        except:
            print("Could not extraxt toot_dict")
        
        if toot_dict['is_retweet'] == False and toot_dict['user_id'] == '15872417' and toot_dict['is_reply'] == False:
            try:
                tootMastodon(toot_dict['text'], media=toot_dict['media', mastodon])
                print("Tooted")
            except:
                print("Something went wrong")
        else:
            print("Tweet not tootable!")
            pprint([toot_dict['is_retweet'], toot_dict['user_id'], toot_dict['is_reply']])

    def on_error(self, status_code):
        if status_code == 420:
            return False

userStream = UserListener()
kuduschStream = tweepy.Stream(auth = api.auth, listener=userStream, tweet_mode='extended', include_ext_alt_text='true')

print("Ready to go!")
while True:
    try:
        kuduschStream.filter(follow = ["15872417"])
    except:
        print("Restarting")
        pass
    else:
        print("Restarting")
        break
