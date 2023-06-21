import requests
from bs4 import BeautifulSoup
import cfscrape
import re

session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123',
    'Accept-Language': 'ru',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}
def getCoords(flat_page):
    coords = flat_page.find('div', attrs={'class':'map_info_button_extend'}).contents[1]
    coords = re.split('&amp|center=|%2C', str(coords))
    coords_list = []
    for item in coords:
        if item[0].isdigit():
            coords_list.append(item)
    lat = float(coords_list[0])
    lon = float(coords_list[1])
    print(lat)
    print(lon)
    return lat, lon

def str_square_to_float(str_square):
    return float(str_square.replace('м²', '').replace(',', '.').strip())

def scrape_page():
    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    response = scraper.get("https://kazan.cian.ru/sale/flat/286890103/")
    page_soup = BeautifulSoup(response.content, 'lxml')
    desc_block = page_soup.find('div', attrs={"data-name": "ObjectSummaryDescription"}).select('div[data-testid="object-summary-description-info"]')
    flat_desc_dict = {}
    for index, element in enumerate(desc_block):
        title = element.select_one('div[data-testid="object-summary-description-title"]')
        value = element.select_one('div[data-testid="object-summary-description-value"]')
        flat_desc_dict[title.text] = value.text
scrape_page()