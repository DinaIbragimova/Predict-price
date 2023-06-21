import requests
from geopy.distance import geodesic
import csv

def get_kindergartens(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        (
            node["amenity"="kindergarten"](around:{radius},{latitude},{longitude});
            way["amenity"="kindergarten"](around:{radius},{latitude},{longitude});
            relation["amenity"="kindergarten"](around:{radius},{latitude},{longitude});
        );
        out;
    """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                    count += 1
                else:
                    count += 1
                    print(element)
        else:
            print("В указанном радиусе не найдено садиков.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_schools(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    amenities = ['school', 'college', 'university']
    amenity_query = "|".join(amenities)
    overpass_query = f"""
        [out:json];
        (
            node["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
            way["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
            relation["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
        );
        out;
    """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    count += 1
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    count += 1
        else:
            print("В указанном радиусе не найдено учебных заведений.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_foods(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    amenities = ['cafe', 'restaurant', 'fast_food', 'pub', 'bar']
    amenity_query = "|".join(amenities)
    overpass_query = f"""
        [out:json];
        (
            node["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
            way["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
            relation["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
        );
        out;
    """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    count += 1
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    count += 1
        else:
            print("В указанном радиусе не найдено точек общественного питания.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_bus(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        (
            node["highway"="bus_stop"](around:{radius},{latitude},{longitude});
            way["highway"="bus_stop"](around:{radius},{latitude},{longitude});
            relation["highway"="bus_stop"](around:{radius},{latitude},{longitude});
        );
        out;
    """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            bus_points = []
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    bus_points_name = element['tags']['name']
                    bus_points.append(bus_points_name)
            count = len(list(set(bus_points)))
        else:
            print("В указанном радиусе не найдено автобусных остановок.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_healthcare(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    amenities = ['hospital', 'dentist', 'doctors', 'clinic', 'pharmacy']
    amenity_query = "|".join(amenities)
    overpass_query = f"""
            [out:json];
            (
                node["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
                way["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
                relation["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
            );
            out;
        """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    count += 1
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
            else:
                count += 1
        else:
            print("В указанном радиусе не найдено мед.учреждений.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_parking(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
                [out:json];
                (
                    node["amenity"="parking"](around:{radius},{latitude},{longitude});
                    way["amenity"="parking"](around:{radius},{latitude},{longitude});
                    relation["amenity"="parking"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                    count += 1
                else:
                    print("нет название")
                    count += 1
        else:
            print("В указанном радиусе не найдено парковок.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_leisure(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
                [out:json];
                (
                    node["leisure"](around:{radius},{latitude},{longitude});
                    way["leisure"](around:{radius},{latitude},{longitude});
                    relation["leisure"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    print("нет название")
                count += 1
        else:
            print("В указанном радиусе не найдено объектов досуга.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_shops(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
                [out:json];
                (
                    node["shop"](around:{radius},{latitude},{longitude});
                    way["shop"](around:{radius},{latitude},{longitude});
                    relation["shop"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    print("нет название")
                count += 1
        else:
            print("В указанном радиусе не найдено магазин.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_sports(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
                [out:json];
                (
                    node["sport"](around:{radius},{latitude},{longitude});
                    way["sport"](around:{radius},{latitude},{longitude});
                    relation["sport"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    print("нет название")
                count += 1
        else:
            print("В указанном радиусе не найдено спортивных объектов.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_historic(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
                [out:json];
                (
                    node["historic"](around:{radius},{latitude},{longitude});
                    way["historic"](around:{radius},{latitude},{longitude});
                    relation["historic"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    print("нет название")
                count += 1
        else:
            print("В указанном радиусе не найдено исторических объектов.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_tourism(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
                [out:json];
                (
                    node["tourism"](around:{radius},{latitude},{longitude});
                    way["tourism"](around:{radius},{latitude},{longitude});
                    relation["tourism"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    print("нет название")
                count += 1
        else:
            print("В указанном радиусе не найдено туристических объектов.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_banks(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    amenities = ['bank', 'atm']
    amenity_query = "|".join(amenities)
    overpass_query = f"""
                [out:json];
                (
                    node["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
                    way["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
                    relation["amenity"~"{amenity_query}"](around:{radius},{latitude},{longitude});
                );
                out;
            """
    response = requests.post(overpass_url, data=overpass_query)
    count = 0
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                if 'tags' in element and 'name' in element['tags']:
                    kindergarten_name = element['tags']['name']
                    print(kindergarten_name)
                else:
                    print("нет название")
                count += 1
        else:
            print("В указанном радиусе не найдено банкоматов.")
    else:
        print("Произошла ошибка при получении данных.")
    return count

def get_bus_dist(latitude, longitude, radius):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        (
            node["highway"="bus_stop"](around:{radius},{latitude},{longitude});
        );
        out;
    """
    response = requests.post(overpass_url, data=overpass_query)
    min_distance = 3
    if response.status_code == 200:
        data = response.json()
        if 'elements' in data:
            for element in data['elements']:
                stop_latitude = element['lat']
                stop_longitude = element['lon']
                distance = geodesic((latitude, longitude), (stop_latitude, stop_longitude)).kilometers
                if distance < min_distance:
                    min_distance = round(distance, 3)
            print(min_distance)
        else:
            print("В указанном радиусе не найдено садиков.")
    else:
        print("Произошла ошибка при получении данных.")
    return min_distance

def centr_distance(latitude, longitude):
    centr_lat = 55.796127
    centr_lon = 49.106414
    distance = geodesic((latitude, longitude), (centr_lat, centr_lon)).kilometers
    print(round(distance, 3))
    return round(distance, 3)

def getLocationByAddress(address, api_key):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "format": "json",
        "apikey": api_key,
        "geocode": address,
    }
    response = requests.get(geocoder_api_server, params=params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates
    else:
        print("Ошибка выполнения запроса")
        return "-1"

def read():
    with open('cian_ads.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        count = 0
        for i in range(0, 1019):
            count += 1
            next(reader)
        # Чтение строк из CSV-файла
        for row in reader:
            # Обработка данных строки
            write(row)
            count += 1
            if count == 4472:
                break

def write(row):
    cian = row
    location_keys = ["861f27e7-5938-4024-82a5-a2ce7222a1a8", "c138d496-9b83-436e-9128-59d86fef3d59",
                     "4da0cf54-d330-419b-a512-e6a860f7c660"]
    location_index = 0
    coord = getLocationByAddress(cian[14], location_keys[location_index])
    if coord in "-1":
        location_index += 1
        if location_index > 2:
            location_index = 2
        coord = getLocationByAddress("Казань", location_keys[location_index])
    lat = coord.split(" ")[1]
    lon = coord.split(" ")[0]
    shop = get_shops(lat, lon, 500)
    bus = get_bus(lat, lon, 500)
    sport = get_sports(lat, lon, 500)
    bank = get_banks(lat, lon, 500)
    healthcare = get_healthcare(lat, lon, 500)
    parking = get_parking(lat, lon, 500)
    catering = get_foods(lat, lon, 500)
    kindergarten = get_kindergartens(lat, lon, 500)
    study = get_schools(lat, lon, 500)
    leisure = get_leisure(lat, lon, 500)
    historical = get_historic(lat, lon, 500)
    tourism = get_tourism(lat, lon, 500)
    bus_dist = get_bus_dist(lat, lon, 3000)
    centr_dist = centr_distance(lat, lon)
    row = cian + [lat, lon, shop, bus, sport, bank, healthcare, parking, catering, kindergarten, study, leisure, historical, tourism, bus_dist, centr_dist]
    with open('flats.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(row)


read()