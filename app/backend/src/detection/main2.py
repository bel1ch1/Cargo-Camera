from cv2 import VideoCapture, destroyAllWindows

from constantes import ARUCO_DICT, ARUCO_PARAM
from detection import pose_of_container

cap = VideoCapture(0)

marker_size_M = 0.165

while True:
    ret, frame = cap.read()

    if ret:
        output = pose_of_container(frame, ARUCO_DICT, ARUCO_PARAM, marker_size_M)
        if output != None:
            print(f"X : {output[0]}, Y : {output[1]}, distance: {output[2]}")
        else:
            print("Not found")
    else:
        print("Camera not found")
        break

cap.release()
destroyAllWindows()
