#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
from pprint import pprint
import sys
import json
import requests
from mastodon import Mastodon
import config as config

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

def getTootDict(tweet_json):
    toot_dict = {}
    toot_dict['id'] = tweet_json['id']
    toot_dict['user_id'] = str(tweet_json['user']['id'])
    try:
        toot_dict['text'] = tweet_json['full_text']
    except:
        toot_dict['text'] = tweet_json['text']

    try:
        toot_dict['is_retweet'] = tweet_json['retweeted_status']['id']
    except:
        toot_dict['is_retweet'] = False
    
    try:
        imgs = []
        for img in tweet_json['extended_entities']['media']:
            img_dict = {}
            img_dict['url'] = img['media_url_https']
            img_dict['data'] = requests.get(img_dict['url']).content
            try:
                img_dict['description'] = img['description']
            except:
                img_dict['description'] = None

            imgs.append(img_dict)
        toot_dict['media'] = imgs
    except:
        toot_dict['media'] = None
    return(toot_dict)

try:
    tweet = api.get_status(sys.argv[1], tweet_mode='extended', include_ext_alt_text='true')
    tweet = tweet._json
    pprint(tweet)
    pprint(getTootDict(tweet))
except:
    tweets = api.user_timeline()[0:5]
    for tweet in tweets:
        pprint(tweet._json)
        print("\n")
