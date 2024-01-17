#cv prebuilt lib
#---------------------------------------------------------------------------------------------------------------
from ultralytics import YOLO
model = YOLO("yolov8n.pt")

import cv2
cap = cv2.VideoCapture("D:/murdering/uccrime_Shooting002_x264.mp4")
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
#---------------------------------------------------------------------------------------------------------------



#lib for auto data analysis
#--------------------------------------------------
from sklearn.linear_model import LinearRegression
from collections import deque
import statistics

max_queue_size = 100000000
my_queue = deque(maxlen=max_queue_size)

def enqueue(data):
    my_queue.append(data)

#--------------------------------------------------

#general purpose lib
#-------------------------------------------------
import csv
from time import time
import math
#-------------------------------------------------





currently_in = 0
frame_count = 0
howmanygrids = 25



while cap.isOpened():

    success, frame = cap.read()
    results = model.track(frame,persist=True,verbose=False,classes = [0],conf = 0.3)
    result = results[0]
    cv2.imshow('res',result.plot())
        
       #smoothening of people count  
#------------------------------------------------------------------------------------

    x = len(result.boxes)
    if x > currently_in:
       currently_in = x
    elif (x < currently_in) and (currently_in - x) > 0 :
       currently_in = x
#------------------------------------------------------------------------------------
       

    #managing array size acc. to people in frame
#-----------------------------------------------------------------------------   
    con = [0] * currently_in
    cord = [0] * currently_in
    centroid = [[0] * 2] * currently_in
    x_ = [0] * currently_in
    y_ = [0] * currently_in
    speed = [0] * currently_in
    grids = [[0] * 2] * currently_in
#-------------------------------------------------------------------------------
    
    for i in range(currently_in ):
        con[i] = result.boxes[i].conf
        cord[i] = result.boxes[i].xyxy
        x_[i] = (cord[i][0][2] - cord[i][0][0])
        y_[i] = (cord[i][0][3] - cord[i][0][1])

        #speed processing between this 
        centroid[i][0] =  (x_[i] / 2) + cord[i][0][2]  
        centroid[i][1] =  (y_[i] / 2) + cord[i][0][3]

#---------------------------------------------------------------------------------
        

        #crowd analysis
#---------------------------------------------------------------------------------        
        grids[i][0] = int(centroid[i][0] / howmanygrids)
        grids[i][1] = int(centroid[i][1] / howmanygrids)
#---------------------------------------------------------------------------------
        



    #eol
#---------------------------------------------------------------------------------------------        
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()


