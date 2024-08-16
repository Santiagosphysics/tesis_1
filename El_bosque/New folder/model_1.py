import pytesseract 
import matplotlib.pyplot as plt 
import numpy as np 
import cv2
from PIL import Image, ImageFont, ImageDraw
from pytesseract import Output 

min_confidence = 40

def bouding_box(result, img, i, color = (255,100,0)):
    x = result['left'][i]
    y = result['top'][i]
    w = result['width'][i]
    h = result['height'][i]
    cv2.rectangle(img, (x,y), (x + w, y + h), color, 2)
    return x, y, img

font = './Fonts/calibri.ttf'

def write_text(text, x, y, img, font, font_size=25):
    font = ImageFont.truetype(font, font_size)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y - font_size), text, font=font)
    img = np.array(img_pil)
    return img

def application(path_img):
    img = cv2.imread(path_img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)
    img = cv2.bitwise_not(img)
    config = '--psm 11'
    result = pytesseract.image_to_data(img, output_type=Output.DICT, config=config)
    
    for i in range(len(result['text'])):
        confidence = int(result['conf'][i])
        if confidence > min_confidence:
            text = result['text'][i]
            if not text.isspace():
                x, y, img = bouding_box(result, img, i)
                img = cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 150, 255))
                # img = write_text(text, x, y, img, font)
                print(text)
                
    return img
                
path_img = r'./images/image_test_8.jpg'
img = application(path_img)

plt.imshow(img, cmap='gray')
plt.axis(False)
plt.show()
