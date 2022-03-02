# -- NSFW Module --
from random import choice

from bs4 import BeautifulSoup
import requests

from utils import utilities

proxyDict = utilities.get_proxy()


class NSFW():
    '''
    This is an NSFW Class

    Methods:
    get_nsfw : gets an NSFw image from imagefap.com
    '''

    def __init__(self) -> None:
        pass

    def get_nsfw(self) -> str:
        html = requests.get(
            "https://www.imagefap.com/pictures/8925384/Zero-Two-%28Darling-in-the-Franxx%29?gid=8925384&view=2", proxies=proxyDict).text
        soup = BeautifulSoup(html, 'lxml')

        # Get the div with id="gallery"
        # Traverse the tree
        # Randomly choose one of the children(rows)
        # Randomly choose one of the children(columns)
        # Go to <img> tag and get the "src"
        try:
            image = choice(list(choice(list(soup.find("div", id="gallery").form.table.children)[
                           1:-1]).children)[1:-1]).img["src"]
        except Exception:
            image = ""
        return image
