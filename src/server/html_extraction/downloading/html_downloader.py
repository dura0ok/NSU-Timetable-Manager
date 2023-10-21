import requests

from .html_downloading_exception import HTMLDownloadingException


class HTMLDownloader:
    @staticmethod
    def download(url: str) -> str:
        response: requests.Response = requests.get(url)

        if not response.ok:
            raise HTMLDownloadingException('Cannot download HTML')

        return response.text
