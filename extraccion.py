import PPIF as pf
import cv2


def detecting_characters(contour, image_print, number_file):

    character = []
    image = image_print.copy()
    widths = [17, 10]
    for w in widths:
        low_limit, high_limit, max_aspect, min_aspect, whole_area = pf.estimation_area(image_print, w, 35)
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

    name_number = pf.calculting_name()

    return src, name_number


def run():

    source, name_number = call_image()
    no_noise = pf.softing_noise(source, 21)
    resize, image_tocut = pf.resizing(no_noise, source)

    cv2.imshow('Image', resize)
    cv2.waitKey(0)
    to_detect, to_cut = pf.threshold_image(resize)
    contour, _ = cv2.findContours(to_detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detecting, character = detecting_characters(contour, resize, _)
    character = pf.org_character(character)
    to_cut = pf.preparing_tocut(image_tocut)
    segmented = pf.cutting_characters(character, to_cut)

    for img in segmented:

        cv2.imwrite('./Prueba/' + str(name_number) + '.jpg', img)
        name_number = name_number + 1


if __name__ == '__main__':
    run()