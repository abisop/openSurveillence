import cv2 as cv
import time
import numpy as np

#globals
flag = 0    
divided_frame = []
segments = 4
pass_frame = [0] * segments
mean_array = [0] * segments
index = [0] * segments

def divide_frame(frame, num_rows, num_cols):
    height, width = frame.shape
    part_height = height // num_rows
    part_width = width // num_cols

    parts = []
    for row in range(num_rows):
        for col in range(num_cols):
            start_row = row * part_height
            end_row = (row + 1) * part_height
            start_col = col * part_width
            end_col = (col + 1) * part_width

            part = frame[start_row:end_row, start_col:end_col]
            parts.append(part)

    return parts

def passing_a_frame(frame):           # it passes frame for further processing
     
     divided_frame = divide_frame(frame,2,2)
     for i in range(len(divided_frame)):
        pass_frame[i] = cv.mean(divided_frame[i])
        mean_array[i] = np.array(pass_frame[i][:3])
        
        if mean_array[i][0] > 0.2:
            index[i] = 1
        else:
            index[i] = 0    
     return index , mean_array

def input_camera_stream(port):
    frame2 = 0
    cap = cv.VideoCapture(port)
    pass_flag = 1
    # Initialize variables
    alpha = 0.8  # Weight for current frame
    beta = 0.2   # Weight for previous frame
    prev_frame = None
    
    threshold_value = 125

    k = 1
    while True:
        ret, orignal_frame = cap.read()
        frame = orignal_frame
        #to grayscale
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Initialize prev_frame if it's the first frame
        if prev_frame is None:
            prev_frame = frame_gray
            continue

        result = cv.addWeighted(frame_gray, alpha, prev_frame, beta, 0)

        _, frame = cv.threshold(result, threshold_value, 255, cv.THRESH_BINARY)

        result = cv.absdiff(frame, frame2)
        result = cv.medianBlur(result,15)
        
        cv.imshow('real',result)
 
        frame2=frame
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        #print(result.shape)

        index, mean = passing_a_frame(result)

        for i in range (segments - 1 ):
            if( index[i] == 1):
                pass_flag = 1
                t = time.time()
            elif((time.time() - t) > 10):
                pass_flag = 0

            if (pass_flag == 1):
                cv.imshow('frame',orignal_frame)

        #functions for further processing if ((((( pass_flag == 1  ))))))
    cap.release()
    cv.destroyAllWindows()


def main():  # processing in this node
    input_camera_stream(1)
    

main()
