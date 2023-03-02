import calc_time as ct
import requests
from bs4 import BeautifulSoup
import excel_logic as ex
import time
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

ct.start_time

# ua = UserAgent()
# userAgent = ua.random
# print(userAgent)

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
browser = webdriver.Chrome(options=chrome_options)

url = 'https://www.google.com/search?q=site%3A%22myshopify.com%22+intext%3A%22camping+gear%22&oq=site%3A%22myshopify.com%22+intext%3A%22camping+gear%22'

excel_file_to_be_saved = "camping_gear.xlsx"

browser.get(url)

soup = BeautifulSoup(browser.page_source, 'html.parser')

error = 'Our systems have detected unusual traffic from your computer network'

if error in soup.text:
    time.sleep(20)
    browser.refresh()
    # browser.get(url)
    # soup = BeautifulSoup(browser.page_source, 'html.parser')


def getSingleNicheData(url):
    page = requests.get(url)
    newSoup = BeautifulSoup(page.content, 'html.parser')

    brandName = newSoup.find(
        'meta', attrs={'property': 'og:site_name'})['content']

    instagram = newSoup.findAll('a', attrs={'href': True})

    for i in instagram:
        if 'instagram' in i['href']:
            instagram = i['href']
            break

    print(brandName, instagram)


totalPagesIndex = 1

for i in range(20):
    browser.get(url+'&start='+str(i*10))
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # singlePageData = soup.findAll('cite', attrs={'role': 'text'})
    singlePageData = soup.findAll(
        'div', attrs={'class': 'yuRUbf'})

    # remove duplicates
    singlePageData = list(dict.fromkeys(singlePageData))

    singlePageIndex = 1
    for data in singlePageData:
        data = data.find('a', attrs={'href': True})['href']
        # remove data after .com
        # data = data.text.split('.com')[0]
        print(data)
        # brandName, instagram = getSingleNicheData(data)

        singleEntry = [data]

        index = 1
        for entry in singleEntry:
            ex.ws.cell(row=totalPagesIndex + 1, column=index,
                       value=entry)
            index += 1

        totalPagesIndex += 1

    time.sleep(10)


ex.wb.save(excel_file_to_be_saved)

# print(singlePageData)

ct.calc_total_time()
