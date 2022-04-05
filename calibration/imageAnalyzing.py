# -*- coding: utf-8 -*-
"""
@author: srica
"""

import cv2 as cv
import numpy as np

import constants

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) * SQUARE SIZE
objp = np.zeros((constants.NX*constants.NY, 3), np.float32)
objp[:, :2] = np.mgrid[0:constants.NX, 0:constants.NY].T.reshape(-1, 2)
objp = objp * constants.SQUARE_SIZE

def getPoints():
    objpoints, imgpoints = ([] for i in range(2))
    
    for imgName in constants.IMAGES:
        img = cv.imread(imgName)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
        # find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (constants.NX, constants.NY), None)
        
        # if found add object and image points
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
            cornersFound = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), constants.CRITERIA)
            
            # draw the corners and show image
            cv.drawChessboardCorners(img, (constants.NX, constants.NY), cornersFound, True)
            img = cv.resize(img, (0, 0), fx = constants.SHRINK, fy = constants.SHRINK)
            #cv.imshow(imgName, img)
        else:
            print("No pattern found on " + imgName)
            
    # q or esc to exit all windows
    #cv.waitKey()
    #cv.destroyAllWindows()
    
    return objpoints, imgpoints

     
def getCameraVlaues(objpoints, imgpoints):
    # if at least 1 image is considered   
    if objpoints:
        # get random image
        img = cv.imread('a52s/viber_image_2022-03-27_19-11-37-526.jpg')
        h,  w = img.shape[:2]
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        # get camera intrinsic and extrinsic parameters
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print("Camera matrix: {}".format(mtx))
        print("Distortion matrix: {}".format(dist))
        #print("Rotation matrix: {}".format(rvecs))
        #print("Translation matrix: {}".format(tvecs))
        
        return mtx, dist, rvecs, tvecs