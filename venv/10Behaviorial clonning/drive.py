import socketio
import eventlet
import numpy as np
from flask import Flask
import tensorflow as tf
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2



sio = socketio.Server()
app = Flask(__name__)

def  img_preprocess(img):
    img = img[60:135,:,:]
    img = cv2.cvtColor(img,cv2.COLOR_RGB2YUV)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img

@sio.on('telemetry')
def telemetry(sid, data):
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    image = np.array([image])
    steering_angle = float(model.predict(image))
    send_control(steering_angle, 1.0)



@sio.on('connect')
def connect(sid, environ):
    print('connected')
    send_control(0,0)#this is a command given to

    print("hello world")

def send_control(steering_angle, throttle):
    sio.emit('steer', data ={
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__()
    }
             )
if __name__ == '__main__':
    model = load_model('model.h5')
   # app.run(port= 3000)
    app = socketio.Middleware(sio,app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)