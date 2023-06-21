import csv
import datetime
import re
from itertools import product
import requests
import cfscrape
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

CITY = {
    'name': 'ekb',
    'cian_region': 4743
}

MAX_PAGE = 55
BASE_URL = 'https://{city_name}.cian.ru/cat.php?region={cian_region}&{tale}'.format(
    city_name=CITY['name'],
    cian_region=CITY['cian_region'],
    tale='deal_type=sale&engine_version=2&object_type%5B0%5D=1&offer_type=flat&p={page}&room{room_type}=1'
)
ROOM_TYPES = {
    1: (1, '1-комнатная'),
    2: (2, '2-комнатная'),
    3: (3, '3-комнатная'),
    4: (4, '4-комнатная'),
    5: (5, '5-комнатная'),
    6: (6, '6-комнатная'),
    9: (0, 'студия'),
}

scraper = cfscrape.create_scraper()


class NoMorePagesException(Exception):
    pass


def scrape_page(url):
    response = scraper.get(url)

    page_soup = BeautifulSoup(response.content, 'lxml')
    offers = page_soup.select('div[data-name="LinkArea"] a[href*="/flat/"]')
    offers_links = [offer['href'] for offer in offers]
    return offers_links


def str_square_to_float(str_square):
    return float(str_square.replace('м²', '').replace(',', '.').strip())


def scrape_offer(url):
    response = scraper.get(url)

    offer_soup = BeautifulSoup(response.content, 'lxml')
    return offer_soup


def parse_offer(offer_soup):
    print("start parse_offer")
    price: str = offer_soup.select_one('span[itemprop="price"]')['content']
    price_value = int(price.replace(' ', '')[:-1])  # ex.: '2 700 000 ?' -> 2700000

    desc_block = offer_soup.find('div', attrs={"data-name": "ObjectSummaryDescription"}).select(
        'div[data-testid="object-summary-description-info"]')
    flat_desc_dict = {}
    for index, element in enumerate(desc_block):
        title = element.select_one('div[data-testid="object-summary-description-title"]')
        value = element.select_one('div[data-testid="object-summary-description-value"]')
        flat_desc_dict[title.text] = value.text
    flat_square = flat_desc_dict.get('Общая')
    flat_square_value = str_square_to_float(flat_square) if flat_square else ''

    flat_live_square = flat_desc_dict.get('Жилая')
    flat_live_square_value = str_square_to_float(flat_live_square) if flat_live_square else ''

    flat_kitchen_square = flat_desc_dict.get('Кухня')
    flat_kitchen_square_value = str_square_to_float(flat_kitchen_square) if flat_kitchen_square else ''

    flat_floor = flat_desc_dict.get('Этаж', '').split(' из ')
    flat_floor_value = flat_floor[0]
    total_floors_value = flat_floor[1]

    house_year_value = flat_desc_dict.get('Построен', '')

    header_information = offer_soup.find('section', attrs={"data-name": "Main"})

    residental_complex = header_information.select_one('div[data-name="Parent"] a[data-name="Link"]')
    residental_complex_value = '' if residental_complex is None else residental_complex.get_text().removeprefix('в ')

    address = header_information.select_one('address[class="a10a3f92e9--address--F06X3"]')
    address_value = ''
    street_value = ''
    district_value = ''
    microdistrict_main_value = ''
    microdistrict_local_value = ''
    flat_number_value = ''
    for index, element in enumerate(address.findChildren("a", recursive=False)):
        full_address = element.text + ", "
        if "р-н" in element.text:
            district_value = element.text.replace("р-н", "").strip()
        if "мкр" in element.text:
            microdistrict_main_value = element.text.replace("мкр.", "").strip()
        if "ул" in element.text:
            street_value = element.text.replace("ул.", "").strip()
        if "жилмассив" in element.text:
            microdistrict_local_value = element.text.replace("жилмассив", "").strip()
        if index + 1 == len(address.findChildren("a", recursive=False)):
            flat_number_value = element.text
            full_address = element.text
        address_value += full_address

    general_information_block = offer_soup.find('div', attrs={"data-name": "GeneralInformation"})
    home_info = general_information_block.select_one('article[data-name="AdditionalFeaturesGroup"]')
    flat_type_value = ''
    flat_toilet_value = ''
    flat_repair_value = ''
    flat_ceiling_value = ''
    flat_window_view_value = ''
    flat_balcony_value = ''
    for index, element in enumerate(home_info.findChildren("li", recursive=True)):
        title = element.select_one('span[class="a10a3f92e9--name--x7_lt"]')
        value = element.select_one('span[class="a10a3f92e9--value--Y34zN"]')
        if title.text in "Тип жилья":
            flat_type_value = value.text
        if title.text in "Санузел":
            flat_toilet_value = value.text
        if title.text in "Балкон/лоджия":
            flat_balcony_value = value.text
        if title.text in "Ремонт":
            flat_repair_value = value.text
        if title.text in "Высота потолков":
            flat_ceiling_value = value.text.replace(',', '.').replace('м', '').strip()
        if title.text in "Вид из окон":
            flat_window_view_value = value.text

    house_data_block = offer_soup \
        .find('div', attrs={"data-name": "BtiHouseData"}) \
        .find('div', attrs={"class": "a10a3f92e9--column--XINlk"})
    home_info = house_data_block.select('div[data-name="Item"]')
    house_type_value = ''
    flat_gas_value = ''
    flat_floor_type_value = ''
    flat_entrances_value = ''
    flat_lifts_value = ''
    flat_heating_value = ''
    flat_garbage_value = ''
    flat_parking_value = ''
    for index, element in enumerate(home_info):
        title = element.select_one('div[class="a10a3f92e9--name--pLPu9"]')
        value = element.select_one('div[class="a10a3f92e9--value--G2JlN"]')
        if title.text in "Тип дома":
            house_type_value = value.text
        if title.text in "Тип перекрытий":
            flat_floor_type_value = value.text
        if title.text in "Подъезды":
            flat_entrances_value = value.text
        if title.text in "Лифты":
            flat_lifts_value = value.text
        if title.text in "Отопление":
            flat_heating_value = value.text
        if title.text in "Мусоропровод":
            flat_garbage_value = value.text
        if title.text in "Газоснабжение":
            flat_gas_value = value.text
        if title.text in "Парковка":
            flat_parking_value = value.text

    return {
        'price': price_value,
        'total_square': flat_square_value,  # стоимость квартиры
        'live_square': flat_live_square_value,
        'kitchen_square': flat_kitchen_square_value,
        'floor': flat_floor_value,
        'total_floors': total_floors_value,
        'residental_complex': residental_complex_value,
        'district': district_value,
        'flat_number': flat_number_value,
        'street': street_value,
        'microdistrict_main': microdistrict_main_value,
        'microdistrict_local': microdistrict_local_value,
        'full_address': address_value,
        'flat_type': flat_type_value,
        'toilet': flat_toilet_value,
        'balcony': flat_balcony_value,
        'repair_status': flat_repair_value,
        'window_view': flat_window_view_value,
        'ceiling': flat_ceiling_value,
        'house_type': house_type_value,
        'house_year': house_year_value,
        'lifts': flat_lifts_value,
        'parking': flat_parking_value,
        'gas': flat_gas_value,
        'floor_type': flat_floor_type_value,
        'entrances': flat_entrances_value,
        'heating': flat_heating_value,
        'garbage': flat_garbage_value,
    }


