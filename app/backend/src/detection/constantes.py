import cv2


MARKER_SIZE_M = 0.165 # Размер маркера
ARUCO_PARAM = cv2.aruco.DetectorParameters()
FRAME_SHAPE = [640, 480]
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # набор маркеров
