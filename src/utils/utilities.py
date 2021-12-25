import os
import time
import discord

from dotenv import load_dotenv

def get_doujin_embed(doujin):
    '''
    Gets the embed form from the provided parameters from the Doujin instance
    '''

    embed = discord.Embed(title=doujin.title, url=doujin.url, color=0xFF5733)

    embed.add_field(name="ID", value=doujin.id, inline=True)
    
    for i in doujin.languages:
        if i == "english":
            embed.add_field(name="Language", value="English", inline=True)
            break
    else:
        embed.add_field(name="Language", value="Non-English", inline=True)

    embed.add_field(name="Page", value=doujin.pages, inline=True)

    if len(doujin.parodies) != 0:
        embed.add_field(name="Parodies", value=", ".join(doujin.parodies), inline=False)

    if len(doujin.characters) != 0:
        embed.add_field(name="Characters", value=", ".join(doujin.characters), inline=False)

    if len(doujin.tags) != 0:
        embed.add_field(name="Tags", value=", ".join(doujin.tags), inline=False)

    if len(doujin.artists) != 0:
        embed.add_field(name="Authors", value=", ".join(doujin.artists), inline=True)

    if len(doujin.groups) != 0:
        embed.add_field(name="Groups", value=", ".join(doujin.groups), inline=True)

    if doujin.cover != "":
        embed.set_image(url=doujin.cover)

    embed.set_footer(text = "Enjoy!")
    return embed

def checkPattern(message, pattern):
    '''
    Check if there's a pattern in a message

    Example:
    "uwogh" is in "UWWWWWOOOGGGGH"
    but not
    "UWOOHHGGG"
    but yes
    "Understand world organization grandpa yeet"
    '''

    index = 0
    check = 0
    for i in message:
        if i == pattern[index]:
            check += 1
            index += 1
        
        if check == len(pattern):
            return True
    return False
    
def in_oneWord(message):
    '''
    Checks if the pattern is in one word
    
    Example:
    not "Understand world organization grandpa yeet"
    yes "UnderstandWorldOrganizationGrandpaYeet"
    '''

    for i in message.split():
        if checkPattern(i, "uwogh"):
            return True
    return False

def get_proxy():
    '''
    Gets a random working free proxy that works with HTTPS from free-proxy-list.net

    It works by scraping the website and getting the list of proxies available and checks one by one
    which one can connect to nhentai.net
    '''


    from bs4 import BeautifulSoup
    import requests


    try:
        requests.get("https://nhentai.net")
        return {}
    except Exception:
        # Find available free proxy
        soup = BeautifulSoup(requests.get("https://free-proxy-list.net").text, 'lxml')
        table = list(soup.find("table", class_ = "table table-striped table-bordered").thead.find_next_sibling().children)

        print("Getting a working proxy server..")
        for i in table:
            https = i.find("td", class_ = "hx").text
            if https == "yes":
                proxy = ":".join(map(lambda ip : ip.text, i.select("td")[:2]))
                try:
                    result = requests.get("https://nhentai.net", proxies={"https" : "https://"+proxy})
                except Exception:
                    print("Failed. Retrying..")
                    continue
                if result.status_code == 200:
                    break

        print("Connected to:", proxy)
        proxyDict = {
                    "http"  : "http://"+proxy, 
                    "https" : "https://"+proxy, 
                    }
        return proxyDict

# Login to Instagram

def instagram_login():
    '''
    Logs into instagram and save the cookies
    '''


    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import pickle

    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])


    load_dotenv()
    driver = webdriver.Chrome(executable_path=r"src\instagram\chromedriver.exe", options=opt)
    driver.get("https://www.instagram.com/")

    username = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    password.clear()
    username.send_keys(os.getenv("ig_username"))
    password.send_keys(os.getenv("ig_password"))
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Save Info')]"))).click()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Turn On')]"))).click()

    pickle.dump(driver.get_cookies() , open(r"src\instagram\cookies.pkl", "wb"))

def ig_post_embed(profile, post, start_time: float):
    '''
    Gets the embed form of a Post instance
    '''
    
    
    if post:
        if post.media_type == "image":
            embed = discord.Embed(title=profile.username, url=post.url, color=0xFF5733)
            embed.set_image(url=post.media)
            embed.add_field(name="Caption:", value=post.caption, inline=False)
            embed.set_footer(text="Uploaded: "+post.upload_date+"\nExecution time: "+str((time.time() - start_time)))
            return embed

        elif post.media_type == "video":
            embed = discord.Embed(title=profile.username, url=post.url, color=0xFF5733)
            embed.add_field(name="Caption:", value=post.caption, inline=False)
            embed.set_footer(text="Uploaded: "+post.upload_date+"\nExecution time: "+str((time.time() - start_time)))
            return embed
    else:
        return -1