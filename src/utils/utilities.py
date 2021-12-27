import os

from dotenv import load_dotenv

def get_cogs(folder):
    subfolders = [file.path for file in os.scandir(folder) if file.is_dir()]
    paths = [os.listdir(path) for path in subfolders]
    cogs = []
    for folders in paths:
        for file in folders:
            if file.endswith("cog.py"):
                cogs.append(file)
    return cogs

def checkPattern(message, pattern):
    '''
    Check if there's a pattern in a message

    This function is explicitly used by `in_oneWord` function

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
    
def in_oneWord(message, pattern):
    '''
    Checks if the pattern is in one word
    
    Example:
    not "Understand world organization grandpa yeet"
    yes "UnderstandWorldOrganizationGrandpaYeet"
    '''

    for i in message.split():
        if checkPattern(i, pattern):
            return True
    return False

def get_proxy():
    '''
    Gets a random working free proxy that works with HTTPS from free-proxy-list.net

    It works by scraping free-proxy-list.net and getting the list of proxies available and checks one by one
    and checks which one works with https and can connect to nhentai.net
    '''

    from bs4 import BeautifulSoup
    import requests

    try: # if nhentai.net is blocked
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