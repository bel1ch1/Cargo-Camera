import cv2
import pickle
import numpy as np

from .constantes import MARKER_SIZE_M, ARUCO_PARAM

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


# Поиск позиции
def pose_esitmation(frame, arucoDict, valid_X, valid_Y):
    """Возвращает значение отклонения от set_valid_area и дистанцию"""

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Ищем маркеры
    corners, _, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=ARUCO_PARAM)

    # если нашли
    if corners:

        # Определяем сдвиг
        _ , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, MARKER_SIZE_M, cam_mat, dist_coef
        )

        # Определяем дистанцию до маркера
        distance_to_marker = np.linalg.norm(tvec)

        # координаты X c отклонение от допустимого значения
        c1X = corners[0][0][0][0] - valid_X
        c2X = corners[0][0][1][0] - valid_X
        c3X = corners[0][0][2][0] - valid_X
        c4X = corners[0][0][3][0] - valid_X

        # координаты Y c отклонение от допустимого значения
        c1Y = valid_Y - corners[0][0][0][1]
        c2Y = valid_Y - corners[0][0][1][1]
        c3Y = valid_Y - corners[0][0][2][1]
        c4Y = valid_Y - corners[0][0][3][1]

        # дистанция
        d = distance_to_marker

        # Вывод в консоль
        print(
            f"{c1X, c1Y}, {c2X, c2Y}, {c3X, c3Y}, {c4X, c4Y}, \ndistance: {d}"
            )
        # Возврат значений
        return f"1:{c1X, c1Y}, 2:{c2X, c2Y}, 3:{c3X, c3Y}, 4:{c4X, c4Y}, \ndistance: {d}"


# калибровка позици отсчета координат
def calibrate_centered_marker(cap, arucoDict) -> list:
    """Находит координаты отцентрованного маркера.
    Возвращает найденные координаты"""

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
        calibrate = True # Статус
        corner_X = corners[0][0][0][0] # Первый угол по X
        corner_Y = corners[0][0][0][1] # Первый угол по Y

        return[calibrate, corner_X, corner_Y]


# Установка границ допустимых координат
def set_valid_area(valid_area_param: int ,calibrate_status, corner_X, corner_Y) -> list:
    """ Устанавливает допустимую область отклонения маркера"""
    if calibrate_status:
        valid_X = corner_X+valid_area_param
        valid_Y = corner_Y+valid_area_param
        return [valid_X, valid_Y]
    else:
        return None
