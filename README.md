# Hello World Python Flask

This is a sample application showing how to deploy a simple Flask-based hello world app using Cloud Foundry and the Python buildpack.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/IBM-Bluemix/python-hello-world-flask.git)

![Bluemix Deployments](https://deployment-tracker.mybluemix.net/stats/4f7252bee5e6aa6f1611b130ee63dd98/badge.svg)

## Running the app on Bluemix

1. If you do not already have a Bluemix account, [sign up here][bluemix_signup_url]

2. Download and install the [Cloud Foundry CLI][cloud_foundry_url] tool

3. Clone the app to your local environment from your terminal using the following command:

  ```
  $ git clone https://github.com/IBM-Bluemix/python-hello-world-flask.git
  ```

4. `cd` into this newly created directory

5. Connect to Bluemix in the command line tool and follow the prompts to log in.

  ```
  $ cf api https://api.ng.bluemix.net
  $ cf login
  ```

6. Push the app to Bluemix.

  ```
  $ cf push
  ```

And voila! You now have your very own instance of the Python Hello World sample app running on Bluemix.

## Run the app locally
1. If you do not already have a Bluemix account, [sign up here][bluemix_signup_url]

2. If you have not already, [download Python][download_python_url] and install it on your local machine. There are a number of best practices for developing locally with Python and we will leave the excersice of learning those up to you.

3. Clone the app to your local environment from your terminal using the following command:

  ```
  $ git clone https://github.com/IBM-Bluemix/python-hello-world-flask.git
  ```

4. `cd` into this newly created directory

5. Create a new virtual environment with [virtualenv][virtualenv_url] and activate

  ```
  $ virtualenv venv
  $ source venv/bin/activate
  ```
  
6. Install the dependencies with pip

  ```
  $ pip install -r requirements.txt
  ```

7. Start your app locally with the following command

  ```
  $ python hello.py
  ```

This command will create a new Flask app and start your application. When your app has started, your console will print that your `Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)`.

## Troubleshooting

The primary source of debugging information for your Bluemix app is the logs. To see them, run the following command using the Cloud Foundry CLI:

  ```
  $ cf logs hello-world-flask --recent
  ```
For more detailed information on troubleshooting your application, see the [Troubleshooting section](https://www.ng.bluemix.net/docs/troubleshoot/troubleshoot.html) in the Bluemix documentation.

## Contribute
We are more than happy to accept external contributions to this project, be it in the form of issues and pull requests. If you find a bug, please report it via the [Issues section][issues_url] or even better, fork the project and submit a pull request with your fix! Pull requests will be evaulated on an individual basis based on value add to the sample application.

## Privacy Notice

The hello-world-flask sample web application includes code to track deployments to Bluemix and other Cloud Foundry platforms. The following information is sent to a [Deployment Tracker](https://github.com/IBM-Bluemix/cf-deployment-tracker-service) service on each deployment:

* Python package version
* Python repository URL
* Application Name (`application_name`)
* Space ID (`space_id`)
* Application Version (`application_version`)
* Application URIs (`application_uris`)
* Labels of bound services
* Number of instances for each bound service and associated plan information

This data is collected from the `setup.py` file in the sample application and the `VCAP_APPLICATION` and `VCAP_SERVICES` environment variables in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix to measure the usefulness of our examples, so that we can continuously improve the content we offer to you. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

### Disabling Deployment Tracking

Deployment tracking can be disabled by removing `cf_deployment_tracker.track()` from the `hello.py` file.

## License

This app is covered by the Apache 2.0 license. For more information, see [License.txt](License.txt) for license information.

[live_demo_url]: https://capital-weather.mybluemix.net/
[bluemix_signup_url]: https://console.ng.bluemix.net/registration/
[cloud_foundry_url]: https://github.com/cloudfoundry/cli
[download_python_url]: https://www.python.org/downloads/
[virtualenv_url]: https://virtualenv.pypa.io/en/stable/
[issues_url]: https://github.com/IBM-Bluemix/python-hello-world-flask/issues
