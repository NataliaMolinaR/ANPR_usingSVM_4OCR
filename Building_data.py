import csv
import numpy as np
import cv2
import PPIF as pif
import glob


def reading_data(n):

    file = './Base_datos/' + str(n) + '.jpg'
    src = cv2.imread(file)

    src, _ = pif.resizing(src, src, 15)

    cv2.imshow('Letra' + str(n), src)
    cv2.moveWindow('Letra' + str(n), 100, 50)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return src


def reducing_chanel(example):
    gray = cv2.cvtColor(example, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 7)
    return thresh_img


def run():
    quantity_examplet = len(glob.glob('./Base_datos/*'))
    print(quantity_examplet)
    for n in range(601, quantity_examplet):
        print(n)
        example = reading_data(n)
        data = reducing_chanel(example)
        data = data.reshape(-1)
        tag = int(input('Escribe la etiqueta del caracter: '))
        training_example = np.append(data, tag)
        # print(len(data),len(training_example))
        with open('./data_base.csv',  'a', newline='') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(training_example)


if __name__ == '__main__':
    run()

