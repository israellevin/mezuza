#!/usr/bin/python
import cv
import sys
import math
import socket
import shutil
from time import time, sleep

ACTHIGH = 10
ACTLOW = -3
PIXCOUNT = 10000
TH = 50
ADAPT = 0.96
CAMERA = 0
DISPLAY = False

# Command line options
try:
    ACTHIGH = int(sys.argv.pop(1))
    ACTLOW = int(sys.argv.pop(1)) * -1
    PIXCOUNT = int(sys.argv.pop(1))
    TH = int(sys.argv.pop(1))
    ADAPT = int(sys.argv.pop(1))
    CAMERA = int(sys.argv.pop(1))
    sys.argv.pop(1)
    DISPLAY = True
except IndexError:
    pass

print ACTHIGH, ACTLOW, PIXCOUNT, TH, ADAPT, CAMERA, DISPLAY

# Initialization
cam = cv.CaptureFromCAM(CAMERA)
img = cv.QueryFrame(cam)
while not img:
    print 'Retrying capture'
    sleep(1)
    cam = cv.CaptureFromCAM(CAMERA)
    img = cv.QueryFrame(cam)
size = width, height = cv.GetSize(img)
depth = img.depth
nchan = img.nChannels
print "Got image %s\n%iX%iX%iX%i" % (img, width, height, depth, nchan)

col = cv.CreateImage(size, depth, nchan)
avg = cv.CreateImage(size, depth, nchan)
val = cv.CreateImage(size, depth, 1)
dif = 0
act = -100

if DISPLAY:
    cv.NamedWindow('out', 0);

# Frame loop
stime = time()
framecnt = 0
while True:

    # FPS calc
    if DISPLAY:
        framecnt = framecnt + 1
        ctime = time()
        if ctime - stime >= 1:
            print '%ifps' % (framecnt)
            framecnt = 0
            stime = ctime

    # Get original image
    img = cv.QueryFrame(cam)

    # Adaptive diff
    #cv.Smooth(img, col, cv.CV_GAUSSIAN, 3, 0)
    cv.AddWeighted(img, 1 - ADAPT, avg, ADAPT, 0, avg)
    cv.AbsDiff(img, avg, col)
    cv.CvtColor(col, col, cv.CV_RGB2HSV)
    cv.Split(col, None, None, val, None)
    cv.CmpS(val, TH, val, cv.CV_CMP_GE)
    #cv.Dilate(val, val, None, 18)
    #cv.Erode(val, val, None, 10)
    dif = cv.CountNonZero(val)

    # Show image if it's radically new
    if(dif < PIXCOUNT):
        if act < 0:
            act = ACTLOW
        else:
            act -= 1
    else:
        if act > 0:
            act = ACTHIGH
        else:
            act += 1
            if act > 0:
                cv.SaveImage('/tmp/tmp.png', img);
                shutil.move('/tmp/tmp.png', "/shared/%s.png" % (time()));
                if DISPLAY:
                    cv.ShowImage('out', img)

    # Exit on escape key
    k = cv.WaitKey(20)
    if -1 != k:
        if k == 27:
            break
