import bs4.element
import requests
from bs4 import BeautifulSoup

from .consts import BASE_URL


def get_timetable(group_num: str):
    table_url = BASE_URL + group_num
    raw_data = get_raw_table(table_url)
    print(f"Raw data: {type(raw_data)}")
    rows = raw_data.findAll("tr")
    for item in rows:
        el = item.select_one("td:nth-child(2)")
        if el is not None:
            print(el.text)
    return 'ok'


def get_raw_table(table_url: str) -> bs4.element.Tag:
    raw_resp = requests.get(table_url)
    if raw_resp.status_code != 200:
        raise Exception(f"Invalid status code: {raw_resp.status_code}")
    soup = BeautifulSoup(raw_resp.text, 'html.parser')
    return soup.find("table", {"class": "time-table"})