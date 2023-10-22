from flask import Flask
from flask_cors import CORS

from extractor import Extractor
from html_extraction import HTMLExtractor


def split_url_word(url_word: str) -> str:
    return ' '.join(url_word.split('+'))


app = Flask(__name__)
CORS(app)
extractor: Extractor = HTMLExtractor()


@app.route('/timetable/<group_id>')
def get_timetable(group_id: str) -> str:
    return extractor.extract_timetable(group_id).to_json()


@app.route('/room/<room_name>')
def get_room(room_name: str) -> str:
    return extractor.extract_room(split_url_word(room_name)).to_json()


@app.route('/tutor/<tutor_name>')
def get_tutor(tutor_name: str) -> str:
    return extractor.extract_tutor(split_url_word(tutor_name)).to_json()


@app.route('/times')
def get_times() -> str:
    return extractor.extract_times().to_json()


app.run()
