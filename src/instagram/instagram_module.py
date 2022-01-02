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
opt.add_argument("--headless")
cookies = pickle.load(open(r"src\instagram\cookies.pkl", "rb"))
driver = webdriver.Chrome(executable_path=CHROMEDRIVER, options=opt)
driver.get("https://www.instagram.com/")
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()

class Post():
    '''
    This is a Post Class

    Post{
        media       : url
        caption     : str
        upload date : str
    }
    '''

    def __init__(self, url) -> None:
        self.url = url
        url += "?__a=1"
        container = json.loads(requests.get(url).text)["graphql"]["shortcode_media"]


        self.is_video = container["is_video"]
        if self.is_video:
            self.media = container["video_url"]
        else:
            self.media = container["display_resources"][-1]["src"]

        caption_container = container["edge_media_to_caption"]["edges"]
        if caption_container:
            self.caption = caption_container[0]["node"]["text"]
        else:
            self.caption = "."

        self.unix = container["taken_at_timestamp"]
        self.upload_date = datetime.utcfromtimestamp(self.unix).strftime('%d %B %Y %H:%M:%S')
        
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
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//a[@tabindex='0']")))
            links = driver.find_elements(By.XPATH, "//a[@tabindex='0']")
            for a in links: # Adds non-duplicate links using a dictionary
                link = a.get_attribute("href")
                if "/p/" in link:
                    posts[link] = 0

            time.sleep(0.8)

        return list(posts.keys())


    def download(self, start, end):
        """
        Downloads every single post from start to end (1 based index).
        It only works with images because videos have weird links

        How does it work?
        1. Open chrome and visit instagram and load the cookies in it (login credentials)
        2. Input the query onto the search bar and returns the first account
        3. Loads all the post and getting their links by scrolling down until the `end` index is found
        4. Loads all the post and gets the image from each one of them
        5. Writes the byte stream onto a .jpg file
        """
        
        PATH = "src/instagram/posts/"

        posts = self.load_profile(end)[start-1:end]

        index = 1
        if PATH not in os.listdir():
            os.mkdir("posts")
        
        for post_url in posts:
            try:
                post = Post(url=post_url)

                url = post.media
                if not post.is_video:
                    with open(PATH+str(index)+".jpg", "wb") as file:
                        file.write(requests.get(url).content)
                else:
                    with open(PATH+str(index)+".mp4", "wb") as file:
                        file.write(requests.get(url).content)

                index += 1
            except Exception:
                print(f"Error in {index}")
                continue

    async def get_random_post(self) -> Post:
        '''
        Gets a random post from the account
        '''

        n_posts = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "g47SY "))).get_attribute("innerText").strip())
        posts = self.load_profile(randrange(n_posts % 60)) # Makes sure the randrange does not exceed 60

        try:
            post_url = choice(posts)
            return Post(post_url)
        except IndexError:
            return 0

    async def get_post(self, index) -> Post:
        '''
        Gets a post based on an index
        '''

        posts = self.load_profile(index)
        try:
            post_url = posts[index-1]
            return Post(post_url)
        except IndexError:
            return 0

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
    profile = await create_profile("real yami")
    await profile.get_post(40)