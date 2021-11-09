from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
from app.utils.http import get_html,get_african_lyrics
from app.utils.config import AFRILYRICS_URL
from logging import log
app=Flask(__name__)


def index():
    html=get_html(AFRILYRICS_URL)
    soup=BeautifulSoup(html, 'html.parser')
    hot_row=[ i for i in soup.find(class_='item-info-overlay').findAll(class_='item') ]
    items=[]

    for item in hot_row:
        item_title=item.find(class_='item-title').findAll('a')[0]
        item_author=item.find(class_='item-author').findAll('a')[0]
        item_media=item.find(class_='item-media').findAll('a')[0]

        items.append({
            'title':item_title.getText(),
            'link':item_title['href'].split('https://afrikalyrics.com')[1],
            'image':item_media['data-bg'],
            'artist':{
                'name':item_author.getText(),
                'link':item_author['href'].split('https://afrikalyrics.com')[1]
            }
            
        })

    response={}
    response['result']=items
    return jsonify(response)


def artist(name):
    """ function to return artist info and songs lyrics """
    
    return jsonify({'message':'working on this - will be available soon','url':f'/artist/{name}',})


def get_song_lyrics(songlink):
    """ function to return song lyrics """
    suggestion,body=get_african_lyrics(AFRILYRICS_URL+songlink)
    if body:
        return jsonify({'body':body,'suggestions':suggestion})
    return jsonify({'message':'working on this - will be available soon','url':f'/artist/{songlink}',})

app.add_url_rule('/','index',index)
app.add_url_rule('/artist/<name>','artist',artist)
app.add_url_rule('/<songlink>','get-lyrics',get_song_lyrics)