import cv2
import pickle

from .detection import pose_esitmation, center_coords


# Подгружаем данные для определения дистанции
with open('calibration_params//dist.pkl', 'rb') as f:
    dist_coef = pickle.load(f)

with open('calibration_params//cameraMatrix.pkl', 'rb') as g:
    cam_mat = pickle.load(g)


# Константы
MARKER_SIZE_M = 0.165 # Размер маркера
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # набор маркеров
FRAME_SHAPE = [640, 480]

arucoParam = cv2.aruco.DetectorParameters()

cap = cv2.VideoCapture(0)
while True:

    success, frame = cap.read()

    if not success:
        break

    # Получаем центр координат
    center = center_coords()

    # Вывод координат и дистанции
    output=pose_esitmation(frame, ARUCO_DICT, center[0], center[1])

    # Вывод кадров
    cv2.imshow("Output", frame)

    # Остановка
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
