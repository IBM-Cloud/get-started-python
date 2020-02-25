###############################################################################
# Copyright IBM Corporation 2018                                              #
#                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License");             #
# you may not use this file except in compliance with the License.            #
# You may obtain a copy of the License at                                     #
#                                                                             #
# http://www.apache.org/licenses/LICENSE-2.0                                  #
#                                                                             #
# Unless required by applicable law or agreed to in writing, software         #
# distributed under the License is distributed on an "AS IS" BASIS,           #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
# See the License for the specific language governing permissions and         #
# limitations under the License.                                              #
###############################################################################
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
import ssl
import re
from pymongo import MongoClient

app = Flask(__name__, static_url_path='')

db_name = 'mydb'
collection_name = 'mycollection' # MongoDB requires a collection name.
client = None
db = None
vendor_name = None # Record DB vendor to determine which methods are used.

# Allow for any service with some permutation of a vendor name to be used
# (this is mostly to provide a general solution for user-provided services).
mongo_re = re.compile(r'.*[Mm][Oo][Nn][Gg][Oo].*')
cloudant_re = re.compile(r'.*[Cc][Ll][Oo][Uu][Dd][Aa][Nn][Tt].*')

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')

    mongo_result = next(iter(filter(lambda key: mongo_re.search(key) != None, vcap)), None)
    cloudant_result = next(iter(filter(lambda key: cloudant_re.search(key) != None, vcap)), None)
    user_provided_result = next(iter(filter(lambda key: key == 'user-provided', vcap)), None)

    # Allow for user-provided services to be used.
    if user_provided_result:
        if mongo_re.search(vcap[user_provided_result][0]['name']):
            mongo_result = user_provided_result
        elif cloudant_re.search(vcap[user_provided_result][0]['name']):
            cloudant_result = user_provided_result

    if mongo_result:
        creds = vcap[mongo_result][0]['credentials']
        uri = creds['uri']
        client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
        db = client[db_name][collection_name]
        vendor_name = 'mongo'
    elif cloudant_result:
        creds = vcap[cloudant_result][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
        vendor_name = 'cloudant'

elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
    vendor_name = 'cloudant'

elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        
        mongo_result = next(iter(filter(lambda key: mongo_re.search(key) != None, vcap['services'])), None)
        cloudant_result = next(iter(filter(lambda key: cloudant_re.search(key) != None, vcap['services'])), None)
        
        if mongo_result:
            #creds = vcap['services']['compose-for-mongodb'][0]['credentials']
            creds = vcap['services'][mongo_result][0]['credentials']
            uri = creds['uri']
            client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)
            db = client[db_name][collection_name]
            vendor_name = 'mongo'
        elif cloudant_result:
            #creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
            creds = vcap['services'][cloudant_result][0]['credentials']
            user = creds['username']
            password = creds['password']
            url = 'https://' + creds['host']
            client = Cloudant(user, password, url=url, connect=True)
            db = client.create_database(db_name, throw_on_exists=False)
            vendor_name = 'cloudant'

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

def get_visitor_cloudant():
    return list(map(lambda doc: doc['name'], db))

def get_visitor_mongo():
    return list(map(lambda doc: doc['name'], db.find(projection={"_id": False, "count": False})))

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        # Call vendor-specific handler.
        return jsonify(globals()['get_visitor_' + vendor_name]())
    else:
        print('No database')
        return jsonify([])

def add_visitor_cloudant(data):
    my_document = db.create_document(data)
    data['_id'] = my_document['_id']
    return data

def add_visitor_mongo(data):
    data['_id'] = str(db.insert_one(data).inserted_id)
    return data

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        # Call vendor-specific handler.
        data = globals()['add_visitor_' + vendor_name](data)
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
