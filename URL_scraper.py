import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Beautiful Soup Module required.  Attempting to install using pip.")
    try:
        import pip
        pip.main(['install', bs4])
    except Exception as e:
        print(e)
        print("Pip module not found!  Please go to https://www.crummy.com/software/BeautifulSoup/#Download to install Beautiful Soup Module.")

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