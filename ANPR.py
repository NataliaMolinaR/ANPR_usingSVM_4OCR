import detecting_plate as dp
import Extraction as et
import PPIF as pf
import joblib
import cv2
from time import time


def character2str(character, plate_len, index):
    """This function transform the ID character to string text"""

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
    """ This function call the image that will be used for recognition"""

    file = './fuente/matricula_144.jpg'
    src = cv2.imread(file)
    name_number = pf.calculting_name()
    return src, name_number


def run():

    pis_time = time()
    image, name_number = call_image()
    plate = dp.detecting_plate(image, name_number)
    try:

        characters = et.extraction(plate)
        pif_time = time()
        svm_recon = joblib.load('modelo_entrenado1.pkl')
        plate_str = ''
        index = 1
        plate_len = len(characters)

        rs_time = time()
        for segment in characters:

            data = segment.reshape(-1)
            character = svm_recon.predict([data])
            str_character = character2str(character, plate_len, index)
            plate_str += str_character
            rf_time = time()

            for i in range(0, len(characters)): #Showing the character extraction results
                graf, _ = pf.resizing(image, image, 150)
                cv2.imshow('Plate', graf)
                cv2.imshow('Character' + str(i), characters[i])
                cv2.moveWindow('Character' + str(i), 20 + i * 120, 250)
            index += 1

        pif_time = round(pif_time - pis_time, 3)
        r_time = round(rf_time - rs_time, 3)
        print('Tiempo de procesamiento de imagen: '+ str(pif_time))
        print('Tiempo de reconocimiento de caracteres: ' +str(r_time))

        print('La placa es:', plate_str)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except UnboundLocalError:
        print("Oops! May be your plate is physically deteriorated,"
              " Try the picture again with better light conditions...")

    except:
        print("Oops! I can't see all characters correctly. Try taking "
              "the picture again  and make sure about position and light conditions")

if __name__ == '__main__':
    run()