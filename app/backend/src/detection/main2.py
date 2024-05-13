import threading
import asyncio

import uvicorn
from fastapi import FastAPI, Request, WebSocketDisconnect, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from websockets.exceptions import ConnectionClosed

from cv2 import VideoCapture, destroyAllWindows, imencode
from cv2.aruco import DetectorParameters, getPredefinedDictionary, DICT_4X4_50

#from constantes import ARUCO_DICT, ARUCO_PARAM
from detection import pose_of_container

ARUCO_PARAM = DetectorParameters()
ARUCO_DICT = getPredefinedDictionary(DICT_4X4_50)

cap = VideoCapture(0)

marker_size_M = 0.165


####################### THREAD - DETECTION ###########################################
def detection():
    while True:
        ret, frame = cap.read()

        if ret:
            output = pose_of_container(frame, marker_size_M, ARUCO_DICT, ARUCO_PARAM)
            if output != None:
                print(f"X : {output[0]}, Y : {output[1]}, distance: {output[2]}")
            else:
                print("Not found")
        else:
            print("Camera not found")
            break

    cap.release()
    destroyAllWindows()
######################################################################################




####################### THREAD - API #################################################
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


# Метод меняющий переменную размера маркера
@app.post('/set_marker_size')
async def set_new_marker_size(size: float):
    global marker_size
    marker_size = size
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
#                 _, buffer = imencode('.jpg', frame)
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




####################### ENTRY POINT ##################################################
if __name__ == '__main__':
    #  Multi threading
    frame_processing_thread = threading.Thread(target=detection)
    fastapi_thread = threading.Thread(target=run_api)

    fastapi_thread.start()
    frame_processing_thread.start()

    fastapi_thread.join()
    frame_processing_thread.join()
