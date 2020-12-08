import numpy as np
from sklearn import svm


def run():
    with open("./data_base.csv") as file:
        n_cols = len(file.readline().split(";"))
        print(n_cols)

    X = np.loadtxt("./data_base.csv", delimiter=";", usecols=np.arange(0, n_cols - 1))
    a = np.arange(0,n_cols)
    print(a)
    print(X.shape)
    print(X[:, n_cols - 2])
    y = np.loadtxt("./data_base.csv", delimiter=";", usecols= n_cols-1)
    print(y.shape)
    print(y)



if __name__ == '__main__':
    run()
