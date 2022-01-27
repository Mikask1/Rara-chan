# -- Instagram Module --
from random import choice, randrange
import time
import os
from datetime import datetime
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import requests
import json

CHROMEDRIVER = r"src\instagram\chromedriver.exe"

opt = webdriver.ChromeOptions()
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
# opt.add_argument("--headless")
cookies = pickle.load(open(r"src\instagram\cookies.pkl", "rb"))
driver = webdriver.Chrome(executable_path=CHROMEDRIVER, options=opt)
driver.get("https://www.instagram.com/")
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

class Post():
    '''
    This is a Post Class

    Post{
        media       : url
        caption     : str
        upload date : str
    }
    '''

    class Media():
        def __init__(self, container):
            media_type_dct = {1: "image", 2: "video"}
            self.media_type = media_type_dct[container["media_type"]]
            
            if self.media_type == "image":
                self.url = container["image_versions2"]["candidates"][0]["url"]
            elif self.media_type == "video":
                self.url = container["video_versions"][0]["url"]

    def __init__(self, url) -> None:
        self.url = url
        url += "?__a=1"

        request = session.get(url).text

        container = json.loads(request)["items"][0]
        unix = container["taken_at"]
        self.upload_date = datetime.utcfromtimestamp(unix).strftime('%d %B %Y %H:%M:%S')

        self.is_carousel = True if container["media_type"] == 8 else False

        if self.is_carousel:
            self.media = []
            for item in container["carousel_media"]:
                self.media.append(self.Media(item))
        else:
            self.media = self.Media(container)

        self.caption = container["caption"]["text"] if container["caption"] else None

class Profile():
    '''
    This is a Profile Class

    Profile{
        username : str
        link : url
        driver : Selenium Driver
    }

    Methods:
    load_profile : Loads an Instagram profile
    get_random_post : Get a random post from the profile
    get_post : Get an indexed post from the profile
    '''


    def __init__(self) -> None:
        pass

    async def _init(self, query):
        self.link = None
        self.exist = 1
        if query[:26] == "https://www.instagram.com/":
            self.link = query
        else:
            search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
            search.clear()
            search.send_keys(query)

            # Waits until the search bar finishes it's search
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-hidden='false']")))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='none']")))
            results = driver.find_elements(By.XPATH, "//div[@role='none']")

            index = 0
            if results: # if the search query returns anything
                while results: # Checks if the result is an account
                    self.link = results[index].find_element(By.TAG_NAME, "a").get_attribute("href")
                    if "explore" in self.link:
                        index += 1
                        continue
                    break
            else:
                self.exist = 0
        
        if self.link:
            self.username = self.link[26:-1]
            driver.get(self.link)

    def load_profile(self, index) -> list:
        '''
        Load the account's posts
        '''

        posts = {}
        
        links = []
        while len(posts) < index: # Keeps scrolling down until the index of the post is found
            if index > 12:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//a[@tabindex='0']")))
            links = driver.find_elements(By.XPATH, "//a[@tabindex='0']")
            for a in links: # Adds non-duplicate links using a dictionary
                link = a.get_attribute("href")
                if "/p/" in link:
                    posts[link] = 0

            time.sleep(0.8)

        return list(posts.keys())

    async def get_random_post(self) -> str:
        '''
        Gets a random post from the account
        '''

        n_posts = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "g47SY "))).get_attribute("innerText").strip())
        posts = self.load_profile(randrange(n_posts % 60)) # Makes sure the randrange does not exceed 60

        try:
            post_url = choice(posts)
            return post_url
        except IndexError:
            return 0

    async def get_post(self, index) -> str:
        '''
        Gets a post based on an index
        '''

        posts = self.load_profile(index)
        try:
            post_url = posts[index-1]
            return post_url
        except IndexError:
            return 0
    
    async def get_properties(self, url) -> Post:
        return Post(url)

def instagram_login():
    '''
    Logs into instagram and save the cookies

    Enter username and password, 
    then press "Save Info" to save login info
    then press "Turn On" to turn on notification
    then saves the cookies in a pickle which will be applied in the future to the webdriver
    '''
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pickle
    from dotenv import load_dotenv

    load_dotenv()
    USERNAME = os.getenv("ig_username")
    PASSWORD = os.getenv("ig_password")

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER, options=opt)
    driver.get("https://www.instagram.com/")

    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    password.clear()   
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save Info')]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Turn On')]"))).click()

    pickle.dump(driver.get_cookies() , open(r"src\instagram\cookies.pkl", "wb"))
    driver.close()

async def create_profile(query):
    profile = Profile()
    await profile._init(query)
    return profile


async def main():
    profile1 = await create_profile("tom holland")
    url1 = await profile1.get_post(1)
    task1 = asyncio.create_task(profile1.get_properties(url1))

    post1 = await task1
    for i in post1.media:
        print(i.url)

if __name__ == "__main__":
    asyncio.run(main())