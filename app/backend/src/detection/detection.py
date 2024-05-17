import pickle

from cv2 import cvtColor, COLOR_BGR2GRAY
from cv2.aruco import DetectorParameters, getPredefinedDictionary, detectMarkers,\
    estimatePoseSingleMarkers, DICT_4X4_50

marcer_size_M = 0.165


# Подгружаем данные для определения дистанции
with open('calibration_params//dist.pkl', 'rb') as f:
    dist_coef = pickle.load(f)

with open('calibration_params//cameraMatrix.pkl', 'rb') as g:
    cam_mat = pickle.load(g)


ARUCO_PARAM = DetectorParameters()
ARUCO_DICT = getPredefinedDictionary(DICT_4X4_50)


def pose_of_container(frame, marker_size_M, ARUCO_DICT=ARUCO_DICT, ARUCO_PARAM=ARUCO_PARAM):
    """Возваращает отклонение контейнера от центра (X, Y, Distance)"""
    # Серый трешхолд для матрицы кадра
    gray = cvtColor(frame, COLOR_BGR2GRAY)
    # Нахождение маркера
    corners, _, _ = detectMarkers(gray, dictionary=ARUCO_DICT, parameters=ARUCO_PARAM)
    if corners:
        # Вектора положения
        _, tvec, _ = estimatePoseSingleMarkers(
            corners, markerLength=(marker_size_M/1000), cameraMatrix=cam_mat, distCoeffs=dist_coef
        )

        # Отколонение от центра по X
        X_coord = tvec[0][0][0]
        # Отколонение от центра по Y
        Y_xoord = tvec[0][0][1]
        # Дистанция от камеры до маркера
        distance_to_marker = tvec[0][0][2]
        return X_coord, Y_xoord, distance_to_marker
    else:
        return None
