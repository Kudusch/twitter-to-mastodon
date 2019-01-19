from mastodon import Mastodon
import tweepy
import requests
import json
import re

def getTootDict(tweet_json, debug=False):
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
            if debug == False:
                img_dict['data'] = requests.get(img_dict['url']).content
            else:
                img_dict['data'] = ">>data<<"

            try:
                img_dict['description'] = img['ext_alt_text']
            except:
                img_dict['description'] = None

            media_formated_text = ''.join(media_formated_text.split(img['url']))
            
            imgs.append(img_dict)
       
        toot_dict['media'] = imgs
        toot_dict['text'] = media_formated_text
    except:
        toot_dict['media'] = None
    return(toot_dict)

def uploadMediaMastodon(media, mastodon):
    id_list = []
    for m in media:
        media_dict = mastodon.media_post(m['data'], mime_type="image/jpeg", description=m['description'], focus=None)
        id_list.append(media_dict['id'])
    return(id_list)

def tootMastodon(text, mastodon, media=None):
    if media:
        media_ids = uploadMediaMastodon(media, mastodon)
        mastodon.status_post(text, media_ids=media_ids)
    else:
        mastodon.status_post(text)