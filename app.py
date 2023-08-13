from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
from io import BytesIO
from PIL import Image

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


@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(message)

@socketio.on('chat')
def chat(message):
    result = f"{message['who']}: {message['data']}"
    emit('get chat', result, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
