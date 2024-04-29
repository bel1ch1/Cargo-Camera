from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from websockets.exceptions import ConnectionClosed
from fastapi.templating import Jinja2Templates
import uvicorn
import asyncio
import cv2


app = FastAPI()
camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
templates = Jinja2Templates(directory="templates")


# Рендер стартовой страницы
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Кнопка запуска приложения для детекции
@app.get('/start_detection')
async def start_detection_app(request: Request):
    """Отвечает на запросс для старта приложения детекции"""
    request = {"status": "True"}
    return request


# Калибровка позиции для пользователя
@app.get('/calibration')
def calibration(request: Request):
    """Выводит картинку для пользователя, чтобы откалибровать положение груза"""
    return templates.TemplateResponse("calibration.html", {"request": request})


# Апгрейд протокола до websocket-а
@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                _, buffer = cv2.imencode('.jpg', frame)
                await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.03)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")
    finally:
        await websocket.close()
        RedirectResponse("/")

# Точка входа
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000) # менять
