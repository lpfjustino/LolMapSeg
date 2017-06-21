import cv2

import numpy as np

from matplotlib import pyplot as plt
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
    map = cv2.imread(curr_map, cv2.IMREAD_COLOR)[-map_res[0]:,:map_res[1],:]

    gs_map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
    gs_map = cv2.equalizeHist(gs_map)

    circles = cv2.HoughCircles(gs_map,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=13,minRadius=9,maxRadius=13)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(map, (i[0], i[1]), i[2], (0, 255, 0), 2)

    cv2.imshow('Map', map)
    cv2.waitKey(0)

    return circles[0,:,:2], map

'''
    Legacy function that used Hough circles to find the champions
'''
def find_champions(map, circles, all_champs):
    # cv2.imshow('mapa', map)
    # cv2.waitKey(0)

    res = 12
    for circle in circles:
        # 1 and 0 because the circles' centers are respectively y and x
        candidate = map[circle[1]-res:circle[1]+res, circle[0]-res:circle[0]+res]
        candidate = circular_crop_map(candidate)
        diffs = []

        # cv2.imshow('a',candidate)
        # cv2.waitKey(0)
        for i, champ in enumerate(all_champs):
            # cv2.imshow('a',champ['crop'])
            # cv2.waitKey(0)

            gs_champ = cv2.cvtColor(champ['crop'], cv2.COLOR_BGR2GRAY)
            gs_candidate = cv2.cvtColor(candidate, cv2.COLOR_BGR2GRAY)

            champ_hist = cv2.calcHist([gs_champ],[0],None,[256],[0,256])
            candidate_hist = cv2.calcHist([gs_candidate],[0],None,[256],[0,256])

            err = cv2.compareHist(champ_hist, candidate_hist,cv2.HISTCMP_CHISQR)

            diffs.append(err)

        print('>',min(diffs))
        i = np.argmin(diffs)
        print(all_champs[i]['name'])

'''
    Uses template matching in order to identify the champions' portraits
'''
def read_map(curr_map, all_champions, left='False'):
    map_res = [200, 200]
    map = cv2.imread(curr_map, cv2.IMREAD_COLOR)[-map_res[0]:,:map_res[1],:]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    # methods = ['cv2.TM_CCOEFF']

    w = 24
    h = 24

    for meth in methods:
        for i, champ in enumerate(all_champs):
            print(champ['name'])
            template = champ['crop']
            img = map.copy()
            method = eval(meth)
            # Apply template Matching
            res = cv2.matchTemplate(img, template, method)
            print(res.shape)
            print(np.where(res >= 0.8))
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv2.rectangle(img, top_left, bottom_right, 255, 2)

            plt.subplot(121), plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(img)
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth + ' - ' + champ['name'])
            # plt.show()

            im_name = meth + "_" + champ['name'] + ".png"
            cv2.imwrite(im_name, img)


def circular_crop_champ(image_name):
    image = cv2.imread(image_name, cv2.IMREAD_COLOR)
    radius = int(image.shape[0]/2)

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if (x-radius) ** 2 + (y-radius) ** 2 > radius ** 2:
                image[x, y, :] = 0

    image = cv2.resize(image, (0, 0), fx=1/5, fy=1/5)

    # cv2.imshow('ch', image)
    # cv2.waitKey(0)

    return image

def circular_crop_map(candidate):
    image = candidate
    radius = int(image.shape[0]/2) # Ignores 1 px  radius to reduce error from the border

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if (x-radius) ** 2 + (y-radius) ** 2 > radius ** 2:
                image[x, y, :] = 0

    # cv2.imshow('ch', image)
    # cv2.waitKey(0)

    return image




def load_champions_images():
    all_champs = fetch_champions()
    # all_champs = ['Soraka', 'Fiora', 'Ahri', 'Graves', 'Brand', 'Alistar', 'Nautilus']
    all_champs = ['Alistar']
    base = []

    for champ in all_champs:
        crop = circular_crop_champ('images/champs/' + champ + '.png')
        base.append({'name': champ, 'crop': crop})

    return base

curr_map = 'images/tst.png'
# curr_map = 'images/img1.png'

# Hough test
# circles, map = read_map(curr_map)
# find_champions(map, circles, all_champs)
# find_champions(map, circles, all_champs)

all_champs = load_champions_images()

read_map(curr_map, all_champs)

# Champion images fetching
# champions = fetch_champions()
# images = fetch_images(champions)





