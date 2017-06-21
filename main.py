import cv2 as cv
import numpy as np
from fetcher import fetch_champions

import urllib3
import requests

import shutil

import time


'''
    Legacy function that used Hough method to identify the champions' portraits
'''
def read_map_hough(curr_map, left='False'):
    map_res = [200, 200]
    map = cv.imread(curr_map, cv.IMREAD_COLOR)[-map_res[0]:,:map_res[1],:]

    gs_map = cv.cvtColor(map, cv.COLOR_BGR2GRAY)
    gs_map = cv.equalizeHist(gs_map)

    circles = cv.HoughCircles(gs_map,cv.HOUGH_GRADIENT,1,20,param1=50,param2=13,minRadius=9,maxRadius=13)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(map, (i[0], i[1]), i[2], (0, 255, 0), 2)

    cv.imshow('Map', map)
    cv.waitKey(0)

    return circles[0,:,:2], map

'''
    Uses template matching in order to identify the champions' portraits
'''
def read_map(curr_map, left='False'):
    map_res = [200, 200]
    map = cv.imread(curr_map, cv.IMREAD_COLOR)[-map_res[0]:,:map_res[1],:]

    gs_map = cv.cvtColor(map, cv.COLOR_BGR2GRAY)
    gs_map = cv.equalizeHist(gs_map)

    circles = cv.HoughCircles(gs_map,cv.HOUGH_GRADIENT,1,20,param1=50,param2=13,minRadius=9,maxRadius=13)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv.circle(map, (i[0], i[1]), i[2], (0, 255, 0), 2)

    cv.imshow('Map', map)
    cv.waitKey(0)

    return circles[0,:,:2], map



def circular_crop_champ(image_name):
    image = cv.imread(image_name, cv.IMREAD_COLOR)
    radius = int(image.shape[0]/2)

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if (x-radius) ** 2 + (y-radius) ** 2 > radius ** 2:
                image[x, y, :] = 0

    image = cv.resize(image, (0, 0), fx=1/5, fy=1/5)

    # cv.imshow('ch', image)
    # cv.waitKey(0)

    return image

def circular_crop_map(candidate):
    image = candidate
    radius = int(image.shape[0]/2) - 1 # Ignores 1 px  radius to reduce error from the border

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if (x-radius) ** 2 + (y-radius) ** 2 > radius ** 2:
                image[x, y, :] = 0

    # cv.imshow('ch', image)
    # cv.waitKey(0)

    return image

def find_champions(map, circles, all_champs):
    # cv.imshow('mapa', map)
    # cv.waitKey(0)

    res = 12
    for circle in circles:
        # 1 and 0 because the circles' centers are respectively y and x
        candidate = map[circle[1]-res:circle[1]+res, circle[0]-res:circle[0]+res]
        candidate = circular_crop_map(candidate)
        diffs = []

        # cv.imshow('a',candidate)
        # cv.waitKey(0)
        for i, champ in enumerate(all_champs):
            # cv.imshow('a',champ['crop'])
            # cv.waitKey(0)

            gs_champ = cv.cvtColor(champ['crop'], cv.COLOR_BGR2GRAY)
            gs_candidate = cv.cvtColor(candidate, cv.COLOR_BGR2GRAY)

            champ_hist = cv.calcHist([gs_champ],[0],None,[256],[0,256])
            candidate_hist = cv.calcHist([gs_candidate],[0],None,[256],[0,256])

            err = cv.compareHist(champ_hist, candidate_hist,cv.HISTCMP_CHISQR)

            diffs.append(err)

        print('>',min(diffs))
        i = np.argmin(diffs)
        print(all_champs[i]['name'])


def load_champions_images():
    all_champs = fetch_champions()
    base = []

    for champ in all_champs:
        crop = circular_crop_champ('images/champs/' + champ + '.png')
        base.append({'name': champ, 'crop': crop})

    return base

curr_map = 'images/tst.png'

circles, map = read_map(curr_map)

all_champs = load_champions_images()
# find_champions(map, circles, all_champs)
find_champions(map, circles, all_champs)
# champions = fetch_champions()
#images = fetch_images(champions)





