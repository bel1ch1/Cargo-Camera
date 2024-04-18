import cv2

from detection import pose_esitmation,\
    get_centered_marker, set_valid_area
from constantes import ARUCO_DICT


# Инициализируем камеру
cap = cv2.VideoCapture(0)


# Калибруем позицию отсчета координат
cb_pos = []
while not cb_pos:
    ret, frame= cap.read()
    if ret:
        cv2.imshow('cb', frame)
        k = cv2.waitKey(10) & 0xff
        if k == ord('s'):
            cb_pos = get_centered_marker(cap, ARUCO_DICT)
    else:
        break
cv2.destroyAllWindows()


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
    output=pose_esitmation(frame, ARUCO_DICT, valid_area[0], valid_area[1], valid_area[2], valid_area[3])

    # Вывод кадров
    cv2.imshow("Output", frame)

    # Остановка
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()
