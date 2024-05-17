import threading
import pickle
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from cv2 import VideoCapture, waitKey, destroyAllWindows

from detection import pose_of_container


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


def run_api():
    uvicorn.run(app, host='127.0.0.1', port=8000)
######################################################################################





####################### THREAD - DETECTION ###########################################
def detection():
    # Ининциализируем камеру
    cap = VideoCapture(0)
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
        k = waitKey(30) & 0xff
        if k == 27:
            break
    # Чистим ресуры
    cap.release()
    destroyAllWindows()
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
