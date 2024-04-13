import cv2
import pickle
import numpy as np


# Подгружаем данные для определения дистанции
with open('calibration_params//dist.pkl', 'rb') as f:
    dist_coef = pickle.load(f)

with open('calibration_params//cameraMatrix.pkl', 'rb') as g:
    cam_mat = pickle.load(g)


# Константы
MARKER_SIZE_M = 0.165 # Размер маркера
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) # набор маркеров
FRAME_SHAPE = [640, 480]

# Параметры
arucoParam = cv2.aruco.DetectorParameters()


def center_coords(shape = FRAME_SHAPE) -> list:
    """Изменяет точку отсчета координат"""
    center_X = FRAME_SHAPE[0] / 2
    center_Y = FRAME_SHAPE[1] / 2
    return [center_X, center_Y]



# Поиск позиции
def pose_esitmation(img, arucoDict, centerX, centerY):
    """Возвращает координаты углов маркера и дистанцию до него"""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Ищем маркеры
    corners, _, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    # если нашли
    if corners:

        # Определяем сдвиг
        _ , tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, MARKER_SIZE_M, cam_mat, dist_coef)

        # Определяем дистанцию до маркера
        distance_to_marker = np.linalg.norm(tvec)

        # координаты X
        c1X = corners[0][0][0][0] - centerX
        c2X = corners[0][0][1][0] - centerX
        c3X = corners[0][0][2][0] - centerX
        c4X = corners[0][0][3][0] - centerX

        # координаты Y
        c1Y = corners[0][0][0][1] - centerY
        c2Y = corners[0][0][1][1] - centerY
        c3Y = corners[0][0][2][1] - centerY
        c4Y = corners[0][0][3][1] - centerY

        # дистанция
        d = distance_to_marker

        # Вывод в консоль
        print(f"{c1X, c1Y}, {c2X, c2Y}, {c3X, c3Y}, {c4X, c4Y}, \ndistance: {d}")
        # Возврат значений
        return f"1:{c1X, c1Y}, 2:{c2X, c2Y}, 3:{c3X, c3Y}, 4:{c4X, c4Y}, \ndistance: {d}"

def calibrate_centered_marker(img, arucoDict, centerX, centerY ) -> list:
    """находит координаты отцентрованного маркера.
    Возвращает найденные координаты"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Ищем маркеры
    corners, _, _ = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    # если нашли
    if corners:
        calibrate = True
        return[calibrate, corners]


def set_valid_area(valid_area: int ,calibrate_status, **centered_corners: str):
    """У станавливает допустимую область отклонения маркера"""
    pass



# захват видео с камеры и обработка
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
