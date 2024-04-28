from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/calibration")
async def calibration_frames():
    video_capture = cv2.VideoCapture(0)

    def generate():
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                break
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace; boundary=frame")
