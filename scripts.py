import requests
import json
from exportcomments import ExportComments


def getExportUrl(link):
    # Instantiate the client Using your API key
    ex = ExportComments(
        'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d')

    # get the reponse from API
    response = ex.exports.create(
        url='https://www.youtube.com/watch?v=U5NdL3RokJc&t=452s&ab_channel=IndieFolkCentral', replies='false', twitterType=None
    )
    

    # format response to get the URL
    str_response = str(response.body)
    str_response = str_response.replace("'", '"')
    str_response = str_response.replace("True", '"True"')
    str_response = str_response.replace("False", '"False"')
    str_response = str_response.replace("None", '"None"')
    json_resp = json.loads(str_response)

    fileName = json_resp['data']['rawUrl']

    return fileName


def getFile(fileName):
    
    import urllib.parse


    #url = "https://www.example.com/search?q=flask+request"
    

    #print(encoded_url)
    header = {'Accept': '*/*'}

    url = "https://exportcomments.com{}".format(fileName)
    
    encoded_url = urllib.parse.quote(url, safe='')
    print(url)
    
    r = requests.get(url, headers=header)

    print(r.content)

    return encoded_url
