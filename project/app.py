import os
from flask import Flask, Blueprint, render_template, Response
from flask_login import login_required, current_user
from . import db
import cv2

main = Blueprint('main', __name__)

camera = cv2.VideoCapture(1)


def gen_frames():
    print(camera)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/stream')
@login_required
def stream():
    return render_template('stream.html', name=current_user.name)


@main.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
