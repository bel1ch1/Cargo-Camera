from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import cv2
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Отправляем в браузер HTML
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Функция генератор для отправки видео потока (байтов)
def generate_frames(cap):
    while True:
        success, frame = cap.read()
        if not success:
            break

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n'
        )


@app.get("/video_feed")
async def video_feed():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return {"error": "Could not open video file"}

    frame_generator = generate_frames(cap)

    return StreamingResponse(frame_generator, media_type="multipart/x-mixed-replace; boundary=frame")



uvicorn.run(app, host='127.0.0.1', port=8000)
