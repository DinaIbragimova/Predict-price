import csv
from math import cos, radians
from geopy.distance import distance
from geopy import Point
import pandas as pd
from sklearn.linear_model import LinearRegression

import requests

def read(fileName):
    with open(fileName, 'r') as file:
        file.readline()
        write("dataset.csv", file.readlines())

# запись данных в файл
def write(fileName, rows):
    with open(fileName, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in rows:
            elements = row.split(";")
            if elements[19] == "":
                continue
            lon, lat = getLocationByAddress(handleAddress(elements[19], elements[20])).split(" ")
            school = getPlacesByCoords(lon, lat, "школа")
            kindergarten = getPlacesByCoords(lon, lat, "садик")
            supermarket = getPlacesByCoords(lon, lat, "магазин")
            clinic = getPlacesByCoords(lon, lat, "поликлиника")
            pharmacy = getPlacesByCoords(lon, lat, "аптека")
            bus_stop = getPlacesByCoords(lon, lat, "автобусная остановка")
            cafe = getPlacesByCoords(lon, lat, "кафе")
            park = getPlacesByCoords(lon, lat, "парк")
            parking = getPlacesByCoords(lon, lat, "парковка")
            bank = getPlacesByCoords(lon, lat, "банк")
            if lat != "-1" and school != "-1" and kindergarten != "-1" and supermarket != "-1" and clinic != "-1" and\
                    pharmacy != "-1" and bus_stop != "-1" and cafe != "-1" and park != "-1" and parking != "-1" and bank != "-1":
                new_row = [elements[2], elements[3], elements[6], elements[7], elements[8], elements[9], elements[10], elements[11], elements[12], elements[13], elements[14],
                           elements[16], elements[17], elements[18], elements[19], elements[20], lat, lon, school, kindergarten, supermarket, clinic, pharmacy, bus_stop, cafe, park, parking, bank]
                writer.writerow(new_row)

def handleAddress(address, residential_complex):
    if "Республика Татарстан" in address or "Казань" in address:
        new_address = address
    else:
        if residential_complex != "":
            new_address = f"Казань, {residential_complex}"
        else:
            new_address = f"Казань, {address}"
    return new_address

def getLocationByAddress(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    api_key = "4da0cf54-d330-419b-a512-e6a860f7c660"
    params = {
        "geocode": address,
        "format": "json",
        "apikey": api_key,

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


def getPlacesByCoords(lon, lat, search_type):
    api_key = "AIzaSyAvLY-w84YIouQbqxNAR3XZ7OqBXwIvp2c"  # израсходовано
    radius = 500
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&keyword={search_type}&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        count = 0
        for result in data["results"]:
            count += 1
            name = result["name"]
            address = result["vicinity"]
            print(name, address)
        return f"{count }"
    else:
        print("Ошибка выполнения запроса")
        return "-1"

def read2(fileName):
    with open(fileName, 'r') as file:
        file.readline()
        write("dataset2.csv", file.readlines())

# запись данных в файл
def write2(fileName, rows):
    with open(fileName, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in rows:
            elements = row.split(";")
            lon = elements[17]
            lat = elements[16]
            school = if getPlacesByCoords(lon, lat, "лицей") == 0:
                
            kindergarten = getPlacesByCoords(lon, lat, "садик")
            supermarket = getPlacesByCoords(lon, lat, "магазин")
            clinic = getPlacesByCoords(lon, lat, "поликлиника")
            pharmacy = getPlacesByCoords(lon, lat, "аптека")
            bus_stop = getPlacesByCoords(lon, lat, "автобусная остановка")
            cafe = getPlacesByCoords(lon, lat, "кафе")
            park = getPlacesByCoords(lon, lat, "парк")
            parking = getPlacesByCoords(lon, lat, "парковка")
            bank = getPlacesByCoords(lon, lat, "банк")
            if lat != "-1" and school != "-1" and kindergarten != "-1" and supermarket != "-1" and clinic != "-1" and\
                    pharmacy != "-1" and bus_stop != "-1" and cafe != "-1" and park != "-1" and parking != "-1" and bank != "-1":
                new_row = [elements[2], elements[3], elements[6], elements[7], elements[8], elements[9], elements[10], elements[11], elements[12], elements[13], elements[14],
                           elements[16], elements[17], elements[18], elements[19], elements[20], lat, lon, school, kindergarten, supermarket, clinic, pharmacy, bus_stop, cafe, park, parking, bank]
                writer.writerow(new_row)



# read("cian_parsing_result_sale_11_56_kazan_20_Apr_2023_16_39_21_810164.csv")

getPlacesByCoords(49.183992, 55.793202, "")