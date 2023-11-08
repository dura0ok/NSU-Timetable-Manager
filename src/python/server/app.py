import logging
from logging.config import dictConfig

import werkzeug
from flask import Flask, request
from markupsafe import escape

from common import Serializer, JSONSerializer, ServerResponse
from extraction import HTMLExtractor, Extractor
from server_logging import *


def split_url_word(url_word: str) -> str:
    return ' '.join(url_word.split('+'))


def configure_logging() -> None:
    # Disable default logger
    logging.getLogger('werkzeug').disabled = True

    # Add file handler
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s : %(message)s',
        }},
        'handlers': {'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'default',
            'mode': 'w',
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['file']
        }
    })


configure_logging()
app = Flask(__name__)
extractor: Extractor = HTMLExtractor()
serializer: Serializer = JSONSerializer()


def handle_response(response: ServerResponse) -> bytes:
    log_response(logger=app.logger, response=response, _request=request)
    return serializer.serialize(response)


@app.route('/timetable/<group_id>', methods=['GET'])
def get_timetable(group_id: str) -> bytes:
    return handle_response(response=extractor.extract_timetable(escape(group_id)))


@app.route('/room/<room_name>', methods=['GET'])
def get_room(room_name: str) -> bytes:
    return handle_response(response=extractor.extract_room(split_url_word(escape(room_name))))


@app.route('/tutor/<tutor_name>', methods=['GET'])
def get_tutor(tutor_name: str) -> bytes:
    return handle_response(response=extractor.extract_tutor(split_url_word(escape(tutor_name))))


@app.route('/times', methods=['GET'])
def get_times() -> bytes:
    return handle_response(response=extractor.extract_times())


@app.before_request
def request_handler():
    log_request(logger=app.logger, _request=request)


@app.errorhandler(werkzeug.exceptions.HTTPException)
def error_handler(e):
    log_http_error(logger=app.logger, e=e, _request=request)
    return e


app.run(host='0.0.0.0')
