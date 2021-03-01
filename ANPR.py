import detecting_plate as dp
import Extraction as et
import PPIF as pf
import joblib
import cv2


def character2str(character, plate_len, index):

    int_character = character.astype(int)[0]

    if plate_len == 7:              # NEW PLATES

        if int_character < 10:      # Numbers
            str_character = str(int_character)

        else:                       # Letters
            str_character = chr(int_character + 55)
        print('caracter', character, str_character)

    if plate_len == 6:              # OLD PLATES

        if int_character < 10:      # Numbers
            str_character = str(int_character)

            if int_character == 0 and not (index == 4 or index == 5):
                str_character = 'O'

        else:                       # Letters
            if int_character == 24 and (index == 4 or index == 5):
                str_character = '0'
            else:
                str_character = chr(int_character + 55)
        print('caracter', character, str_character)

    return str_character


def call_image():

    file = './muestras/carro_1.jpg'
    src = cv2.imread(file)
    name_number = pf.calculting_name()
    return src, name_number


def run():

    image, name_number = call_image()
    plate = dp.detecting_plate(image, name_number)
    characters = et.extraction(plate)
    svm_recon = joblib.load('modelo_entrenado1.pkl')
    plate_str = ''
    index = 1
    plate_len = len(characters)

    for segment in characters:

        data = segment.reshape(-1)
        character = svm_recon.predict([data])
        str_character = character2str(character, plate_len, index)
        plate_str += str_character

        for i in range(0, len(characters)):
            graf, _ = pf.resizing(plate, plate, 150)
            cv2.imshow('Plate', graf)
            cv2.imshow('Character' + str(i), characters[i])
            cv2.moveWindow('Character' + str(i), 20 + i * 120, 250)
        index += 1


    print('La placa es:', plate_str)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()