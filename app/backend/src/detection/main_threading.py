import threading
import asyncio
import cv2
import pickle
import uvicorn
from fastapi import FastAPI, Request, WebSocketDisconnect, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from websockets.exceptions import ConnectionClosed


####################### PARSING ######################################################
# Подгружаем данные для определения дистанции
with open('calibration_params//dist.pkl', 'rb') as f:
    dist_coef = pickle.load(f)

with open('calibration_params//cameraMatrix.pkl', 'rb') as g:
    cam_mat = pickle.load(g)
######################################################################################


####################### VAR ##########################################################
marker_size_M = 0.165
######################################################################################


####################### CONSTS #######################################################
ARUCO_PARAM = cv2.aruco.DetectorParameters()
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
######################################################################################


####################### DETECTION FUNC ###############################################
def pose_of_container(frame, marker_size_M, ARUCO_DICT=ARUCO_DICT, ARUCO_PARAM=ARUCO_PARAM):
    """Возваращает отклонение контейнера от центра (X, Y, Distance)"""
    # Серый трешхолд для матрицы кадра
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Нахождение маркера
    corners, _, _ = cv2.aruco.detectMarkers(gray, dictionary=ARUCO_DICT, parameters=ARUCO_PARAM)
    if corners:
        # Вектора положения
        _, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
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
######################################################################################



####################### THREAD - API #################################################
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Отправляем в браузер HTML
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Метод меняющий переменную размера маркера
@app.post('/set_marker_size')
async def set_new_marker_size(size: float):
    global marker_size_M
    marker_size_M = size
    return {'message' : 'Marker size is updated'}


# @app.websocket("/ws")
# async def video_feed(websocket: WebSocket):
#     """
#     Обработчик WebSocket, который отправляет кадры c камеры.
#     """
#     await websocket.accept()
#     try:
#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break
#             else:
#                 _, buffer = cv2.imencode('.jpg', frame)
#                 await websocket.send_bytes(buffer.tobytes())
#             await asyncio.sleep(0.05)  # Задержка для снижения нагрузки на сервер
#     except (WebSocketDisconnect, ConnectionClosed):
#         print('disconnected')
#     finally:
#         cap.release()
#         RedirectResponse("/")


def run_api():
    uvicorn.run(app, host='127.0.0.1', port=8000)
######################################################################################





####################### THREAD - DETECTION ###########################################
def detection():
    # Ининциализируем камеру
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        # Если получили камеру
        if ret:
            output = pose_of_container(frame, marker_size_M)
            if output != None:
                print(f"X : {output[0]}, Y : {output[1]}, distance: {output[2]}")
            else:
                print("Not found")
        else:
            print("Camera not found")
            break

        # Остановка
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    # Чистим ресуры
    cap.release()
    cv2.destroyAllWindows()
######################################################################################





####################### ENTRY POINT ##################################################
if __name__ == '__main__':
    #  Multi threading
    frame_processing_thread = threading.Thread(target=detection)
    fastapi_thread = threading.Thread(target=run_api)

    fastapi_thread.start()
    frame_processing_thread.start()

    fastapi_thread.join()
    frame_processing_thread.join()
######################################################################################
