import csv
import numpy as np
import cv2


def run():

    with open("./data_base.csv") as file:
        n_cols = len(file.readline().split(";"))
        print(n_cols)

    X = np.loadtxt("./data_base.csv", delimiter=";", usecols=np.arange(0, n_cols - 1))
    Y = np.loadtxt("./data_base.csv", delimiter=";", usecols=n_cols - 1)
    Y_new = Y

    for index in range(0, len(Y_new)):
        if int(Y_new[index]) == 0:
            char = X[index].reshape(27, 15)
            cv2.imshow('Letra', char)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            tag = int(input('Correcion:'))
            Y_new[index] = tag

    Data_base = np.insert(X, X.shape[1], Y_new, 1)
    Data_base = Data_base.astype(int)

    print('Tamano X: ', X.shape, 'Tamano: ', Y.shape)
    print(Data_base.shape)

    with open('./data_base1.csv', 'a', newline='') as file:
        writer = csv.writer(file, lineterminator='\n', delimiter=";")
        writer.writerows(Data_base)


if __name__ == '__main__':
    run()

