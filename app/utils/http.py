
  
from urllib import request as urlrequest
from urllib.error import URLError, HTTPError
import requests
from bs4 import BeautifulSoup
import random
import re
from .config import HEADERS
from app.utils.config import AFRILYRICS_URL



def get_html(link):
    try:
        req = urlrequest.Request(
            link,
            data=None,
            headers=HEADERS,
        )
        data = urlrequest.urlopen(req).read()
        return data
    except Exception:
        data = requests.get(link, headers=HEADERS).text
        return data

def get_african_lyrics(link):
    html = get_html(AFRILYRICS_URL+link)
    soup = BeautifulSoup(html, 'html.parser')
    all_p = [ p.text for p in soup.find(id="tracks").find(class_="col-xs-12").findAll("p")]
    suggestions = [ s.find(class_="item-title").find('a').get_text()+" by "+str(s.find(class_="item-author").get_text()).replace("\n", "") for s in soup.findAll(
        class_='item r')]
    body = ""

    for p in all_p:
        body += p


    return (suggestions, body)


def get_countries():
    html=get_html(AFRILYRICS_URL+'countries-list')
    soup=BeautifulSoup(html,'html.parser')
    
    items =[ item for item in soup.find(class_='row').findAll(attrs={'data-id':'item-4'})]
    
    sidebar_items= [ item for item in soup.find(class_='item-list').findAll(attrs={'data-id':'item-4'})]
    print(sidebar_items)

    result=[]
    for item in items:
        title=item.find(class_='item-title').getText()
        media=item.find(class_='item-media').findAll('a')[0]
        result.append({
            'title':title,
            'image':media['data-bg'],
            'link':media['href'].split('https://afrikalyrics.com')[1]
        })

    top_lyrics=[]

    for item in sidebar_items:
        title=item.find(class_='item-title').findAll('a')[0]
        media=item.find(class_='item-media').findAll('a')[0]
        author=item.find(class_='item-author').findAll('a')[0]
        print(media)
        top_lyrics.append({
            'title':title['title'],
            'image':media['data-bg'],
            'artist_name':author.text,
            'artist_link':author['href'].split('https://afrikalyrics.com')[1],
            'link':title['href'].split('https://afrikalyrics.com')[1]
        })

    return top_lyrics,result
    