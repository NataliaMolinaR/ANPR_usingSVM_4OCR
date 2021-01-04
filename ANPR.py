import detecting_plate as dp
import Extraction as et
import PPIF as pf
import joblib
import cv2
from sklearn import svm


def character2str(character):

    int_character = character.astype(int)[0]

    if int_character < 10:
        str_character = str(int_character)
    else:
        str_character = chr(int_character + 55)
    print('caracter', character, str_character)

    return str_character


def call_image():

    file = './muestras/carro_6.jpg'
    src = cv2.imread(file)
    name_number = pf.calculting_name()
    return src, name_number


def run():

    image, name_number = call_image()
    plate = dp.detecting_plate(image, name_number)
    characters = et.extraction(plate)
    svm_recon = joblib.load('modelo_entrenado.pkl')
    plate_str = ''

    for segment in characters:

        data = segment.reshape(-1)
        character = svm_recon.predict([data])
        str_character = character2str(character)
        plate_str += str_character

        for i in range(0, len(characters)):
            cv2.imshow('Plate', plate)
            cv2.imshow('Character' + str(i), characters[i])
            cv2.moveWindow('Character' + str(i), 20 + i * 120, 250)

    print('La placa es:', plate_str)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()