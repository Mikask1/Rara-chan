# -- Instagram Module --
from random import choice, randrange
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle

import os

opt = webdriver.ChromeOptions()
opt.add_experimental_option('excludeSwitches', ['enable-logging'])
cookies = pickle.load(open(r"src\instagram\cookies.pkl", "rb"))

class Post():
    '''
    This is a Post Class

    Post{
        media       : url
        caption     : str
        upload date : str
    }
    '''

    def __init__(self, url, driver) -> None:
        driver.get(url)
        self.url = url

        self.media_type = "image"
        try: # Checks if the content is an image or video
            image_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button']"))).find_element(By.TAG_NAME, "img")
            self.media = image_element.get_attribute("src")

            if self.media == None: # Checks if the content is a video
                video_element = driver.find_element(By.TAG_NAME, "video")
                self.media = video_element.get_attribute("src")
                self.media_type = "video"
        except Exception:
            video_element = driver.find_element(By.TAG_NAME, "video")
            self.media = video_element.get_attribute("src")
            self.media_type = "video"
        
        try: # Checks if a caption exists
            caption_element = driver.find_element(By.XPATH, "//li[@role='menuitem']").find_element(By.TAG_NAME, "span")
            self.caption = caption_element.get_attribute("innerText")
        except Exception:
            self.caption = "."
        
        upload_date_element = driver.find_element(By.XPATH, "//a[@href='"+url[25:]+"']/*")
        self.upload_date = upload_date_element.get_attribute("innerText").capitalize()

        driver.quit()

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


    def __init__(self, query) -> None:
        link = ""

        self.driver = webdriver.Chrome(executable_path=r"src\instagram\chromedriver.exe", options=opt)

        self.driver.get("https://www.instagram.com/")
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.exist = 1
        if query[:26] == "https://www.instagram.com/":
            link = query
        else:
            self.driver.refresh() # Refresh to apply the cookies

            search = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
            search.clear()
            search.send_keys(query)

            # Waits until the search bar finishes it's search
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-hidden='false']")))
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@role='none']")))
            results = self.driver.find_elements(By.XPATH, "//div[@role='none']")

            index = 0
            if results: # if the search query returns anything
                while results: # Checks if the result is an account
                    link = results[index].find_element(By.TAG_NAME, "a").get_attribute("href")
                    if "explore" in link:
                        index += 1
                        continue
                    break
            else:
                raise 
        
        if link:
            self.link = link
            self.username = link[26:-1]
            self.driver.get(link)

    def load_profile(self, index) -> list:
        '''
        Load the account's posts
        '''

        posts = {}
        while len(posts) < index: # Keeps scrolling down until the index of the post is found
            links = self.driver.find_elements(By.XPATH, "//a[@tabindex='0']")

            for a in links: # Adds non-duplicate links using a dictionary
                link = a.get_attribute("href")
                if "/p/" in link:
                    posts[link] = 0

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        return list(posts.keys())

    def get_random_post(self) -> Post:
        '''
        Gets a random post from the account
        '''

        n_posts = int(WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "g47SY "))).get_attribute("innerText").strip())
        posts = self.load_profile(randrange(n_posts % 60)) # Makes sure the randrange does not exceed 60

        try:
            post_url = choice(posts)
            return Post(post_url, self.driver)
        except IndexError:
            return 0

    def get_post(self, index) -> Post:
        '''
        Gets a post based on an index
        '''

        posts = self.load_profile(index)
        try:
            post_url = posts[index-1]
            return Post(post_url, self.driver)
        except IndexError:
            return 0