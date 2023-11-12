import uvicorn
from fastapi import FastAPI

from extraction import Extractor
from extraction.html_extraction import HTMLExtractor


def split_url_word(url_word: str) -> str:
    return ' '.join(url_word.split('+'))


app = FastAPI()
extractor: Extractor = HTMLExtractor()


@app.get('/timetable/{group_id}')
def get_timetable(group_id: str):
    return extractor.extract_timetable(split_url_word(group_id))


@app.get('/room/{room_name}')
def get_room(room_name: str):
    return extractor.extract_room(split_url_word(room_name))


@app.get('/tutor/{tutor_name}')
def get_tutor(tutor_name: str):
    return extractor.extract_tutor(split_url_word(tutor_name))


@app.get('/times')
def get_times():
    return extractor.extract_times()


if __name__ == '__main__':
    uvicorn.run('main:app')
