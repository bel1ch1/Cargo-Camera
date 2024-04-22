import cv2
import pickle
import numpy as np

from constantes import MARKER_SIZE_M, ARUCO_PARAM

# Подгружаем данные для определения дистанции
with open('calibration_params//dist.pkl', 'rb') as f:
    dist_coef = pickle.load(f)

with open('calibration_params//cameraMatrix.pkl', 'rb') as g:
    cam_mat = pickle.load(g)


# пока не использовал
def center_coords() -> list:
    """Изменяет точку отсчета координат"""
    center_X = None
    center_Y = None
    return [center_X, center_Y]


# Поиск позиции (Главная)
def pose_esitmation(
        frame, arucoDict, valid_Left_X, valid_Right_X, valid_Left_Y, valid_Right_Y
    ):
    """Возвращает значение отклонения от точек set_valid_area и дистанцию"""

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Ищем маркеры
    corners, _, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=ARUCO_PARAM)

    # если нашли
    if corners:

        # Определяем сдвиг
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, MARKER_SIZE_M, cam_mat, dist_coef
        )

        # Определяем дистанцию до маркера
        distance_to_marker = np.linalg.norm(tvec)



        # координаты маркера по X
        c1X = corners[0][0][0][0]# - valid_Left_X  # отклоненние от левой
        c3X = corners[0][0][2][0]# - valid_Right_X # отклоненние от правой
        # координаты маркера по Y
        c1Y = corners[0][0][0][1]  # отклоненние от верхней
        c3Y = corners[0][0][2][1] # отклоненние от нижний
        # дистанция
        d = distance_to_marker


        cv2.drawFrameAxes(frame, cam_mat, dist_coef, rvec, tvec, 0.1, 4)

        # Допустимая зона
        if valid_Left_X <= c1X and c3X <= valid_Right_X:
            x_coords = "in an valid area"
        if valid_Left_Y <= c1Y and c3Y <= valid_Right_Y:
            y_coords  = "in an valid area"

        # Другие случаи
        if c1X < valid_Left_X or c3X > valid_Right_X:
            x_coords = "not in an valid area"
        if c1Y < valid_Left_Y or c3Y > valid_Right_Y:
            y_coords = "not in an valid area"


        # Вывод в консоль
        print(
            f"X: {x_coords}, Y: {y_coords}, \ndistance: {d}"
        )
        # Возврат значений
        return f"1:{c1X, c1Y}, 3:{c3X, c3Y}, \ndistance: {d}"


# калибровка позици отсчета координат (Для set_valid_area)
def get_centered_marker(cap, arucoDict) -> list:
    """Находит координаты отцентрованного маркера.
    Возвращает статус получения координат, найденные координаты:
    [cb_status, L_X, R_X, L_Y, R_Y]"""

    # Проверяем, успешно ли открыта веб-камера
    if not cap.isOpened():
        return None

    # Захватываем один кадр с веб-камеры
    ret, frame = cap.read()

    # Проверяем, успешно ли получен кадр
    if not ret:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Ищем маркеры
    corners, _, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=ARUCO_PARAM)

    # если нашли
    if corners:
        cb_status = True # Статус
        corner_L_X = corners[0][0][0][0] # Первый угол по X
        corner_L_Y = corners[0][0][0][1] # Первый угол по Y
        corner_R_X = corners[0][0][2][0] # Третий угол по X
        corner_R_Y = corners[0][0][2][1] # Третий угол по Y
        return[cb_status, corner_L_X, corner_R_X, corner_L_Y, corner_R_Y]


# Установка границ допустимых координат (Для главной)
def set_valid_area(valid_area_param: int ,cb_status, L_X, R_X, L_Y, R_Y) -> list:
    """ Устанавливает допустимую область отклонения маркера.
    Возвращает координаты от которых считается отклонение:
    [valid_L_X, valid_R_X, valid_L_Y, valid_R_Y]"""

    if cb_status:
        valid_L_X = L_X - valid_area_param
        valid_L_Y = L_Y - valid_area_param
        valid_R_X = R_X + valid_area_param
        valid_R_Y = R_Y + valid_area_param
        return [valid_L_X, valid_R_X, valid_L_Y, valid_R_Y]
    else:
        return None
