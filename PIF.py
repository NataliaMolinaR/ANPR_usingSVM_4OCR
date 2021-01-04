import cv2
import numpy as np


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
    """This function compare all the contours found as width and height average"""

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

    return plate_detected, plate


def detecting_characters(contour, image_print, number_file):

    height, width = image_print.shape[0:2]
    height_max_char = 40
    height_min_char = 34
    character = []

    for c in contour:
        x, y, w, h = cv2.boundingRect(c)

        if (h <= height_max_char) and (h >= height_min_char) and (
                y / height < 0.38):  # FILTERING THE RECTANGLE'S HEIGHT

            image_plate_char = cv2.rectangle(image_print, (x, y), (x + w, y + h), (0, 255, 0), 1)  # DRAWING THE PLATE'S RECTANGLE

            rectangle_char = (x, y, w, h)                   # x = UPPER - LEFT CORNER OF THESE RECTANGLE

            character.append(rectangle_char)                # FILLING THE CHARACTER VARIABLE.

            #print(rectangle_char)

            cv2.imshow('Plate number  ' + number_file, image_plate_char)
            cv2.moveWindow('Plate number  ' + number_file, 30, 20)

            #cv2.waitKey(0)

    image_plate_char = image_print

    return image_plate_char, character


def toget_characters(image, number_file):

    character = []
    characters_detected = False
    missing_character = False
    image_plate_char = None
    image_print = image.copy()

    while not characters_detected:
        s_noise = softing_noise(image, 5)

        thresh, _ = threshold_image(s_noise)

        #cv2.imshow('thresh', thresh)
        # cv2.waitKey(0)

        contour = finding_contours(thresh)

        image_plate_char, character = detecting_characters(contour, image_print, number_file)

        """cv2.imshow('Image plate char', image_plate_char)
        cv2.waitKey(0)"""

        if len(character) >= 6:

            sorted_char = org_character(character)

            for n in range(0, len(sorted_char) - 1):

                left_character = sorted_char[n]
                left_x = left_character[0]

                right_character = sorted_char[n + 1]
                right_x = right_character[0]

                distance = right_x - left_x

                if distance > 37:
                    missing_character = True

            if not missing_character:
                characters_detected = True

        if missing_character:
            print(' Character lost, please take a new picture.')
            break

        if characters_detected:
            image_plate_char, character = image_plate_char, character
            break

        if not characters_detected:

            s_noise = softing_noise(image, 5)

            dilating = dilating_image(s_noise, 3, 1)

            thresh, _ = threshold_image(dilating)  # IT TURN BLACK WHITE COLOR

            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)

            contour = finding_contours(thresh)

            image_plate_char, character = detecting_characters(contour, image_print, number_file)

            """cv2.imshow('Image plate char', image_plate_char)
            cv2.waitKey(0)"""

            if len(character) >= 6:

                sorted_char = org_character(character)

                for n in range(0, len(sorted_char) - 1):

                    left_character = sorted_char[n]
                    left_x = left_character[0]

                    right_character = sorted_char[n + 1]
                    right_x = right_character[0]

                    distance = right_x - left_x

                    if distance > 37:
                        missing_character = True

                if not missing_character:
                    characters_detected = True

            if missing_character:
                print(' Character lost, please take a new picture.')
                break

            if characters_detected:
                image_plate_char, character = image_plate_char, character
                break

    return image_plate_char, character, missing_character


def key_ordenation(tupla):
    return tupla[0]


def org_character(characters):

    ord_characters = sorted(characters, key=key_ordenation)
    return ord_characters


def filling_white(image, smaller_image):

    rec_char_outer = image.copy()
    rec_char_inter = smaller_image.copy()

    fil_out, col_out = rec_char_outer.shape[0:2]
    fil_int, col_int = rec_char_inter.shape[0:2]

    dif_fil = (fil_out - fil_int)/2

    left_limit = 10
    right_limit = col_out * 0.77
    up_limit = 10
    down_limit = fil_out * 0.90
    for n in range(0, fil_out):
        for m in range(0, col_out):
            if ((m < left_limit) or (m > right_limit)) or ((n < up_limit) or (n > down_limit)):
                rec_char_outer[n, m] = 255

    return rec_char_outer


def cutting_characters(character, plate_image2cut):

    preparing = []
    m = len(character)

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

        width_outer = 35
        height_outer = 55

        x_outer = int(ulc_X) - 10
        y_outer = int(ulc_Y) - 10

        outer_xf = x_outer + width_outer
        outer_yf = y_outer + height_outer

        rec_char_outer = plate_image2cut[y_outer:outer_yf, x_outer:outer_xf]
        rec_char_inter = plate_image2cut[start_y:final_y, start_x: final_x]
        prep = filling_white(rec_char_outer, rec_char_inter)

        preparing.append(prep)

        if len(preparing) == m:
            for i in range(0, m):

                cv2.imshow('Character' + str(i), preparing[i])
                cv2.moveWindow('Character' + str(i), 30 + i*125, 150)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return preparing


def storage_plates_char(character, number_file, plates_characters, plate):

    info_char = (character, number_file)

    sorted_info_char = org_character(character)

    # print('Mostrando sorted_info_char', sorted_info_char, len(sorted_info_char))

    final = cutting_characters(sorted_info_char, plate)

    plates_characters.append(final)

    # print('PLATES CHARACTERS', plates_characters, len(plates_characters))

    return plates_characters

"""print('left_x: ', left_x, ' right_x', right_x, 'difference right - left', distance )
                print(' Character:', sorted_char)
                cv2.waitKey(0)"""



