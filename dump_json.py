#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mastodon import Mastodon
from pprint import pprint
import sys
from utilities import *
import config as config
import tweepy


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

try:
    input_id = sys.argv[1]
except:
    input_id = None

try:
    if sys.argv[2] == 'toot':
        toot_flag = True
    else:
        toot_flag = False
except:
    toot_flag = False

if input_id:
    tweet = api.get_status(input_id, tweet_mode='extended', include_ext_alt_text='true')
    tweet = tweet._json
    toot_dict = getTootDict(tweet, debug = False)
    if toot_dict['is_retweet'] == False and toot_dict['user_id'] == '15872417' and toot_dict['is_reply'] == False:
        tootMastodon(toot_dict['text'], media=toot_dict['media'], mastodon = mastodon)
        try:
            pprint(toot_dict)
            if toot_flag == True:
                #tootMastodon(toot_dict['text'], media=toot_dict['media'])
                print("Tooted!")
        except:
            print("Something went wrong")
    else:
        print("Tweet not tootable!")
        pprint([toot_dict['is_retweet'], toot_dict['user_id'], toot_dict['is_reply']])
else:
    tweets = api.user_timeline(tweet_mode='extended', include_ext_alt_text='true')[0:5]
    for tweet in tweets:
        tweet = tweet._json
        toot_dict = getTootDict(tweet)
        if toot_dict['is_retweet'] == False and toot_dict['user_id'] == '15872417' and toot_dict['is_reply'] == False:
            try:
                pprint(toot_dict)
                print("Tooted")
            except:
                print("Something went wrong")
        else:
            print("Tweet not tootable!")
            pprint([toot_dict['is_retweet'], toot_dict['user_id'], toot_dict['is_reply']])
        print("\n")