def init_parsing(file_name=None, yield_rows=False):
    timer_start = datetime.datetime.now()
    flats_hashes = set()
    for room_type in ROOM_TYPES.keys():
        for page_number in range(1, MAX_PAGE):
            page_timer_start = datetime.datetime.now()
            offers_data = {}
            try:
                page_offers_links = scrape_page(BASE_URL.format(page=page_number, room_type=room_type))
                print('Got offers on page {}, room_type {}'.format(page_number, room_type))
            except NoMorePagesException:
                print('[NMP]: Skip page {} for room_type {}'.format(page_number, room_type))
                break
            for link in page_offers_links:
                offers_data[link] = scrape_offer(link)
            for offer_id, offer_data in offers_data.items():
                try:
                    flat_info = parse_offer(offer_data['soup'])
                except Exception as e:
                    print('[DNG] Exception during parsing. ', e)
                    continue

                flat_hash = '{}{}{}{}{}{}'.format(
                    flat_info['total_square'],
                    offer_data['room_type'],
                    flat_info['floor'],
                    flat_info['district'],
                    flat_info['microdistrict_main'],
                    flat_info['street'],
                    flat_info['flat_number']
                )
                if flat_hash in flats_hashes:
                    print('[DOUBLE] Skip offer saving')
                    continue
                flats_hashes.add(flat_hash)

                row = [
                    flat_info['price'],  # стоимость квартиры
                    flat_info['room_type'],  # количество комнат
                    flat_info['total_square'],  # общая площадь
                    flat_info['live_square'],   # жилая площадь
                    flat_info['kitchen_square'],  # площадь кухни
                    flat_info['floor'],  # этаж, на котором расположена квартира
                    flat_info['total_floors'],  # количество этажей в доме
                    flat_info['residental_complex'],  # жилой комплекс
                    flat_info['district'],  # район, в котором находится квартира
                    flat_info['flat_number'],  # номер квартиры
                    flat_info['street'],  # улица
                    flat_info['microdistrict_main'],   # микрорайон
                    flat_info['microdistrict_local'],   # жилмассив
                    flat_info['full_address'],  # полный адрес дома
                    flat_info['flat_type'],  # тип жилья (вторичка / первичка)
                    flat_info['toilet'],  # количество и типы санузлов
                    flat_info['balcony'],  # количество балконов и/или лоджий
                    flat_info['repair_status'],  # тип ремонта
                    flat_info['window_view'],   # вид из окна
                    flat_info['ceiling'],  # высота потолков
                    flat_info['house_type'],  # тип дома
                    flat_info['house_year'],  # год постройки
                    flat_info['lifts'],  # количество и типы лифтов в доме
                    flat_info['parking'],  # тип парковки
                    flat_info['gas'],   # тип газоснабжения
                    flat_info['floor_type'],  # тип перекрытий
                    flat_info['entrances'],  # номер подъезда
                    flat_info['heating'],  # тип отопления
                    flat_info['garbage'],  # мусоропровод
                ]
                if file_name:
                    with open(file_name, 'a', newline='', encoding='utf - 8') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(row)

                if yield_rows:
                    yield row

                print('[I] Batch has been parsed and saved.')


