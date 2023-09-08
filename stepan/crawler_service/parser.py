import requests
from bs4 import BeautifulSoup

from src.crawler_service.consts import URL


def parse_timetable():
    raw_resp = requests.get(URL)
    if raw_resp.status_code != 200:
        raise Exception("invalid status code")
    soup = BeautifulSoup(raw_resp.text, 'html.parser')
    subjects_schedule_table = soup.find('.time-table')


if __name__ == "__main__":
    parse_timetable()
