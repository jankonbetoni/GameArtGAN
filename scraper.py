from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread, Lock
import collections
import datetime
import time
import os
import pathlib
import requests
import subprocess

images  = []
img_num = 0
workers = 20
threads = []
tasks   = Queue()
lock    = Lock()

def welcome_message():
    now = datetime.datetime.now()
    today = now.strftime("%A • %B %e • %H:%M • %Y")
    print('\n  DeviantArt Scraper')
    print('\n  DATE:  ' + today)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r"./chromedriver")
    return driver

def get_username(d):
    global username
    html = d.page_source
    soup = BeautifulSoup(html, 'html.parser')
    username = soup.find(class_='gruserbadge').find('a').get_text()

def get_thumb_links():
    d = get_driver()
    #d.get('https://www.deviantart.com/popular-all-time/?q=32x32&offset=0')
    d.get('https://www.deviantart.com/popular-all-time/?q=32x32&offset=14880')
    unique_img = scroll_page_down(d)
    time.sleep(0.5)
    for img in unique_img:
        print(img)
    #global expected_img_num
    #expected_img_num = str(len(unique_img))
    #get_username(d)
    #print('  Unique images found = ' + expected_img_num)
    #print('  Artist = ' + username + "\n")
    time.sleep(0.5)
    d.close()

def scroll_page_down(d):
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height

    last_height = d.execute_script("return document.body.scrollHeight")
    counter = 14748
    downloaded = set()
    while True:
        # Scroll down to bottom

        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page

        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height

        new_height = d.execute_script("return document.body.scrollHeight")
        # Get the tumbnail image links

        im = d.find_element_by_class_name('page-results')
        links = im.find_elements_by_class_name('torpedo-thumb-link')
        print(links)
        h = {'User-Agent': 'Firefox'}
        s = requests.Session()
        for link in links:
            img = link.find_element_by_css_selector('img')
            #print('img')
            #print(img)
            l = img.get_attribute('src')
            if l in downloaded:
              continue
            downloaded.add(l)
            #images.append(l)
            #print(l)
            req = s.get(l, headers=h)
            time.sleep(0.1)
            download_now(req, str(counter))
            counter += 1
        # Remove duplicates

        unique_img = list(set(images))
        time.sleep(0.5)
        # Break when the end is reached

        if new_height == last_height:
            break
        last_height = new_height
    return unique_img


def get_full_image(l):
    s = requests.Session()
    h = {'User-Agent': 'Firefox'}
    soup = BeautifulSoup(s.get(l, headers=h).text, 'html.parser')
    title = ''
    link = ''
    try:
        link = soup.find('a', class_='dev-page-download')['href']
    except TypeError:
        try:
            link = soup.find('img', class_='dev-content-full')['src']
            title = soup.find('a',
                                 class_='title').text.replace(' ', '_').lower()
        except TypeError:
            try:
                link = age_restricted(l)
            except (WebDriverException, AttributeError):
                link = age_restricted(l)
        pass
    req = s.get(link, headers=h)
    time.sleep(0.1)
    download_now(req,title)
    # Return tuple

    url = req.url
    ITuple = collections.namedtuple('ITuple', ['u', 't'])
    it = ITuple(u=url, t=title)
    return it

def name_format(url, title):
    if url.find('/'):
        #name =  url.rsplit('/', 1)[1]
        #p1 = name.split('-')[0]
        p2 = url.split('.')[-1]
        if len(p2) > 5:
          if '.png' in p2:
            p2 = 'png'
          elif '.gif' in p2:
            p2 = 'gif'
        name = title + '.' + p2
    return name

def download_now(req,title):
    url = req.url
    name = name_format(url,title)
    pathlib.Path('{}.deviantart.com'.format('pixels')).mkdir(parents=True, exist_ok=True)
    with open(os.path.join('{}.deviantart.com/'.format('pixels'), '{}'.format(name)),'wb') as file:
        file.write(req.content)

def save_img(url):
    try:
        with open('{}-gallery.txt'.format(username), 'a+') as file:
            file.write(url + '\n')
    except:
        print('An write error occurred.')
        pass

def worker_thread(q, lock):
    while True:
        link = q.get()
        if link is None:
            break
        p = get_full_image(link)
        url = p.u
        title = p.t
        name = name_format(url, title)
        with lock:
            global img_num
            img_num += 1
            save_img(url)
            print('Image ' + str(img_num) + ' - ' + name)
        q.task_done()

def main():
    welcome_message() # Display Welcome Message
    get_thumb_links()
		

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()

