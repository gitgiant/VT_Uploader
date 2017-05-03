import requests
from bs4 import BeautifulSoup
import uploader

def scrape_URLS(URL):
    response = requests.get(URL)
    # parse html
    page = BeautifulSoup(response.content, "lxml")

    links = page.find_all('a')

    # Go through every found link and upload
    for tag in links:
        link = tag.get('href',None)
        if link is not None:
            uploader.upload_URL(link)

    # Upload the page itself
    uploader.upload_URL(URL)