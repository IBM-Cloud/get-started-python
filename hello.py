from flask import Flask, render_template, request
import cf_deployment_tracker
import os

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/visitors', methods=['GET', 'POST'])
def hello_world():
    content = request.json
    return "Hello " + content['name'] + "!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
