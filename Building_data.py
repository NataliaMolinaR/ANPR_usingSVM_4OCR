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

    src, _ = pif.resizing(src, src, 15)

    width, height = src.shape[0:2]
    print(width, height)
    cv2.imshow('letter', src)
    cv2.moveWindow('letter', 100, 50)
    cv2.waitKey(0)

    return src


def run():

    data = reading_data()
    data = data.reshape(-1)
    print('Flatered', data)
    with open('./data_base.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(data)


if __name__ == '__main__':
    run()

