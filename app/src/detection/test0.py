from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from websockets.exceptions import ConnectionClosed
from fastapi.templating import Jinja2Templates
import cv2
import asyncio
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Отправляем в браузер HTML
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index_v.html", {"request": request})


# Калибровка позиции для пользователя
@app.get('/calibration')
def calibration(request: Request):
    """Выводит картинку для пользователя, чтобы откалибровать положение груза"""
    return templates.TemplateResponse("video.html", {"request": request})


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        cap = cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, format=BGRx' ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.03)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")
        cap.release()
    finally:
        await websocket.close()


if __name__ == '__main__':
    uvicorn.run(app, host='10.131.121.22', port=8000)