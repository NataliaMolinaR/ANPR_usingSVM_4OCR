import cv2
import numpy as np
import os
import glob


def calculting_name():

    list_of_files = glob.glob('./muestras/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    _, name_file = os.path.split(latest_file)
    name, _ = os.path.splitext(name_file)
    name_number = str(name)

    return name_number


def resizing(image, image_2, width_desire):

    height, width = image.shape[0:2]

    aspect_ratio = (width / height)

    width_new = width_desire

    height_new = int(round(width_new / aspect_ratio))

    standard_src = cv2.resize(image, (width_new, height_new))

    image_tocut = cv2.resize(image_2,(width_new, height_new))

    return standard_src, image_tocut

def softing_noise(image, kn):
    """ It Softing the noise in the original image. kn  is the dimension  of the Kernel.I recommend you to use kn=5 for
    majority of pictures """

    s_noise = cv2.GaussianBlur(image, (kn, kn), 0)

    return s_noise


def threshold_image(image):
    """Converting to gray scale the image to make an adaptative thresholding for find the outlines"""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh_image_inv = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 7)

    thresh_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)
    return thresh_image_inv, thresh_image


def dilating_image(image, kn, i):
    """Dilating image's contours. kn is the dimensions of kernel"""

    kernel_dlt = np.ones((kn, kn), np.uint8)

    dilation = cv2.dilate(image, kernel_dlt, i)

    return dilation


def erode_image(image, kn, i):
    """Dilating image's contours. kn is the dimensions of kernel"""

    kernel_dlt = np.ones((kn, kn), np.uint8)

    dilation = cv2.erode(image, kernel_dlt, i)

    return dilation

def estimation_area(image, width, height):
    # w 17 h 35 prom
    # w 7 h 35 uno
    # w 10 h 35 I
    # width = 17
    # height = 35

    area = width * height
    height_w, width_w = image.shape[0:2]
    whole_area = height_w * width_w
    relation_area = area / whole_area
    # print(relation_area)

    area_character = relation_area
    bias = area_character * 0.50
    low_limit = area_character - bias
    high_limit = area_character + bias

    aspect_ratio = width / height
    aspect_bias = aspect_ratio * 0.25
    max_aspect = aspect_ratio + aspect_bias
    min_aspect = aspect_ratio - aspect_bias

    return low_limit, high_limit, max_aspect, min_aspect, whole_area


def detecting_characters(contour, image_print, number_file):

    character = []
    image = image_print.copy()
    widths = [17, 10]
    for w in widths:
        low_limit, high_limit, max_aspect, min_aspect, whole_area = estimation_area(image_print, w, 35)
        for c in contour:
            x, y, w, h = cv2.boundingRect(c)
            area_contour = w * h
            aspect_ratio = w / h
            if (area_contour/whole_area >= low_limit) and (area_contour/whole_area <= high_limit) and (aspect_ratio < max_aspect) and (aspect_ratio > min_aspect):
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # DRAWING THE PLATE'S RECTANGLE
                print(w, h)
                cv2.imshow('Dibujando', image)
                cv2.waitKey(0)
                rectangle_char = (x, y, w, h)                   # x = UPPER - LEFT CORNER OF THESE RECTANGLE
                character.append(rectangle_char)                # FILLING THE CHARACTER VARIABLE.


    image_plate_char = image

    return image_plate_char, character


def filling_white(image, smaller_image):

    rec_char_outer = image.copy()
    rec_char_inter = smaller_image.copy()

    fil_out, col_out = rec_char_outer.shape[0:2]
    fil_int, col_int = rec_char_inter.shape[0:2]

    left_limit = 4
    right_limit = col_out * 0.80
    up_limit = 5
    down_limit = fil_out * 0.95
    for n in range(0, fil_out):
        for m in range(0, col_out):
            if ((m < left_limit) or (m > right_limit)) or ((n < up_limit) or (n > down_limit)):
                rec_char_outer[n, m] = 255

    return rec_char_outer


def key_ordenation(tupla):
    return tupla[0]


def org_character(characters):

    ord_characters = sorted(characters, key=key_ordenation)
    return ord_characters


def cutting_characters(character, image_2cut):

    preparing = []
    m = len(character)
    image_2cut = image_2cut.copy()

    for n in character:

        ulc_X = n[0]
        ulc_Y = n[1]

        width = n[2]
        height = n[3]

        start_x = int(ulc_X)
        start_y = int(ulc_Y)

        width_new = int(width)
        height_new = int(height)

        final_x = start_x + width_new
        final_y = start_y + height_new

        width_outer = 25
        height_outer = 45

        x_outer = int(ulc_X) - 4
        y_outer = int(ulc_Y) - 6

        outer_xf = x_outer + width_outer
        outer_yf = y_outer + height_outer

        rec_char_outer = image_2cut[y_outer:outer_yf, x_outer:outer_xf]

        rec_char_inter = image_2cut[start_y:final_y, start_x: final_x]

        prep = filling_white(rec_char_outer, rec_char_inter)

        height_w, width_w = prep.shape[0:2]

        prep, _ = resizing(prep, prep, 15)


        preparing.append(prep)

        # if len(preparing) == m:
        #     for i in range(0, m):
        #         # height_w, width_w = preparing[i].shape[0:2]
        #         # print(height_w, width_w)
        #         cv2.imshow('Character' + str(i), preparing[i])
        #         cv2.moveWindow('Character' + str(i), 20 + i*120, 150)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
    return preparing


def preparing_tocut(image):

    _, image = threshold_image(image)

    return image