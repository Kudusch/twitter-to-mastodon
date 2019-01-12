#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mastodon import Mastodon
import tweepy
import requests
from pprint import pprint
import config as config
import re

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
        urls = tweet_json['entities']['urls']
        url_formated_text = toot_dict['text']
        for url in urls:
            url_formated_text = url['expanded_url'].join(url_formated_text.split(url['url']))
        toot_dict['text'] = url_formated_text
    except:
        pass

    toot_dict['text'] = re.sub(r"(@\w+)", r"\1@twitter.com", toot_dict['text'], 0, re.MULTILINE)

    try:
        toot_dict['is_retweet'] = tweet_json['retweeted_status']['id']
    except:
        toot_dict['is_retweet'] = False

    try:
        toot_dict['is_reply'] = tweet_json['in_reply_to_status_id']
        if toot_dict['is_reply'] == None:
            toot_dict['is_reply'] = False
    except:
        toot_dict['is_reply'] = False
    
    try:
        imgs = []
        media_formated_text = toot_dict['text']
        for img in tweet_json['extended_entities']['media']:
            img_dict = {}
            img_dict['url'] = img['media_url_https']
            img_dict['data'] = requests.get(img_dict['url']).content
            
            try:
                img_dict['description'] = img['description']
            except:
                img_dict['description'] = None

            media_formated_text = ''.join(media_formated_text.split(img['url']))
            
            imgs.append(img_dict)
       
        toot_dict['media'] = imgs
        toot_dict['text'] = media_formated_text
    except:
        toot_dict['media'] = None
    return(toot_dict)

def uploadMediaMastodon(media):
    id_list = []
    for m in media:
        media_dict = mastodon.media_post(m['data'], mime_type="image/jpeg", description=m['description'], focus=None)
        id_list.append(media_dict['id'])
    return(id_list)

def tootMastodon(text, media=None):
    if media:
        media_ids = uploadMediaMastodon(media)
        mastodon.status_post(text, media_ids=media_ids)
    else:
        mastodon.status_post(text)

class UserListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            toot_dict = getTootDict(status._json)
        except:
            print("Could not extraxt toot_dict")
        
        if toot_dict['is_retweet'] == False and toot_dict['user_id'] == '15872417' and toot_dict['is_reply'] == False:
            try:
                pprint(toot_dict)
                tootMastodon(toot_dict['text'], media=toot_dict['media'])
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
kuduschStream.filter(follow = ["15872417"])
