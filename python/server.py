"""
A first simple Cloud Foundry Flask app
Author: Ian Huston
License: See LICENSE.txt
"""
from flask import Flask
from flask import request
import os
import pyhdb
# Downloading pyhdb-0.3.3.tar.gz
import json
import datetime
import Crypto.PublicKey.RSA as RSA
import jws.utils
import python_jwt as jwt

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))

@app.route('/')
def hello_world():
    return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0))

@app.route('/python/test')
def testing_world():
    return 'Testing!!!abc!!! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0))

@app.route('/python/test2')
def testing2_world():
    output = 'Testing More! \n'
    output += '\n'
    output += 'Receiving module should check that it came from our approuter and verify or abort if otherwise.\n'
    output += '\n'
    svcs_json = str(os.getenv("VCAP_SERVICES", 0))
    svcs = json.loads(svcs_json)

	# Verify the JWT before proceeding. or refuse to process the request.
	# https://jwt.io/ JWT Debugger Tool and libs for all languages
    # https://github.com/jpadilla/pyjwt/
    # https://github.com/davedoesdev/python-jwt

    vkey = svcs["xsuaa"][0]["credentials"]["verificationkey"]
    secret = svcs["xsuaa"][0]["credentials"]["clientsecret"]

    #output += 'vkey: ' + vkey + '\n'
    #output += 'secret: ' + secret + '\n'

    #jwt.decode(encoded, verify=False)
    req_host = request.headers.get('Host')
    req_auth = request.headers.get('Authorization')

    #output += 'req_host: ' + req_host + '\n'
    #output += 'req_auth: ' + req_auth + '\n'

    #import jwt
    #output += 'req_auth = ' + req_auth + '\n'

    if req_auth.startswith("Bearer "):
    	output += 'JWT Authorization is of type Bearer! \n'
    else:
    	output += 'JWT Authorization is not of type Bearer! \n'

    output += '\n'

    jwtoken = req_auth[7:]

    #output += 'secret = ' + secret + '\n'

#https://github.com/brianloveswords/python-jws/blob/master/examples/minijwt.py    KEY!
#import Crypto.PublicKey.RSA as RSA
#import jws.utils
#https://pythonhosted.org/Flask-JWT/  ???
#req_auth = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIxMTk1NWFlMC1mOThhLTQyZGItYTg1ZC0wZDlmMjg4ZTdkZGUiLCJzdWIiOiIxNjY4OTEiLCJzY29wZSI6WyJvcGVuaWQiXSwiY2xpZW50X2lkIjoic2ItbmEtNWVmYjk3MjQtNjY2NS00OWIzLTg3NWYtNDc5OTA5NWExZGJhIiwiY2lkIjoic2ItbmEtNWVmYjk3MjQtNjY2NS00OWIzLTg3NWYtNDc5OTA5NWExZGJhIiwiYXpwIjoic2ItbmEtNWVmYjk3MjQtNjY2NS00OWIzLTg3NWYtNDc5OTA5NWExZGJhIiwiZ3JhbnRfdHlwZSI6ImF1dGhvcml6YXRpb25fY29kZSIsInVzZXJfaWQiOiIxNjY4OTEiLCJ1c2VyX25hbWUiOiJYU0FfREVWIiwiZW1haWwiOiJYU0FfREVWQHVua25vd24iLCJmYW1pbHlfbmFtZSI6IlhTQV9ERVYiLCJpYXQiOjE0OTUwODQxMTMsImV4cCI6MTQ5NTEyNzMxMywiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3VhYS9vYXV0aC90b2tlbiIsInppZCI6InVhYSIsInhzLnVzZXIuYXR0cmlidXRlcyI6e30sImF1ZCI6WyJzYi1uYS01ZWZiOTcyNC02NjY1LTQ5YjMtODc1Zi00Nzk5MDk1YTFkYmEiLCJvcGVuaWQiXX0.g--w87ds_4vmRSsdDpMWZ8gJ0gGGnRmWIqGfOrzz4lV4lcYFWqqaaF2eMnlJSiQ2IADfelAOR8Vk2jkxHXwgAU8XLTgQpU4XvWqURcCGOL9g7JLbdH2mxLfZl_3gqDrsZzYr94ucFJtrweuNIz58ndMr00_5iIu1gMfUnEhaz9SaR4Uuonv5n1mz2_dKC-DwAsyjWgTbJJmNtvp9sUpDYpuuTcbyGQUIgzsvueP6SzzQonJmweggSUFRzOuTJKx7TLc5DHBD44Ziv0cYpthSUFk7ynzcaat5GpHQyTGinKgU4XYkNXWf1m2tLPSTrFVgePf1Xx4pdkrcf-ujuXbMnQ"
#req_auth.startswith("Bearer ")
#jwtoken = req_auth[7:]

# Demo to Volker

    # The PKEY in the env has the \n stripped out and the importKey expects them!
    pub_pem = "-----BEGIN PUBLIC KEY-----\n" + vkey[26:-24] + "\n-----END PUBLIC KEY-----\n"
    #output += 'pub_pem = ' + pub_pem + '\n'

    pub_key = RSA.importKey(pub_pem)
    (header, claim, sig) = jwtoken.split('.')
    header = jws.utils.from_base64(header)
    claim = jws.utils.from_base64(claim)
    if jws.verify(header, claim, sig, pub_key, is_json=True):
        output += 'JWT is Verified! \n'
    else:
        output += 'JWT FAILED Verification! \n'

    output += '\n'

    schema = svcs["hana"][0]["credentials"]["schema"]
    user = svcs["hana"][0]["credentials"]["user"]
    password = svcs["hana"][0]["credentials"]["password"]
    conn_str = svcs["hana"][0]["credentials"]["url"]
    host = svcs["hana"][0]["credentials"]["host"]
    port = svcs["hana"][0]["credentials"]["port"]
    driver = svcs["hana"][0]["credentials"]["driver"]

    output += 'schema: ' + schema + '\n'
    output += 'user: ' + user + '\n'
    output += 'password: ' + password + '\n'
    output += 'conn_str: ' + conn_str + '\n'
    output += 'host: ' + host + '\n'
    output += 'port: ' + port + '\n'
    output += 'driver: ' + driver + '\n'

    output += '\n'
    connection = pyhdb.connect(host,int(port),user,password)
    cursor = connection.cursor()
    cursor.execute('SELECT "tempId", "tempVal", "ts", "created" FROM "' + schema + '"."sensors.temp"')
    sensor_vals = cursor.fetchall()

    for sensor_val in sensor_vals:
        output += 'sensor_val: ' + str(sensor_val[1]) + ' at: ' + str(sensor_val[2]) + '\n'

    connection.close()

    return output

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
