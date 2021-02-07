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
tom_flag = True
crash_flag = True
rigth_crash_flag = True
last10_frame_of_y_axis = [0] * 15
low_green = np.asarray([[36, 40, 35]])
high_green = np.asarray([82, 255, 255])
last20_frame_of_X_axis_hihat = [0] * 25
last60_frame_of_X_axis_crash = [0] * 20
last40_frame_of_Y_axis_snare = [0] * 480
last20_frame_of_Y_axis_kick = [0] * 10
last20_frame_of_X_axis_rigth_crash = [0] * 20
last50_frame_of_X_axis_tom = [0] * 30


hihat = cv2.imread('hihatt.png')
hihat = cv2.resize(hihat,(120,180))
h_height, h_width, _ = hihat.shape
snare = cv2.imread('snare.png')
snare = cv2.resize(snare,(160,120))
s_height, s_width, _ = snare.shape
bass = cv2.imread('bass.png')
bass = cv2.resize(bass,(130,110))
b_height, b_width, _ = bass.shape
ride = cv2.imread('ride.jpg')
ride = cv2.resize(ride,(130,210))
r_height, r_width, _ = ride.shape


class Detectors(object):
    def __init__(self):

        return None

    #listenin icinde dahha kuck bir sayi varsa true yoksa false donecek/ 
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
        	return 1

    def record_last20_frame_hihat(self,x_axsis):
    	self.x_axsis = x_axsis
    	last20_frame_of_X_axis_hihat.append(self.x_axsis)
    	last20_frame_of_X_axis_hihat.pop(0)
    	print(*last20_frame_of_X_axis_hihat)
    	return last20_frame_of_X_axis_hihat


    def record_last60_frame_crash(self,x1_axsis):
    	self.x1_axsis = x1_axsis
    	last60_frame_of_X_axis_crash.append(self.x1_axsis)
    	last60_frame_of_X_axis_crash.pop(0)
    	print(*last60_frame_of_X_axis_crash)
    	return last60_frame_of_X_axis_crash

    def record_last50_frame_tom(self,x3_axsis):
    	self.x3_axsis = x3_axsis
    	last50_frame_of_X_axis_tom.append(self.x3_axsis)
    	last50_frame_of_X_axis_tom.pop(0)
    	print(*last50_frame_of_X_axis_tom)
    	return last50_frame_of_X_axis_tom

    def record_last30_frame_rigth_crash(self,x2_axsis):
    	self.x2_axsis = x2_axsis
    	last20_frame_of_X_axis_rigth_crash.append(self.x2_axsis)
    	last20_frame_of_X_axis_rigth_crash.pop(0)
    	print(*last20_frame_of_X_axis_rigth_crash)
    	return last20_frame_of_X_axis_rigth_crash

    def record_last40_frame_snare(self,y_axsis):
    	self.y_axsis = y_axsis
    	last40_frame_of_Y_axis_snare.append(self.y_axsis)
    	last40_frame_of_Y_axis_snare.pop(0)
    	print(*last40_frame_of_Y_axis_snare)
    	return last40_frame_of_Y_axis_snare

    def record_last20_frame_kick(self,y1_axsis):
    	self.y1_axsis = y1_axsis
    	last20_frame_of_Y_axis_kick.append(self.y1_axsis)
    	last20_frame_of_Y_axis_kick.pop(0)
    	print(*last20_frame_of_Y_axis_kick)
    	return last20_frame_of_Y_axis_kick

    def sound_volume(self,num):
        self.num = float(num)
        self.num2 = 0

        #if(float(num) <= 1.7):
         #   num2 = 4
        #elif(float(num) <= 2.4 and float(num) > 1.7):
         #   num2 = 3
        #elif(float(num) <= 3.0 and float(num) > 2.4):
        #    num2 = 2
        #elif(float(num) <= 3.4 and float(num) > 3.0):
        #    num2 = 1
        return 4

    def Detect(self, frame):
        global snare_flag
        global kick_flag
        global hihat_flag
        global crash_flag
        global rigth_crash_flag
        global tom_flag
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
                        if(int(y) > 585):
                        	self.record_last20_frame_kick(int(y))
                        	print("KICKKKK Y CENTER", self.record_last20_frame_kick(int(y)))
                        	if((int(x) > 280 and int(x) < 960) and (self.check_number(last20_frame_of_Y_axis_kick,645) == False)):
                        		print("PAT PAT")
                        		print("KICK CENTERRRR", int(x), int(y))
                        		if(kick_flag == True):
                        			kick_flag = False
                        			drumsounds.play_kick(self.record_last10_frame(int(y)))
                        			frame[600:600+b_height, 765:765+b_width] = bass
                        		elif(kick_flag == False):
                        			kick_flag = True
                        elif((int(y) > 250 and int(y) < 550)):
                        	self.record_last20_frame_hihat(int(x))
                        	if((int(x) > 600) and (self.check_number(last20_frame_of_X_axis_hihat,600) == False)):
                        		print("HIHAT HIHATTTT ")
                        		print("HIHATTTT CENTERRRR", int(x), int(y))
                        		if(hihat_flag == True):
                        			hihat_flag == False
                        			drumsounds.play_ride(self.record_last10_frame(int(y)))
                        			frame[300:300 + r_height, 695:695 + r_width] = ride
                        		elif(hihat_flag == False):
                        			hihat_flag == True
                        #elif((int(y) > 240 and int(y) < 550) and (int(x) < 330)):
                        #	#self.record_last50_frame_tom(int(x))
                        #	print("TOM PATTTT ")
                        #	print("TOM CENTERRRR", int(x), int(y))
                        #	if(tom_flag == True):
                        #		tom_flag == False
                        #		drumsounds.play_tom(0)
                        #	elif(tom_flag == False):
                        #		tom_flag == True	                        					
                        elif((int(y) > 505 and int(y) < 578)):	
                        	#self.record_last40_frame_snare(int(y))
                        	print("SNAREEE", self.record_last40_frame_snare(int(y)))
                        	if((int(x) < 500)):
                        		print("TAKK TAKK")
                        		print("SNAREEE CENTERRRR", int(x), int(y))
                        		if(snare_flag == True):
                        			snare_flag == False
                        			drumsounds.play_snare(4)
                        			frame[510:510+s_height, 280:280+s_width] = snare
                        		elif(snare_flag == False):
                        			snare_flag == True
                        elif((int(y) < 170)):
                        	self.record_last60_frame_crash(int(x))
                        	print("LEFT CRASHHHH", self.record_last60_frame_crash(int(y)))
                        	if((int(x) < 360) and (self.check_number(last60_frame_of_X_axis_crash,180) == False)):
                        		print("LEFT CISSS")
                        		print("CRASHHHH CENTERRRR", int(x), int(y))
                        		if(crash_flag == True):
                        			crash_flag == False
                        			drumsounds.play_crash(self.record_last10_frame(int(y)))
                        			frame[10:10 + h_height, 35:35 + h_width] = hihat
                        		elif(crash_flag == False):
                        			crash_flag == True
                        elif((int(y) < 180)):
                        	self.record_last30_frame_rigth_crash(int(x))
                        	print("Right CRASHHHH", self.record_last30_frame_rigth_crash(int(x)))
                        	if((int(x) > 320) and (self.check_number(last60_frame_of_X_axis_crash,330) == False)):
                        		print("Right CISSS")
                        		print("Right CRASHHHH CENTERRRR", int(x), int(y))
                        		if(rigth_crash_flag == True):
                        			rigth_crash_flag == False
                        			drumsounds.play_crash(0)
                        			frame[10:10 + h_height, 765:765 + h_width] = hihat
                        		elif(rigth_crash_flag == False):
                        			rigth_crash_flag == True


            except ZeroDivisionError:
                pass

        return centers
