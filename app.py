from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
from io import BytesIO
from PIL import Image
import face_recognition
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('index.html',**values)

@app.route('/image')
def image_page():
    return render_template('image.html',**values)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('image')
def image_event(msg):
    print(msg)
    img_byte = base64.b64decode(msg)

    image_stream = BytesIO(img_byte)
    image = Image.open(image_stream)

    image.save('good.jpg')
    emit('get image', {'data': 'save!!'})

def byte_2_img(img):
    img_byte = base64.b64decode(img)

    image_stream = BytesIO(img_byte)
    image = Image.open(image_stream)
    return image

@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(message)

@socketio.on('chat')
def chat(message):
    result = f"{message['who']}: {message['data']}"
    emit('get chat', result, broadcast=True)

@socketio.on('face')
def face_img(message):
    raw_img = message['img']
    img = byte_2_img(raw_img)
    np_img = np.array(img)
    face_locations = face_recognition.face_locations(np_img)
    result = {'rect': face_locations}
    return emit('face rect', result)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
