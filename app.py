import pytz

from datetime import datetime, timezone
from flask import Flask, render_template, jsonify, request
# from flask_socketio import SocketIO, send, emit
from flask_cors import cross_origin
from copy import deepcopy

from views import manage_user
from views import admin_files
from views import chat_instance

# constants
from common.config import ALLOWED_ORIGINS, TIMEZONE

app = Flask(__name__)
# socketio = SocketIO(app)


LOCAL_TIMEZONE = pytz.timezone(TIMEZONE)


@app.route('/send_question', methods=['POST'])
@cross_origin(cross_origin=ALLOWED_ORIGINS)
def send_question():
    """form: {
        message: string,
        user_id: string,
        user_name: string,
    }
    return: {
        answer: string,
    }
    """
    return chat_instance.get_answer(deepcopy(request.get_json()))


@app.route('/upload_file', methods=['POST'])
@cross_origin(cross_origin=ALLOWED_ORIGINS)
def upload_file():
    """form: {
        file: file,
    }
    return: {
        file_rear: boloean,
    }
    """
    return admin_files.upload_file(request)


@app.route('/get_user_id', methods=['GET'])
@cross_origin(cross_origin=ALLOWED_ORIGINS)
def get_uuid():
    return manage_user.get_user_id()

@app.route('/')
def index():
    return render_template('index2.html')

if __name__ == '__main__':
    # socketio.run(app)
    app.run(debug=True)
