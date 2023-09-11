#from flask import Flask
from bs4 import BeautifulSoup

#app = Flask(__name__)


# @app.route('/<group_id>')
# def hello_world(group_id):
#     return get_timetable(group_id)


if __name__ == '__main__':
    f = open('index.html')
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')
    print(soup.find("table", {"class": "time-table"}))
