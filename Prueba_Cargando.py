import csv
import numpy as np
import cv2 as cv


def generate_data(rows, colum):

    image_test = np.zeros((rows, colum), dtype=np.uint8)

    top1 = 0
    top2 = int(rows * 0.5)
    top3 = rows

    lat1 = 0
    lat2 = int(colum * 0.5)
    lat3 = colum

    image_test[top1:top2, lat1:lat2] = 1
    image_test[top1:top2, lat2:lat3] = 2
    image_test[top2:top3, lat1:lat2] = 3
    image_test[top2:top3, lat2:lat3] = 4
    print('Array', image_test)
    return image_test


def run():

    data = generate_data(4, 4)
    with open('./prueba.csv', 'a', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(data)

    data_new = np.loadtxt("./prueba.csv", delimiter=",", usecols=np.arange(0,2))
    print('New array', data_new)
    del data_new



if __name__ == '__main__':
    run()

