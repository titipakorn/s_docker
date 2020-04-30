from pdf2image import convert_from_path
import glob
import os
import re
from fnmatch import filter
from multiprocessing import Process
from subprocess import call
from PIL import ImageOps, Image
import cv2
import numpy as np
import sys
import Augmentor


def center_image(path, save_path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grayscale

    # desired_size = img.shape[:2][::-1]
    desired_size = [706, 151]

    # new_size should be in (width, height) format

    retval, thresh_gray = cv2.threshold(
        gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)
    # find where the signature is and make a cropped region
    points = np.argwhere(thresh_gray == 0)  # find where the black pixels are
    # store them in x,y coordinates instead of row,col indices
    points = np.fliplr(points)
    # create a rectangle around those points
    x, y, w, h = cv2.boundingRect(points)
    crop = gray[y:y+h, x:x+w]  # create a cropped region of the gray image
    try:
        retval, thresh_crop = cv2.threshold(
            crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)

        # old_size is in (height, width) format
        old_size = thresh_crop.shape[:2]

        old_image = Image.fromarray(thresh_crop)
        deltaw = desired_size[0]-old_size[1]
        deltah = desired_size[1]-old_size[0]
        ltrb_border = (deltaw//2, deltah//2, deltaw -
                       (deltaw//2), deltah-(deltah//2))
        new_im = ImageOps.expand(old_image, border=ltrb_border, fill='white')
        new_im.save(save_path)
    except:
        new_im = Image.fromarray(thresh_gray)
        new_im.save(save_path)


def extract_sig(device):
    header_offset = device and 3000 or 2200
    footer_offset = device and 3151 or 2305
    path = device and '/app/data/device/' or '/app/data/app/'
    for file in filter(os.listdir(path), '*.[Pp][Dd][Ff]'):
        pages = convert_from_path(path+file, 300)
        for page in pages:
            h_o = device and (page.width/2)+171 or (page.width/2)+550
            f_o = device and (page.width/2)+171+707 or (page.width/2)+550+370
            page = page.crop((h_o, header_offset, f_o, footer_offset))
            if not os.path.exists(path+'extracted'):
                os.makedirs(path+'extracted')
            page.save(path+'extracted/{}.jpg'.format(file.replace('.pdf',
                                                                  '').replace('.PDF', '')), 'JPEG')
            break
    for file in os.listdir(path+'extracted'):
        if not os.path.exists(path+'crop'):
            os.makedirs(path+'crop')
        center_image(path+'extracted/{}'.format(file),
                     path+'crop/{}'.format(file))


def f():
    extract_sig(True)


def g():
    extract_sig(False)


if __name__ == '__main__':
    p = Process(target=f)
    g = Process(target=g)
    p.start()
    g.start()
    p.join()
    g.join()
    print('extraction: finished')
