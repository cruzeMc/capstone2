import requests
import json

def sentiment(wordObject):
    if wordObject == '':
        return 'neutral'
        
    # elif len(wordObject.replace()) > 80000:
    #     return 'Too long'
        
    else:
        web_link = "http://text-processing.com/api/sentiment/"
        payload = {'text' : wordObject}
        response = requests.post(web_link, payload)
    
        if response.status_code == 200:
            return [str(response.json()['label']),str(response.json()['probability']['pos'])]
        
        elif response.status_code == 503:
            return 'Limit exceeded'
    
        else:
            return "Error"
