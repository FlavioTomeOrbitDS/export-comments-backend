from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from scripts import getExportUrl, getFile
import requests
import io
import urllib.parse
import json
from time import sleep


app = Flask(__name__)
CORS(app)


@app.route("/api/downloadfiles", methods=['POST', 'GET'])
def sendEndpoints():
    print("***************** Download File ***********************")

    # get the endponit from frontend

    json_data = request.get_json()
    print(json_data)
    endpoint = json_data['endpoint']

    print("Making request to: {}".format(endpoint))

    # make the request to API
    header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
              "accept": "application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
    try:
        r = requests.get(endpoint, headers=header)
    except:
        return jsonify('teste')

    # if the download failed, try again
    while r.status_code != 200:
        sleep(0.5)
        print("Making request to: {}".format(endpoint))
        r = requests.get(endpoint, headers=header)

    # return a response as xlsx file format
    buffer = io.BytesIO(r.content)
    # buffer.seek(0)
    return send_file(
        buffer,
        download_name="data.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@app.route("/api/generateEndpoints", methods=['POST', 'GET'])
def generateEndpoints():

    from time import sleep
    
    json_data = request.get_json()

    link = json_data['url']

    print("SEND: {}".format(link))

    # encode link
    encoded_link = urllib.parse.quote(link, safe='')

    # build the request to send to exportcomments api
    url = "https://exportcomments.com/api/v2/export?url={}".format(
        encoded_link)

    header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
              "accept": "application/json"}

    response = requests.put(url, headers=header)
    
    # format response to get the downloadUrl param
    json_data = response.json()
    # print(json_data)
    print(json_data)
    try:
        #print("REPONSE CODE: {}".format(json_data['code']))
        downloadUrl = json_data['data']['downloadUrl']
        url = "https://exportcomments.com"+downloadUrl
    except:        
        url = ''

    # build the full download url
    print("--GET: {}".format(url))

    #exportLink = Exportlink()
    #exportLink.link = linksArray

    Exportlink = {
        'link': url
    }

    return jsonify(Exportlink)


if __name__ == '__main__':
    app.run()
