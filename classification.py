import keras
from keras import backend as k
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import GlobalAvgPool2D
from keras.applications import MobileNetV3Small
from keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
import cv2


mobile = MobileNetV3Small()
def prepare_image(file):
    img_path = ''
    img = image.load_img(file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    print(f'img array {img_array.shape}')
    print(f'img array expand {img_array_expanded_dims.shape}')
    return preprocess_input(img_array_expanded_dims)

pre_img = prepare_image('./good.jpg')
predict = mobile.predict(pre_img)
print(predict)
result = imagenet_utils.decode_predictions(predict)
print(result)
