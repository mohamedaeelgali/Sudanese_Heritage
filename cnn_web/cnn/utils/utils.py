import boto3
import cv2
import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)


def remove_background(img, blur=21, canny_thresh_1=10, canny_thresh_2=100,
                      mask_dilate_iter=10, mask_erode_iter=10, mask_color=(0.0,0.0,1.0)):
    """
    img: RGB image (numpy array) for which we want to remove the background
    """
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, canny_thresh_1, canny_thresh_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)
    
    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    _, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    
    mask = np.zeros(edges.shape)
    for c in contour_info:
        cv2.fillConvexPoly(mask, c[0], (255))
    
    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=mask_dilate_iter)
    mask = cv2.erode(mask, None, iterations=mask_erode_iter)
    mask = cv2.GaussianBlur(mask, (blur, blur), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask
    
    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending
    
    masked = (mask_stack * img) + ((1-mask_stack) * mask_color) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 
    
    # split image into channels
    c_red, c_green, c_blue = cv2.split(img)
    
    #replace background with white color when mask == 1    
    mask_normalized = mask.astype('float32') / 255.0
    c_red[mask_normalized<0.01]=1
    c_green[mask_normalized<0.01]=1
    c_blue[mask_normalized<0.01]=1
    
    return cv2.merge((c_red, c_green, c_blue))