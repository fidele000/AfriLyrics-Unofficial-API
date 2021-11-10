from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
from app.utils.http import get_html,get_african_lyrics,get_countries
from app.utils.config import AFRILYRICS_URL
from logging import log
from flask_cors import CORS, cross_origin


app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@cross_origin()
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
            'link':item_title['href'].replace('https://afrikalyrics.com',''),
            'image':item_media['data-bg'],
            'artist':{
                'name':item_author.getText(),
                'link':item_author['href'].replace('https://afrikalyrics.com','')
            }
            
        })

    response={}
    response['results']=items
    return jsonify(response)


@cross_origin()
def artist(name):
    """ function to return artist info and songs lyrics """
    
    return jsonify({'message':'working on this - will be available soon','url':f'/artist/{name}',})


@cross_origin()
def get_country_list():
    """ get country list """
    top_lyrics,result=get_countries()
    
    return jsonify({'result':result,'top_lyrics':top_lyrics})


@cross_origin()
def get_song_lyrics(songlink):
    """ function to return song lyrics """
    info,body=get_african_lyrics(songlink)

    results=[]

    results.append(
        {
            'info':info,
            'lyrics':body
        }
    )

    if body:
        return jsonify({'results':results})
    return jsonify({'message':'working on this - will be available soon','url':f'/artist/{songlink}',})





app.add_url_rule('/','index',index)
app.add_url_rule('/artist/<name>','artist',artist)
app.add_url_rule('/countries-list','country-list',get_country_list)
app.add_url_rule('/<songlink>','get-lyrics',get_song_lyrics)
