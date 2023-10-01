import requests


class HTMLDownloadingException(Exception):
    pass


def download_html(url: str) -> str:
    response: requests.Response = requests.get(url)

    if not response.ok:
        raise HTMLDownloadingException()

    return response.text
