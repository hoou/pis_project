from os import getenv

from flask import Flask, jsonify

# instantiate the app
app = Flask(__name__)

# set config
app_settings = getenv('APP_SETTINGS')
app.config.from_object(app_settings)


@app.route('/ping')
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
