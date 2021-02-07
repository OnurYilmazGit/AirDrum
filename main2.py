from imutils.video import WebcamVideoStream
from imutils.video import FPS
from detectors2 import Detectors
from tracker import Tracker
import imutils
import cv2
import time
import cProfile

#construct the argument parse and parse the arguments
vs = cv2.VideoCapture(2, cv2.CAP_V4L2)

vs.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
# Create Object Detector
detector = Detectors()

# Create Object Tracker
tracker = Tracker(160, 30, 5, 20)

# Variables initialization
skip_frame_count = 10
track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                (0, 255, 255), (255, 0, 255), (255, 127, 255),
                (127, 0, 255), (127, 0, 127)]
prevTime = 0
# Infinite loop to process video frames

hihat = cv2.imread('hihatt.png')
hihat = cv2.resize(hihat,(130,210))
h_height, h_width, _ = hihat.shape
#h_height, h_width, _ = hihat.shape
snare = cv2.imread('snare.png')
snare = cv2.resize(snare,(130,110))
s_height, s_width, _ = snare.shape
bass = cv2.imread('bass.png')
bass = cv2.resize(bass,(130,110))
b_height, b_width, _ = bass.shape


while(True):
    # Capture frame-by-frame
    retreval, frame = vs.read()
    frame = imutils.resize(frame, width=960)
    print(frame.shape)
    # Make copy of original frame
    # orig_frame = copy.copy(frame)

    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1 / (sec)
    FPS = "FPS: %0.1f" % fps
# Skip initial frames that display logo

# cv2.circle(frame, (300,300), 50, (0, 255, 0), 2)
    #cv2.rectangle(frame, (10, 220), (140, 330), (0, 255, 0), 2)
    #frame[220:220+b_height, 10:10+b_width] = bass
    #cv2.rectangle(frame, (235, 220), (365, 330), (0, 255, 0), 2)
    #frame[220:220+s_height, 235:235+s_width] = snare
# Detect and return centeroids of the objects in the frame
    #cv2.rectangle(frame, (460, 120), (590, 330), (0, 255, 0), 2)
    #frame[120:120 + h_height, 460:460 + h_width] = hihat
    
    centers = detector.Detect(frame)

# If centroids are detected then track them
    if (len(centers) > 0):
        # Track object using Kalman Filter
        tracker.Update(centers)

        # For identified object tracks draw tracking line
        # Use various colors to indicate different track_id
        for i in range(len(tracker.tracks)):
            if (len(tracker.tracks[i].trace) > 1):
                for j in range(len(tracker.tracks[i].trace) - 1):
                    # Draw trace line
                    x1 = tracker.tracks[i].trace[j][0][0]
                    y1 = tracker.tracks[i].trace[j][1][0]
                    x2 = tracker.tracks[i].trace[j + 1][0][0]
                    y2 = tracker.tracks[i].trace[j + 1][1][0]
                    clr = tracker.tracks[i].track_id % 9
                    cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                             track_colors[clr], 2)
                    # ID definition for evey single object
                    #cv2.putText(frame,"ID = " + str(i),(int((x2 + x1) / 2),int((y2 + y1) / 2)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                    # print(*Id_Pool)
    # FPS printer

    cv2.line(frame,(0,200),(960,200),[0,255,0],2)
    cv2.line(frame,(0,580),(960,580),[0,255,0],2)
    cv2.putText(frame, str(FPS), (220, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
    # Display the resulting tracking frame
    cv2.imshow('Tracking', frame)

    # Display the original frame
    # cv2.imshow('Original', orig_frame)

    # Check for key strokes
    k = cv2.waitKey(1) & 0xff
# When everything done, release the capture

cv2.destroyAllWindows()

