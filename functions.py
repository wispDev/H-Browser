#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from bs4 import BeautifulSoup
from requests import get

OPERATIONS = {
    'search_results': '[+] Gathering search results...',
    'parse_results': '[+] Parsing...',
    'search_episodes': '[+] Retreiving available episodes...',
}

# Initialize driver and return it
def init_driver(url):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    sleep(3)

    return driver

def driver_quit(driver):
    driver.quit()

def search(driver, key_word):

    print(OPERATIONS['search_results'])

    search_bar = driver.find_element_by_id('s')
    search_bar.clear()
    search_bar.send_keys(key_word)
    
    search_button = driver.find_element_by_class_name('search-button')
    search_button.click()
    sleep(3)

    return driver    

def get_search_results(driver):

    print(OPERATIONS['parse_results'])

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('div', class_='result-item')

    titles, links = list(), list()
    
    for r in results:
        title_div = r.find('div', class_='title')
        title = title_div.find('a').string
        link = title_div.find('a', href=True)
        
        titles.append(title)
        links.append(link['href'])

    driver.quit()
    return titles, links

def get_episodes(driver):

    print(OPERATIONS['search_episodes'])

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    posters = soup.findAll('div', class_='season_m animation-4')

    episodes, e_links = list(), list()

    for p in posters:
        episode_num = p.find('span', class_="c").get_text()
        link = p.find('a', href=True)

        episodes.append(episode_num)
        e_links.append(link['href'])

    driver.quit()
    return episodes, e_links

def get_video_url(driver):
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    container = soup.findAll('iframe', class_="metaframe rptss")
    url = container[0]['src']

    print(f"[+] Target URL found: {url}")

    return url

def get_video(driver):
    html = driver.page_source
    driver.quit()
    
    status = True

    soup = BeautifulSoup(html, 'html.parser')
    body_tag = soup.find('body')
    video_tag = body_tag.find('video')
    
    try:
        video_source = video_tag.find('source')['src']
    except KeyError:
        video_source = video_tag['src']
    except TypeError:
        video_source = video_tag['src']
    except AttributeError:
        print("[x] Video is currently unavailable...")
        status, video_source = False, None
    
    if status:
        print(f"[+] Target media found: {video_source}")
    
    return video_source, status

def download_video(url, series, episode):
    print(f"[+] Downloading {series}: {episode}...")

    r = get(url)
    file_name = f"{series}_{episode}.mp4"

    try:
        with open(file_name, 'wb') as vid:
            vid.write(r.content)
    except:
        print("[x] Write failed...")
    finally:
        vid.close()
    
    if r.status_code == '200':
        print("[+] Download Successful!")
    else:
        print(f"[x] Download failed! | Status Code: {r.status_code}")
    
    sleep(3)


    
    
    



