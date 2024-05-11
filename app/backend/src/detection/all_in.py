import cv2
import pickle




######################### CONSTANTES #################################################
# Папаметры нахождения маркера
ARUCO_PARAM = cv2.aruco.DetectorParameters()
# Словарь маркеров
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
######################################################################################




######################## PARAMETERS ##################################################
marker_size_M = 0.165
######################################################################################




####################### CAMERA PARAMETERS ############################################
# Подгружаем данные для определения дистанции
with open('calibration_params//dist.pkl', 'rb') as f:
    dist_coef = pickle.load(f)

with open('calibration_params//cameraMatrix.pkl', 'rb') as g:
    cam_mat = pickle.load(g)
######################################################################################




####################### ENTITYS ######################################################
cap = cv2.VideoCapture(0)
######################################################################################




####################### MAIN LOOP ####################################################
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Серый трешхолд для матрицы кадра
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Нахождение маркера
        corners, ids, _ = cv2.aruco.detectMarkers(gray, ARUCO_DICT, ARUCO_PARAM)
        if corners:
            # Вектора положения
            rvec, tvec = cv2.aruco.estimatePoseSingleMarkers(
                corners, marker_size_M, cam_mat, dist_coef
            )
            # Вывод
            # Отколонение от центра по X
            X_coord = tvec[0][0][0]
            # Отколонение от центра по Y
            Y_xoord = tvec[0][0][1]
            # Дистанция от камеры до маркера
            distance_to_marker = tvec[0][0][2]
    else:
        print("Not found")
######################################################################################
