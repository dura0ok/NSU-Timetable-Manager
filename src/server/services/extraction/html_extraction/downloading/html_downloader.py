import requests

from .html_downloading_exception import HTMLDownloadingException


class HTMLDownloader:
    __timeout: int = 5  # In seconds

    @staticmethod
    def download(url: str) -> str:
        try:
            response: requests.Response = requests.get(url, timeout=HTMLDownloader.__timeout)
        except (requests.ReadTimeout, requests.ConnectionError) as e:
            raise HTMLDownloadingException(str(e))
        else:
            if not response.ok:
                raise HTMLDownloadingException('Cannot download HTML')

        return response.text
