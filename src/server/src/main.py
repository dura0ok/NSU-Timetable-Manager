from flask import Flask
from src.parsing import *
from src.parsing.parsing_exceptions import ParsingException
from src.parsing.parsing_result import ParsingResult, create_error_parsing_result
from src.timetable_objects import *


app = Flask(__name__)


@app.route('/room/<room_name>')
def get_room(room_name: str) -> str:
    return parse_room(room_name).to_json()


@app.route('/timetable/<group_id>')
def get_timetable(group_id: str) -> str:
    try:
        timetable: Timetable = parse_timetable_from_group_id(group_id)
        return ParsingResult(result=timetable).to_json()
    except ParsingException as e:
        return create_error_parsing_result(str(e)).to_json()


@app.route('/times/')
def get_times() -> str:
    return parse_times().to_json()


app.run()
