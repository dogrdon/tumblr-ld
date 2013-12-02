#!/usr/bin/env python

import pytumblr
import csv
import time
import datetime
import io
import os
import sys
import requests
import spotlight
import tumblrkeys

'''TODO: Parse out the annotations object to something more linkable,
         how to gather data from the dbpedia metadata,
         add image_permalinks (not sure why this was not working)
                                                                    '''

DBPEDIA_URL = 'http://spotlight.dbpedia.org/rest/annotate'
CONFIDENCE = 0.3
SUPPORT = 20

def create_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st
    
def whoami():
    get_me = client.info()
    i_am = get_me['user']['blogs'][0]['name']
    return i_am
  

#our keys

consumer = tumblrkeys._CONSUMER
secret = tumblrkeys._SECRET
token = tumblrkeys._TOKEN
token_s = tumblrkeys._TOKEN_S


#start a client with our keys
client = pytumblr.TumblrRestClient(consumer, secret, token, token_s)



#put all follows in a list
def get_followed_list():
    followers = []
    following = client.following()    
    key = 'blogs'
    results = following.get(key)
    
    for elem in results:
        followers.append(elem['name'])
    
    return followers


#pull all our followed peoples pertinent data into a csv
def stats_to_csv():
    post_glug = []
    #post_stats = []
    #post_stats.append(header)
    
    #open a csv file for writing
    timestamp = create_timestamp()
    username = whoami()  
    
    filename = username + "OUT_" + timestamp + ".csv"
    
    c = csv.writer(open(filename, "wb"))
    
    c.writerow(['name', 'tags', 'slug', 'caption', 'url', 'annotations'])
    
    followed = get_followed_list()
    
    for name in followed:
        post_glug.append(client.posts(name))
        
    for elem in post_glug:
        for elem2 in elem['posts']:
            if elem2['type'] == 'photo':
                if elem2['blog_name'] is not None:
                    name = elem2['blog_name']
                else:
                    name = ''
                    
                if elem2['slug'] is not None:
                    slug = elem2['slug']
                else:
                    slug = ''
                    
                if elem2['caption'] is not None:
                    caption = elem2['caption']
                else:
                    caption = ''
                    
                 
                if elem2['post_url'] is not None:
                    url = elem2['post_url']
                else:
                    url = ''
                    
                #if elem2['image_permalink']:
                #    img_link = elem2['image_permalink']
                #else:
                #    img_link = ''
                    
                if elem2['tags'] is not None:
                    tags = elem2['tags']
                else:
                    tags = ''
                
                
                if type(name) == list:
                    name = ",".join(namee)
                
                if type(url) == list:
                    url = ",".join(url)
                
                #img_link = ",".join(img_link) 
                tags = ",".join(tags) #turn the tags & img_links into a comma separated string (cause who cares, right?)          
                #stat = '['+ name + ',' + slug + ',' + caption + ',' + url + ']'
                
                #stat = stat.encode('utf-8')
                name = name.encode('utf-8')
                slug = slug.encode('utf-8')
                caption = caption.encode('utf-8')
                url = url.encode('utf-8')                
                #img_link = img_link.encode('utf-8')
                tags = tags.encode('utf-8')
                
                
                try:
                    annotations = annotate_posts(tags)
                except:
                    annotations = 'Error collecting annotations'
                #annotations = annotations.encode('utf-8')
                
            
                c.writerow([name, tags, slug, caption, url, annotations])
                #post_stats.append(stat)
    
    
    #return post_stats

#this function will grab details for each post and annotate it using dpedia spotlight
def annotate_posts(text):
    annotations = spotlight.annotate(DBPEDIA_URL, text, confidence = CONFIDENCE, support = SUPPORT)
    return annotations



