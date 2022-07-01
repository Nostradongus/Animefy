import tensorflow.compat.v1 as tf
from adjust_brightness import adjust_brightness_from_src_to_dst, read_img
import cv2
import numpy as np
from PIL import Image

def load_input_image(image_path, size=[256,256]):
    img = cv2.imread(image_path).astype(np.float32)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = preprocessing(img,size)
    img = np.expand_dims(img, axis=0)
    return img

""" FOR WEB APP ONLY, WHEN DEPLOYED """
# def load_input_image(image_file_buffer, size=[256, 256]):
#     img = Image.open(image_file_buffer).convert('RGB')
#     img = np.array(img).astype(np.float32)
#     img = preprocessing(img, size)
#     img = np.expand_dims(img, axis=0)
#     return img

def preprocessing(img, size):
    h, w = img.shape[:2]
    if h <= size[0]:
        h = size[0]
    else:
        x = h % 32
        h = h - x

    if w < size[1]:
        w = size[1]
    else:
        y = w % 32
        w = w - y
    # the cv2 resize func : dsize format is (W ,H)
    img = cv2.resize(img, (w, h))
    return img/127.5 - 1.0

def inverse_transform(images):
    images = (images + 1.) / 2 * 255
    # The calculation of floating-point numbers is inaccurate, 
    # and the range of pixel values must be limited to the boundary, 
    # otherwise, image distortion or artifacts will appear during display.
    images = np.clip(images, 0, 255)
    return images.astype(np.uint8)

# def imsave(images, path):
#     return cv2.imwrite(path, cv2.cvtColor(images, cv2.COLOR_BGR2RGB))