from flask import Blueprint, render_template, Response
from flask_login import login_required, current_user
from . import db
import cv2

main = Blueprint('main', __name__)

camera = cv2.VideoCapture(0)


@main.route('/')
def index():
    return render_template('index.html')


def gen_frames(camera):
    while True:
        success, image = camera.read()  # read the camera frame
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # if not success:
        #     break
        # else:
        #     ret, buffer = cv2.imencode('.jpg', frame)
        #     frame = buffer.tobytes()
        #     # concat frame one by one and show result
        #     yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@main.route('/stream')
@login_required
def stream():
    return render_template('stream.html', name=current_user.name)


@main.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    camera = cv2.VideoCapture(-1)
    while camera.isOpened():
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
