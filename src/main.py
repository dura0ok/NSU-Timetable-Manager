from flask import Flask
from timetable_crawler import get_timetable

app = Flask(__name__)


@app.route('/<group_id>')
def hello_world(group_id):
    return get_timetable(group_id)


if __name__ == '__main__':
    app.run()
