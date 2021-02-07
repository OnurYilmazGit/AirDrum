from __future__ import print_function
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import argparse
import imutils
import cv2
import numpy as np
import time
import drumsounds
from math import sqrt

snare_flag = True
kick_flag = True
hihat_flag = True
crash_flag = True
last10_frame_of_y_axis = [0] * 15
low_green = np.asarray([[36, 40, 35]])
high_green = np.asarray([82, 255, 255])
last20_frame_of_X_axis_hihat = [0] * 100

class Detectors(object):
    def __init__(self):

        return None

    def check_number(self,list,value):
    	return(all(value < x for x in list))



    def record_last10_frame(self, y_axis):
        self.y_axis = y_axis
        last10_frame_of_y_axis.append(self.y_axis)
        last10_frame_of_y_axis.pop(0)
        sorted(last10_frame_of_y_axis, reverse=True)
        print(*last10_frame_of_y_axis)
        if(last10_frame_of_y_axis[0]-last10_frame_of_y_axis[-1] > 13):
        	#volume = (min(last10_frame_of_y_axis)/50)
        	return self.sound_volume(1)
        else:
        	return 4

    def record_last20_frame_hihat(self,x_axsis):
    	self.x_axsis = x_axsis
    	last20_frame_of_X_axis_hihat.append(self.x_axsis)
    	last20_frame_of_X_axis_hihat.pop(0)
    	print(*last20_frame_of_X_axis_hihat)
    	return last20_frame_of_X_axis_hihat


    def sound_volume(self,num):
        self.num = float(num)
        self.num2 = 0

        if(float(num) <= 1.7):
            num2 = 4
        elif(float(num) <= 2.4 and float(num) > 1.7):
            num2 = 3
        elif(float(num) <= 3.0 and float(num) > 2.4):
            num2 = 2
        elif(float(num) <= 3.4 and float(num) > 3.0):
            num2 = 1
        return self.num2

    def Detect(self, frame):
        global snare_flag
        global kick_flag
        global hihat_flag
        global crash_flag
        global last10_frame_of_y_axis
        global last20_frame_of_X_axis_hihat
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Green color

        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)
        # --
        thresh = cv2.threshold(
            green_mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Blured and applied erosions & dilations to get clear frame.
        blurred = cv2.GaussianBlur(green_mask, (11, 11), 0)
        thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=4)
        # --
        #cv2.imshow("Threshed_Ver", thresh)
        # this line can reduce noises.
        #kernel = np.ones((5, 5), np.uint8)
        #opening = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

       # #D = ndimage.distance_transform_edt(thresh)
        #localMax = peak_local_max(D, indices=False, min_distance=20,
        #                          labels=thresh)

        # perform a connected component analysis on the local peaks,
        # using 8-connectivity, then appy the Watershed algorithm
        #labels = watershed(-D, markers, mask=thresh)
        #print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        centers = []
        blob_radius_thresh = 8

        #cv2.imshow("Green_mask", green_mask)

        snare_x = 300
        snare_y = 285

        min_y = 510
        counter = 0

        # This function return sound volume number

        # to meause velocity, i recorded last 10 frame of y axis.

		
        for c in cnts:
            try:
                area = cv2.contourArea(c)
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if area > 1800:
                    x, y, w, h = cv2.boundingRect(c)
                    #cv2.putText(frame,"Area = " + str(area),(cx - 20, cy - 20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 255, 0),1)
                    print("Area: ", area)
                    print('x = ', x, 'y = ', y, 'w = ', w, 'h = ', h)
                    # Calculate and draw circle
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    centeroid = (int(x), int(y))
                    radius = int(radius)
                    cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                    print('Center Cordinates(x,y) = ', int(
                        x), ' ', int(y), 'radius = ', radius)
                    if (radius > blob_radius_thresh):
                        cv2.circle(frame, centeroid, radius, (0, 255, 0), 2)
                        b = np.asarray([[x], [y]])
                        centers.append(np.round(b))
                            #print((record_last10_frame(self, min_y)))
                        # drum setup conditions
                        if(int(y) > 640 and int(x) > 480):
                        	if(kick_flag == True):
                        		kick_flag = False
                        		drumsounds.play_kick(
                                        self.record_last10_frame(int(y)))
                        	elif(kick_flag == False):
                        		kick_flag = True
                        elif((int(y) > 220 and int(y) < 540) and (int(x) < 360)):
                        	self.record_last20_frame_hihat(int(x))
                        	if(counter==0):
                        		if(int(x) < 300):	
                        			counter = 1
                        			drumsounds.play_hi_hat(0)
                        		else:
                        			#print(check_number(self.record_last20_frame_hihat(x)),330)
                        			counter == 1

                        elif((int(y) > 360 and int(y) < 540) and (int(x) > 480 and int(x) < 660)):
                        	if(snare_flag == True):
                        		snare_flag == False
                        		drumsounds.play_snare(self.record_last10_frame(int(y)))
                        	elif(snare_flag == False):
                        		snare_flag == True
                        elif((int(y) > 0 and int(y) < 100) and (int(x) > 0 and int(x) < 320)):
                        	if(crash_flag == True):
                        		crash_flag == False
                        		drumsounds.play_crash(self.record_last10_frame(int(y)))
                        	elif(crash_flag == False):
                        		crash_flag == True	

            except ZeroDivisionError:
                pass

        return centers
