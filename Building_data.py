import csv
import numpy as np
import cv2

def reading_data():

    file = './fuente/matricula_' + str(n) + '.jpg'
    src = cv2.imread(file)

    return src

def run():

    data = reading_data()
    data = data.reshape(-1)
    print('Flatered', data)
    with open('./prueba.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(data)


if __name__ == '__main__':
    run()

