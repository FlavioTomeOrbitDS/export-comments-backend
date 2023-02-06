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


class Exportlink:
    link = ' '


def json_response(obj):
    return json.dumps(obj.__dict__)


@app.route("/api/getDownloadLinks", methods=['POST', 'GET'])
def receive_data():
    from time import sleep
    json_data = request.get_json()
    linksArray = []
    # Do something with the JSON data
    for link in json_data['url_list']:
        print("Enviando Link para a API: {}".format(link))

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

        try:
            downloadUrl = json_data['data']['downloadUrl']
            url = "https://exportcomments.com"+downloadUrl
        except:
            url = ' '

        # build the full download url

        linksArray.append(url)
        print("--Link de download gerado: {}".format(url))

    exportLink = Exportlink()
    exportLink.link = linksArray

    # Exportlink = {
    #     'link': linksArray
    # }
    # send the full DowloadLink to FrontEnd
    # return jsonify(exportLink)
    return json_response(exportLink)


@app.route("/api/downloadFile", methods=['POST', 'GET'])
def downloadFile():
    from time import sleep
    import pandas as pd
    print("*** Download File *******")

    json_data = request.get_json()
    #downloadLink = json_data['downloadLink'][1]
    df_result = pd.DataFrame()
    for downloadLink in json_data['downloadLink']:
        if downloadLink != '':
            print(downloadLink)
            #downloadLink = request.args.get('link')

            print("Making request to: {}".format(downloadLink))

            header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
                      "accept": "application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
            r = requests.get(downloadLink, headers=header)

            while r.status_code != 200:
                sleep(0.5)
                print("Making request to: {}".format(downloadLink))
                r = requests.get(downloadLink, headers=header)

            df_aux = pd.read_excel(r.content)
            df_result = df_result.append(df_aux)
        #
        # print(df)
    buffer = io.BytesIO()
    df_result.to_excel(buffer, index=False)
    buffer.seek(0)

    return send_file(
        buffer,
        download_name="data.xlsx",
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # return jsonify(df_result.to_dict())


@app.route("/api/downloadfiles", methods=['POST', 'GET'])
def sendEndpoints():
    print("*** Download File *******")
    
    #get the endponit from frontend
    json_data = request.get_json()
    endpoint = json_data['endpoint']

    print("Making request to: {}".format(endpoint))

    #make the request to API
    header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
              "accept": "application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
    r = requests.get(endpoint, headers=header)

    # if the download failed, try again
    while r.status_code != 200:
        sleep(0.5)
        print("Making request to: {}".format(endpoint))
        r = requests.get(endpoint, headers=header)

    #return a response as xlsx file format
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
    
    link  = json_data['url']
    
    print("Enviando Link para a API: {}".format(link))

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

    try:
        downloadUrl = json_data['data']['downloadUrl']
        url = "https://exportcomments.com"+downloadUrl
    except:
        url = ' '

    # build the full download url
    print("--Link de download gerado: {}".format(url))

    #exportLink = Exportlink()
    #exportLink.link = linksArray

    Exportlink = {
        'link': url
     }
    
    return jsonify(Exportlink)
    

if __name__ == '__main__':
    app.run()
