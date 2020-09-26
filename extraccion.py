import PPIF as pf
import cv2
import numpy as np
import glob
import os 


def estimation_area(image):
    # w 17 h 35 prom
    # w 7 h 35 uno
    # w 10 h 35 I

    width = 17
    height = 35

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
    low_limit, high_limit, max_aspect, min_aspect, whole_area = estimation_area(image_print)

    for c in contour:
        x, y, w, h = cv2.boundingRect(c)
        area_contour = w * h
        aspect_ratio = w / h
        if (area_contour/whole_area >= low_limit) and (area_contour/whole_area <= high_limit) and (aspect_ratio < max_aspect) and (aspect_ratio > min_aspect):
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # DRAWING THE PLATE'S RECTANGLE
            # print(w, h)
            # cv2.imshow('Dibujando', image)
            # cv2.waitKey(0)
            rectangle_char = (x, y, w, h)                   # x = UPPER - LEFT CORNER OF THESE RECTANGLE
            character.append(rectangle_char)                # FILLING THE CHARACTER VARIABLE.


    image_plate_char = image

    return image_plate_char, character


def call_image():

    file = './fuente/matricula_121.jpg'
    src = cv2.imread(file)

    return src



def calculting_name():

    list_of_files = glob.glob('./Base_datos/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    _, name_file = os.path.split(latest_file)
    number, _ = os.path.splitext(name_file)
    print(latest_file)
    name_number = int(number) + 1

    return name_number


def run():

    source = call_image()
    name_number = calculting_name()
    aux = pf.resizing(source)
    no_noise = pf.softing_noise(source, 21)
    resize = pf.resizing(no_noise)

    cv2.imshow('Image', resize)
    cv2.waitKey(0)
    to_detect, to_cut = pf.threshold_image(resize)

    cv2.imshow('Image', to_detect)
    cv2.waitKey(0)

    contour, _ = cv2.findContours(to_detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detecting, character = detecting_characters(contour, resize, _)
    character = pf.org_character(character)
    to_cut = pf.preparing_tocut(aux)
    segmented = pf.cutting_characters(character, to_cut)


    for img in segmented:

        cv2.imwrite('./Base_datos/' + str(name_number) + '.jpg', img)
        name_number = name_number + 1


if __name__ == '__main__':
    run()