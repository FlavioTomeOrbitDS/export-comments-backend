from flask import Flask, send_file, request, jsonify, make_response
from flask_cors import CORS
import requests
import io
import urllib.parse
from time import sleep
import os


app = Flask(__name__)
CORS(app)

# How Export Comments API Works:
# First we send an url (instagram, face, youtube post) to API to generate an Download Endpoint
# Then we send de build the full link and send it to API

#****************************************************************************************************#
# Send requests to ExportComments API and get the download file endpoint as response


@app.route("/api/generateEndpoints", methods=['POST', 'GET'])
def generateEndpoints():

    from time import sleep

    # gets the link passed by the frontend
    json_data = request.get_json()
    link = json_data['url']

    # encodes the endpoint as the specified in API documentation
    encoded_link = urllib.parse.quote(link, safe='')

    # builds the request to send to exportcomments API
    url = "https://exportcomments.com/api/v2/export?url={}".format(
        encoded_link)
    header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
              "accept": "application/json"}

    print("SEND TO API: {}".format(url))

    # the api oly supports a few number of requests each time.
    # Then, when the API returns 429 code, the script waits 5 seconds an sends the request again
    full_url = ''
    while full_url == '':
        try:
            response = requests.put(url, headers=header)
            # format response to get the downloadUrl param
            json_data = response.json()
            # print(json_data)
            print(json_data)
            # print("REPONSE CODE: {}".format(json_data['code']))
            downloadUrl = json_data['data']['downloadUrl']
            full_url = "https://exportcomments.com"+downloadUrl
        except:
            full_url = ''
            sleep(5)

    Exportlink = {
        'original_url': link, 
        'link': full_url
    }

    return jsonify(Exportlink)

#****************************************************************************************************#


@app.route("/api/generateEndpointsFromList", methods=['POST', 'GET'])
def generateEndpointsFromList():
    from time import sleep

    # gets the link passed by the frontend
    json_data = request.get_json()
    list_of_endpoints = json_data['list_of_endpoints']

    full_download_url_list = []

    for endpoint in list_of_endpoints:
        # encodes the endpoint as the specified in API documentation
        original_endpoint = endpoint
        endpoint = urllib.parse.quote(endpoint, safe='')

        # builds the request to send to exportcomments API
        url = "https://exportcomments.com/api/v2/export?url={}".format(
            endpoint)
        header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
                  "accept": "application/json"}

        print("SEND TO API: {}".format(url))

        # the api oly supports a few number of requests each time.
        # Then, when the API returns 429 code, the script waits 5 seconds an sends the request again
        full_download_url = ''
        while full_download_url == '':
            try:
                response = requests.put(url, headers=header)
                # format response to get the downloadUrl param
                json_data = response.json()
                # print(json_data)
                print(json_data)
                # print("REPONSE CODE: {}".format(json_data['code']))
                downloadUrl = json_data['data']['downloadUrl']
                full_download_url = "https://exportcomments.com"+downloadUrl
            except:
                full_download_url = ''
                sleep(5)

        full_download_url_list.append({'full_download_url':full_download_url, 'endpoint': original_endpoint})
        sleep(1.0)

    Exportlink = {
        'download_url_list': full_download_url_list
    }

    return jsonify(Exportlink)


#****************************************************************************************************#
@app.route("/api/downloadfiles", methods=['POST', 'GET'])
def sendEndpoints():
    print("***************** Download File ***********************")

    # receive the endpoint from frontend
    json_data = request.get_json()
    endpoint = json_data['endpoint']

    print("Making request to: {}".format(endpoint))

    # make the request to API
    header = {'X-AUTH-TOKEN': 'b11ee661080db564ced715d0f6a88c9adfdbec4e3e7db118f72e720c20defa3b04674c81554a874f8eeba296a0399b2645b34d473fe80eccc5b0a11d',
              "accept": "application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
    try:
        r = requests.get(endpoint, headers=header)
    except:
        # send an Internar Server Error to frontend
        response = make_response('URL Error')
        response.status_code = 500
        return response
        

    #used to limit the number of requests
    requests_count = 0
    # if the download failed, try again
    while r.status_code != 200:
        sleep(1)
        requests_count += 1
        #max number of requests
        if requests_count >= 120:
            print('No data returned by API')            
            # send an Internar Server Error code to frontend
            response = make_response('No data returned by API')
            response.status_code = 500
            return response
            #return jsonify('No data returned by API')
        else:
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
#****************************************************************************************************#
@app.route("/servertest", methods=['POST', 'GET'])
def severtest():
    return 'Server Online!'

@app.route("/")
def hello():
    return 'hello server'

@app.route("/getblob")
def getblob():
    response = make_response('blob retunr')
    response.status_code = 504
    return response
if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0')
