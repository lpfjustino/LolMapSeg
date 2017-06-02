import cv2 as cv
import numpy as np

import urllib3
import requests

from PIL import Image
from io import StringIO

def read_map(curr_map, left='False'):
    map_res = [200, 200]
    map = cv.imread(curr_map, cv.IMREAD_COLOR)[-map_res[0]:,:map_res[1],:]
    #map = np.float32(map)

    #map = cv.imread(curr_map, cv.IMREAD_GRAYSCALE)[-map_res[0]:,:map_res[1]]
    base_map = cv.imread('images/base_map.png', cv.IMREAD_COLOR)

    map = cv.cvtColor(map, cv.COLOR_BGR2GRAY)
    map = cv.equalizeHist(map)

    circles = cv.HoughCircles(map,cv.HOUGH_GRADIENT,1,20,param1=50,param2=13,minRadius=11,maxRadius=13)

    map = cv.cvtColor(map, cv.COLOR_GRAY2RGB)
    print(circles)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(map, (i[0], i[1]), i[2], (0, 255, 0), 2)

    cv.imshow('Map', map)
    cv.waitKey(0)


def fetch_images(champion_names):
    for champion_name in champion_names:
        url = "http://ddragon.leagueoflegends.com/cdn/7.11.1/img/champion/"+champion_name+".png"
        r = requests.get(url)
        cv.imshow('Map', r.text)
        cv.waitKey(0)


def fetch_champions():
    url = "https://br1.api.riotgames.com/lol/static-data/v3/champions?api_key=RGAPI-b3a0e588-5085-43cc-8778-bb2394a4541d"
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-b3a0e588-5085-43cc-8778-bb2394a4541d",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    champs = dict(r.json()['data'])
    champ_names = []
    for champ in champs:
        champ_names.append(champs[champ]['name'])

    return champ_names

curr_map = 'images/img1.png'
#read_map(curr_map)

champions = fetch_champions()
images = fetch_images(champions)





