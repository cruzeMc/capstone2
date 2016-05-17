import requests
import json

def sentiment(wordObject):
    if wordObject == '':
        return ''
    web_link = "http://text-processing.com/api/sentiment/"
    payload = {'text' : wordObject}
    if res
    
    if response.status_code == 200:
        return str(response.json()['label'])
    
    else:
        return "Error"