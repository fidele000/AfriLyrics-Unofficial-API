from flask import Flask,request


app=Flask(__name__)


def index():
    return { 'body':'<empty>'}


app.add_url_rule('/','index',index)