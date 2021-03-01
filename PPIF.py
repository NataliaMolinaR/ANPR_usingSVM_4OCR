import cv2
import numpy as np
import os
import glob

""" This library is used for the character detection and extraction"""

def calculting_name():
    """ This function search ID number of the image that contains a plate number"""

    list_of_files = glob.glob('./muestras/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    _, name_file = os.path.split(latest_file)
    name, _ = os.path.splitext(name_file)
    name_number = str(name)

    return name_number


def resizing(image, image_2, desire_width):
    """This function Resize the image in width and height using original aspect ratio. It use desire width for calculate the new height

    Besides, resizing returns the same image twice because the extraction module needs it for later image processing purposes."""

    height, width = image.shape[0:2]

    aspect_ratio = (width / height)

    new_width = desire_width

    new_height = int(round(new_width / aspect_ratio))

    standard_src = cv2.resize(image, (new_width, new_height))

    image_tocut = cv2.resize(image_2,(new_width, new_height))

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




def estimation_area(image, width, height):
    """ This functions develops differents  area estimation that will be uses in the caracter detection

    There is particular characters that are out of common average:

    Common average: w 17 - h 35.
    One: w 7 - h 35.
    I: w 10 - h 35.

    This occurs by the way that Boundingrectangle works.

    """

    area = width * height
    height_w, width_w = image.shape[0:2]
    whole_area = height_w * width_w
    relation_area = area / whole_area

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
    """This function compare all the contours  values had found  with area_estimation values in order to filter them """
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

                # print(w, h)
                # cv2.imshow('Drawing', image)
                # cv2.waitKey(0)

                rectangle_char = (x, y, w, h)                   # x = UPPER - LEFT CORNER OF THESE RECTANGLE
                character.append(rectangle_char)                # FILLING THE CHARACTER VARIABLE.


    image_plate_char = image

    return image_plate_char, character


def filling_white(image, smaller_image):
    """ This functions set white the pixels according to percents that it has asigned """

    rec_char_outer = image.copy()

    fil_out, col_out = rec_char_outer.shape[0:2]

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
    """ This key indicates that it will be sort by the fisrt tupla's element. This element is the upper left x coordinate of the rectangle."""

    return tupla[0]


def org_character(characters):
    """ This functions will sort the characters have found left to right using the key ordenation"""

    ord_characters = sorted(characters, key=key_ordenation)
    return ord_characters


def cutting_characters(character, image_2cut):
    """ In this functions develops the rectangles cut that contains every single character detected by using
    the coordinates given by  BoundingRectangle function"""

    preparing = []
    m = len(character)
    image_2cut = image_2cut.copy()

    for n in character:

        # The information is extracted from the the tupla n in character list.
        # For more information about this coordinates check the Bounding Rectangle function resources
        ulc_X = n[0]
        ulc_Y = n[1]

        width = n[2]
        height = n[3]

        #There is asigned new name to the above information and is constructed the rectangle.
        start_x = int(ulc_X)
        start_y = int(ulc_Y)

        width_new = int(width)
        height_new = int(height)


        final_x = start_x + width_new
        final_y = start_y + height_new

        # A width and height outter value is placed  that allow a prudential margin of the principal content.
        width_outer = 25
        height_outer = 45


        #Then the rectangle is constructed with these outter width and heigt and the x and y coordinate are displaced too.
        x_outer = int(ulc_X) - 4
        y_outer = int(ulc_Y) - 6

        outer_xf = x_outer + width_outer
        outer_yf = y_outer + height_outer

        # Both rectangles are cutted by image_2cut

        rec_char_outer = image_2cut[y_outer:outer_yf, x_outer:outer_xf]

        rec_char_inter = image_2cut[start_y:final_y, start_x: final_x]

        # Imperfections are corrected and filling with white color by filling_white

        prep = filling_white(rec_char_outer, rec_char_inter)

        prep, _= resizing(prep, prep, 15)

        preparing.append(prep)

    return preparing


def preparing_tocut(image):
    """ This function  makes the treshhold in the entry image but use the non inverted treshold considering subsequent recognition processes"""

    _, image = threshold_image(image)

    return image