def main():
    current_time = datetime.datetime.now()
    file_stamp = current_time.strftime('%Y%m%d_%H%M')
    file_name = 'cian_flats_{}.csv'.format(file_stamp)
    # file_name = 'cian_flats_20230522_0200.csv'

    # with open(file_name, 'w', newline='', encoding='utf-8') as flats_file:
    #     flats_writer = csv.writer(flats_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     flats_writer.writerow([
    #         'ID',
    #         'Price',
    #         'Rooms',
    #         'Views',
    #         'Square',
    #         'Live Square',
    #         'Kitchen',
    #         'Floor',
    #         'Total Floors',
    #         'Residental Complex',
    #         'District',
    #         'Flat number',
    #         'Street',
    #         'Microdistrict',
    #         'Microistrict 2',
    #         'Full address',
    #         'Flat Type',
    #         'Toilet',
    #         'Balcony',
    #         'Repair',
    #         'Window View',
    #         'Ceiling',
    #         'House Type',
    #         'House Year',
    #         'Lifts',
    #         'Parking',
    #         'Gas',
    #         'Floor_type',
    #         'Entrances',
    #         'Heating',
    #         'Garbage',
    #     ])
    timer_start = datetime.datetime.now()
    flats_hashes = set()
    for room_type in range(6, 7):
        for page_number in range(26, 55):
            page_timer_start = datetime.datetime.now()
            offers_data = {}
            try:
                page_offers_links = scrape_page(BASE_URL.format(page=page_number, room_type=room_type))
                print('Got offers on page {}, room_type {}'.format(page_number, room_type))
            except NoMorePagesException:
                print('[NMP]: Skip page {} for room_type {}'.format(page_number, room_type))
                break
            for link in page_offers_links:
                if "pdf" in link:
                    continue
                offers_data[link] = scrape_offer(link)
            for offer_id, offer_data in offers_data.items():
                print(offer_id)
                try:
                    flat_info = parse_offer(offer_data)
                    if not (len(flat_info['microdistrict_main']) > 1 and len(flat_info['window_view']) > 1):
                        continue
                except Exception as e:
                    print('[DNG] Exception during parsing. ', e)
                    continue

                flat_hash = '{}{}{}{}{}'.format(
                    flat_info['total_square'],
                    room_type,
                    flat_info['floor'],
                    flat_info['flat_number'],
                    flat_info['full_address'],
                )
                if flat_hash in flats_hashes:
                    print('[DOUBLE] Skip offer saving')
                    continue
                flats_hashes.add(flat_hash)

                row = [
                    offer_id,
                    flat_info['price'],
                    room_type,
                    flat_info['total_square'],
                    flat_info['live_square'],
                    flat_info['kitchen_square'],
                    flat_info['floor'],
                    flat_info['total_floors'],
                    flat_info['residental_complex'],
                    flat_info['district'],
                    flat_info['flat_number'],
                    flat_info['street'],
                    flat_info['microdistrict_main'],
                    flat_info['microdistrict_local'],
                    flat_info['full_address'],
                    flat_info['flat_type'],
                    flat_info['toilet'],
                    flat_info['balcony'],
                    flat_info['repair_status'],
                    flat_info['window_view'],
                    flat_info['ceiling'],
                    flat_info['house_type'],
                    flat_info['house_year'],
                    flat_info['lifts'],
                    flat_info['parking'],
                    flat_info['gas'],
                    flat_info['floor_type'],
                    flat_info['entrances'],
                    flat_info['heating'],
                    flat_info['garbage'],
                ]
                if file_name:
                    with open(file_name, 'a', newline='', encoding='utf - 8') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(row)

                print('[I] Batch has been parsed and saved.')


if __name__ == '__main__':
    main()
