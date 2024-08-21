import tensorflow  as tf
import numpy as np 
import pandas as pd
import cv2
import imutils
from imutils.contours import sort_contours

import tensorflow as tf 
from tensorflow.keras.models import load_model

import matplotlib.pyplot as plt
import matplotlib

model = load_model('./models/second_model.h5')

matplotlib.use('Agg')

def names_label():
    names = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    names = [label for label in names]
    return names 


def prepro_img(path_img):
    gray = cv2.cvtColor(cv2.imread(path_img), cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)
    img = cv2.Canny(img, 40, 150)
    img = cv2.dilate(img, np.ones((2,2), np.uint8))
    return gray, img


def find_contours(img, gray):
    img_copy = img.copy()
    gray = np.array(gray)
    conts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = imutils.grab_contours(conts)
    conts = sort_contours(conts, method='left-to-right')[0]

    min_w, max_w = 5, 90
    min_h, max_h = 10, 90 
    n = 5
    letters = []
    conts_2 = []
    
    for c in conts:
        (x, y, w, h) = cv2.boundingRect(c)
        if (w >= min_w and w < max_w) and (h >= min_h and h < max_h):
            img_p = gray[y-n : y+h+n,   x-n : x+n+w ]
            cv2.rectangle(img_copy, (x,y), (x+w, h+y), (255,100,0),2)
            img_p = cv2.threshold(img_p, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            img_p = cv2.dilate(img_p, np.ones((2,2), np.uint8 ))
            letters.append(img_p)
            conts_2.append(c)
    plt.imshow(img_copy, cmap='gray');
    return letters, conts_2



def img_prediction(img, model, name_labels):
    img = cv2.resize(img, (28,28))
    img = img.astype('float32')/255.0
    img = np.expand_dims(img, axis=-1)
    img = np.reshape(img, (1,28,28,1))

    prediction = model.predict(img)
    prediction = name_labels[np.argmax(prediction)]

    return prediction


def letter_pred(img, gray):
    names = names_label()
    letters = find_contours(img, gray)[0]
    img_pred = [img_prediction(letter, model, names) for letter in letters]
    question_row = []
    answer_row = []
    for i in range(len(img_pred)):
        if i%2 == 0:
            question_row.append(img_pred[i])
        else:
            answer_row.append(img_pred[i])
    response = ''

    
    for i in answer_row:
        response += i

        if response == 'PREGUNTA' or response == 'PREGUMTA' or response == 'PRECUNTA':
            response = ''
    
    # response = [i for i in response]

    fig, axes = plt.subplots(1, len(letters), figsize=(20,5) )

    for i, letter in enumerate(letters):
        letter = cv2.resize(letter, (28,28))
        axes[i].imshow(letter, cmap='gray')
        axes[i].axis('off')

    return response


# gray, img = prepro_img('./images/image_test_9.jpg')
# answer_row = letter_pred(img, gray)
# print(answer_row)