import detecting_plate as dp
import Extraction as et
import PPIF as pf
import joblib
import cv2
from sklearn import svm


def call_image():

    file = './muestras/carro_1.jpg'
    src = cv2.imread(file)
    name_number = pf.calculting_name()
    return src, name_number


def run():
    image, name_number = call_image()
    plate = dp.searching_plate(image, name_number)
    characters = et.extraction(plate)
    svm_recon = joblib.load('modelo_entrenado.pkl')
    info = []

    for segment in characters:

        data = segment.reshape(-1)
        character = svm_recon.predict([data])
        print('caracter', character)
        int_character = character.astype(int)[0]
        info.append(str(int_character))
        print(info)

        for i in range(0, len(characters)):
            cv2.imshow('Plate', plate)
            cv2.imshow('Character' + str(i), characters[i])
            cv2.moveWindow('Character' + str(i), 20 + i * 120, 250)

    cv2.waitKey(0)
    cv2.destroyAllWindows()










if __name__ == '__main__':
    run()