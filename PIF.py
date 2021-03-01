import cv2
import numpy as np

""" This library is used for the plate detection and extraction"""

def resizing_image(image):
    """It Reading image's dimensions which going to be resizing and proper cutting  it. Whether you want change the size
    of the picture you have to change te width_new parameter. At the bottom of this function are a little code where you
     might check all values"""

    height, width = image.shape[0:2]

    aspect_ratio = (width / height)

    width_new = 1350

    height_new = int(round(width_new / aspect_ratio))

    standard_src = cv2.resize(image, (width_new, height_new))

    start_x = int(height_new * .45)
    final_x = int(height_new * .85)

    start_y = int(width_new * 0.20)
    final_y = int(width_new * 0.85)

    cut_src = standard_src[start_y:final_y, start_x:final_x]

    """print('Height =' + str(height), 'Width =' + str(width), 'Height new =' + str(height_new),
    'Width new =' + str(width_new),'Start_x =' + str(start_x), 'Final_x' + str(final_x), 
    'Start_y =' + str(start_y), 'Final_y' + str(final_y))"""

    return cut_src


def softing_noise(image, kn):
    """ It Softing the noise in the original image. kn  is the dimension  of the Kernel.I recommend you to use kn=5 for
    majority of pictures """

    s_noise = cv2.GaussianBlur(image, (kn, kn), 0)

    return s_noise


def threshold_image(image):
    """Converting to gray scale the image to make an adaptative thresholding for find the outlines"""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 13)

    return thresh_image, gray


def dilating_image(image, kn, i):
    """Dilating image's contours. kn is the dimensions of kernel"""

    kernel_dlt = np.ones((kn, kn), np.uint8)

    dilation = cv2.dilate(image, kernel_dlt, i)

    return dilation


def finding_contours(image):
    """Searching in the image's contour"""

    contour, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contour


def searching_plate(contour, image_print, plate_detected, number_file):
    """This function compare all the contours had found width and height with average values in order to filter them"""

    global plate

    width_max_plate = 190
    width_min_plate = 160
    height_max_plate = 95
    height_min_plate = 70

    for c in contour:
        x, y, w, h = cv2.boundingRect(c)

        if (w <= width_max_plate) and (w >= width_min_plate) and (h <= height_max_plate) and (h >= height_min_plate):  # FILTERING THE RECTANGLE'S HEIGHT

                image_plate = cv2.rectangle(image_print, (x, y), (x + w, y + h), (0, 255, 0), 2)  #DRAWING THE PLATE'S RECTANGLE
                plate_detected = True

                plate = image_print[y:y+h, x:x+w]

                # cv2.imshow('Plate ' + number_file, plate)
                # cv2.moveWindow('Plate ' + number_file, 30, 20)

                # cv2.imshow('Plate detected number  ' + number_file, image_plate)
                # cv2.moveWindow('Plate detected number  ' + number_file, 950, 20)

        if not plate_detected:
            plate = None

    return plate_detected, plate


