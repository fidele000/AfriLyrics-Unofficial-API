
  
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
