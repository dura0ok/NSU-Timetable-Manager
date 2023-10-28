from flask import Flask
from markupsafe import escape

from serialization import Serializer, JSONSerializer
from extraction import HTMLExtractor, Extractor


def split_url_word(url_word: str) -> str:
    return ' '.join(url_word.split('+'))


app = Flask(__name__)

extractor: Extractor = HTMLExtractor()
serializer: Serializer = JSONSerializer()


@app.route('/timetable/<group_id>', methods=['GET'])
def get_timetable(group_id: str):
    return serializer.serialize(extractor.extract_timetable(escape(group_id)))


@app.route('/room/<room_name>', methods=['GET'])
def get_room(room_name: str):
    return serializer.serialize(extractor.extract_room(split_url_word(escape(room_name))))


@app.route('/tutor/<tutor_name>', methods=['GET'])
def get_tutor(tutor_name: str):
    return serializer.serialize(extractor.extract_tutor(split_url_word(escape(tutor_name))))


@app.route('/times', methods=['GET'])
def get_times():
    return serializer.serialize(extractor.extract_times())


app.run()
