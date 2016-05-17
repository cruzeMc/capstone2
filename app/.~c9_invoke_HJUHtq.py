import requests
import json

def sentiment(wordObject):
    if wordObject == '':
    payload = {'text'
    web_link = "http://text-processing.com/api/sentiment/"
    payload = {'text' : wordObject}
    response = requests.post(web_link, payload)
    
    if response.status_code == 200:
        return str(response.json()['label'])
    
    else:
        return "Error"