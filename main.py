import cv2 as cv
import numpy as np

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

curr_map = 'images/img1.png'
read_map(curr_map)