import cv2

from .detection import pose_esitmation,\
    get_centered_marker, set_valid_area

from .constantes import ARUCO_DICT


# Инициализируем камеру
cap = cv2.VideoCapture(0)

# Калибруем позицию отсчета координат
cb_pos = get_centered_marker(cap, ARUCO_DICT)

# Устанавливаем границы допустимых координат
valid_area = set_valid_area(1, cb_pos[0], cb_pos[1], cb_pos[2], cb_pos[3], cb_pos[4])


# Цыкл работы основного модуля
while cap.isOpened():

    # Читаем кадр с камеры
    success, frame = cap.read()

    # Проверка на принятия кадра
    if not success:
        break

    # Вывод координат и дистанции
    output=pose_esitmation(frame, ARUCO_DICT)

    # Вывод кадров
    cv2.imshow("Output", frame)

    # Остановка
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
