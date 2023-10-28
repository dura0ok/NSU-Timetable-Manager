from flask import Flask
from flask_cors import CORS, cross_origin
from markupsafe import escape

from extractor import Extractor
from html_extraction import HTMLExtractor


def split_url_word(url_word: str) -> str:
    return ' '.join(url_word.split('+'))


app = Flask(__name__)
CORS(app)
extractor: Extractor = HTMLExtractor()


@cross_origin()
@app.route('/timetable/<group_id>')
def get_timetable(group_id: str) -> str:
    return extractor.extract_timetable(escape(group_id)).to_json()


@cross_origin()
@app.route('/room/<room_name>')
def get_room(room_name: str) -> str:
    return extractor.extract_room(split_url_word(escape(room_name))).to_json()


@cross_origin()
@app.route('/tutor/<tutor_name>')
def get_tutor(tutor_name: str) -> str:
    return extractor.extract_tutor(split_url_word(escape(tutor_name))).to_json()


@cross_origin()
@app.route('/times')
def get_times() -> str:
    return extractor.extract_times().to_json()


app.run()
