import numpy as np
import cv2 as cv
import os

images_dir = 'static/images'

for img_file in os.listdir(images_dir):
    img_path = os.path.join(images_dir, img_file)

    # Read the image
    img = cv.imread(img_path)
    assert img is not None, "file could not be read, check with os.path.exists()"
    imggray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imggray, 60, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for idx ,cnt in enumerate(contours):
        if cv.contourArea(cnt) > 6000 :
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            new_img = img[y:y+h , x:x+w]
            cv.imwrite(f"croped_img/{idx+1}.png", new_img)
            cv.drawContours(img, [cnt], 0, (0, 255, 0), 3)

    new_width, new_height = 700, 500

# set new dimensions for image
    new_dim = (new_width, new_height)
    resized_img = cv.resize(img, new_dim, interpolation=cv.INTER_AREA)

    cv.imshow('img', resized_img)
    cv.waitKey(0)
