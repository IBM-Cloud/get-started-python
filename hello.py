"""Cloud Foundry test"""
from flask import Flask
import os
 
app = Flask(__name__)
 
port = int(os.getenv("VCAP_APP_PORT"))
 
@app.route('/')
def hello_world():
    return 'Hello World! I am running on port ' + str(port)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
