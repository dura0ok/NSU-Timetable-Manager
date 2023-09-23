import bs4

from src.timetable_objects import Room, RoomLocation


def get_room_url(room_name: str) -> str:
    url_name: str = ' '.join(room_name.split()).replace(" ", "+")
    return f'https://table.nsu.ru/room/{url_name}'


def parse_room_name_from_html(html_page: str) -> str:
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html_page, 'html.parser')
    return soup.find('div', {'class': 'main_head'}).find('h1').text[10:]


def parse_room_from_html(html_page: str) -> Room:
    i1 = html_page.find('room_view')

    i2 = html_page.find('(', i1)
    i3 = html_page.find(')', i1)
    values = html_page[i2 + 1:i3].split(',')

    block: str = values[0][6:-6]
    level: i1 = int(values[1])
    x: int = int(values[2])
    y: i1 = int(values[3])

    room_name: str = parse_room_name_from_html(html_page)
    location: RoomLocation = RoomLocation(block=block, level=level, x=x, y=y)

    return Room(name=room_name, location=location)
