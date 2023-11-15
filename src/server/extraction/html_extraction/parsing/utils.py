import bs4


def create_html_bs4(html_content: str):
    return bs4.BeautifulSoup(markup=html_content, features='html.parser')


def get_messages_chain(e: BaseException) -> str:
    chain: str = str(e)

    current_e = e.__cause__
    while current_e is not None:
        chain += f': {str(current_e)}'
        current_e = current_e.__cause__

    return chain
