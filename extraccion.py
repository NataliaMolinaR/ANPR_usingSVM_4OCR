import PPIF as pf
import cv2


def call_image():

    file = './fuente/matricula_121.jpg'
    src = cv2.imread(file)
    name_number = pf.calculting_name()

    return src, name_number


def run():

    source, name_number = call_image()
    no_noise = pf.softing_noise(source, 21)
    resize, image_tocut = pf.resizing(no_noise, source, 150)
    cv2.imshow('Plate', image_tocut)
    cv2.moveWindow('Plate', 20, 50)

    to_detect, to_cut = pf.threshold_image(resize)
    contour, _ = cv2.findContours(to_detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detecting, character = pf.detecting_characters(contour, resize, _)
    character = pf.org_character(character)
    to_cut = pf.preparing_tocut(image_tocut)
    segmented = pf.cutting_characters(character, to_cut)

    for img in segmented:

        cv2.imwrite('./Prueba/' + str(name_number) + '.jpg', img)
        name_number = name_number + 1


if __name__ == '__main__':
    run()