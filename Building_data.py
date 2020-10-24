import csv
import numpy as np
import cv2
import PPIF as pif


def reading_data():

    n = 1
    file = './Base_datos/' + str(n) + '.jpg'
    src = cv2.imread(file)

    cv2.imshow('letter_origin', src)
    cv2.moveWindow('letter_origin', 20, 50)

    src, _ = pif.resizing(src, src, 5)

    cv2.imshow('letter', src)
    cv2.moveWindow('letter', 100, 50)
    cv2.waitKey(0)

    return src


def reducing_chanel(example):
    gray = cv2.cvtColor(example, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)
    return thresh_img


def run():

    example = reading_data()
    data = reducing_chanel(example)

    data = data.reshape(-1)

    tag = int(input('Escribe la etiqueta del caracter: '))

    training_example = np.append(data, tag)

    with open('./data_base.csv',  'a', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(training_example)

if __name__ == '__main__':
    run()

