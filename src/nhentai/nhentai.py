# -- NHentai Module --
from random import randrange

from bs4 import BeautifulSoup
import requests
import re

from utils import utilities

proxyDict = utilities.get_proxy()

class Doujin():
    '''
    This is Doujin Class

    Doujin{
        parodies    : List
        tags        : List
        artists     : List
        id          : int
        cover       : url
        title       : str
        url         : url
        characters  : List
        groups      : List
        languages   : List
        pages       : int
    }
    '''


    def __init__(self, url:str) -> None:
        print("Getting:",url)
        self.url = url
        soup = BeautifulSoup(requests.get(self.url, proxies=proxyDict).text, 'lxml')
        
        self.valid = 1
        if soup.find("div", id="content").div.h1.text == "404 – Not Found":
            self.valid = 0
            return

        self.cover = soup.find("div", id="cover").a.img["data-src"]
        self.id = soup.find("h3", id="gallery_id").text[1:]
        
        # parodies, characters, tags, artists, groups, languages, categories, pages, upload date, title
        info = list(soup.find("section", id="tags").children)
        try:
            self.parodies = list(map(lambda a : a.span.text.capitalize(), list(info[0].span.children)))
        except AttributeError:
            self.parodies = []
        try:
            self.characters = list(map(lambda a : a.span.text.capitalize(), list(info[1].span.children)))
        except AttributeError:
            self.characters = []
        try:
            self.tags = list(map(lambda a : a.span.text.capitalize(), list(info[2].span.children)))
        except AttributeError:
            self.tags = []
        try:
            self.artists = list(map(lambda a : a.span.text.capitalize(), list(info[3].span.children)))
        except AttributeError:
            self.artists = []
        try:
            self.groups = list(map(lambda a : a.span.text.capitalize(), list(info[4].span.children)))
        except AttributeError:
            self.groups = []
        try:
            self.languages = list(map(lambda a : a.span.text, list(info[5].span.children)))
        except AttributeError:
            self.languages = []
        try:
            self.pages = int(info[7].span.a.span.text)
        except AttributeError:
            self.pages = 0

        try:  
            self.title = "".join(map(lambda span : span.text, list(soup.find("div", id="info").h1.children)))
        except AttributeError:
            self.title = ""

class NHentai():
    '''
    This is an NHentai Class

    Methods:
    get_doujin : gets the Doujin instance from the id
    search : gets a random id from the search query results
    random : gets a random doujin
    popular : gets the popular page doujins
    '''

    
    def __init__(self) -> None:
        pass

    def get_doujin(self, id:int) -> Doujin:
        if id[:22] == "https://nhentai.net/g/":
            return Doujin(id)
        else:
            return Doujin("https://nhentai.net/g/"+str(id))

    def search(self, query:str, lower = 1, upper = 1) -> list:
        urls = []
        for i in range(lower, upper+1):
            url = "https://nhentai.net/search/?q="+"+".join(query.split())+"&page="+str(i)
            soup = BeautifulSoup(requests.get(url, proxies=proxyDict).text, 'lxml')
            

            # If there are no results
            if i == 1:
                results = soup.find("div", id="content").h1.text.strip()
                if results == "0 results":
                    return []

            container = list(list(soup.find("div", id="content").children)[3].children)
            for i in container:
                urls.append("https://nhentai.net"+i.a["href"])
        return urls

    def random(self) -> Doujin:
        url = "https://nhentai.net/"
        soup = BeautifulSoup(requests.get(url, proxies=proxyDict).text, 'lxml')

        link = list(list(soup.find("div", id="content").children)[2].children)[1].a["href"]
        regex = re.compile(r"(?<=/g/)(.*)(?=/)")
        latest_id = int(regex.findall(link)[0]) # find the last id

        id = randrange(1, latest_id)

        return Doujin("https://nhentai.net/g/"+str(id))

    def popular(self) -> list:
        url = "https://nhentai.net/"
        soup = BeautifulSoup(requests.get(url, proxies=proxyDict).text, 'lxml')

        container = soup.find("div", id="content").section.next_sibling.h2.next_siblings
        popular = []
        for i in container:
            link = "https://nhentai.net"+i.a["href"]
            popular.append(link)

        return popular