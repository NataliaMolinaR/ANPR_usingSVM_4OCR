import numpy as np


def run():
    with open("./data_base.csv") as file:
        n_cols = len(file.readline().split(";"))
        print(n_cols)
    X = np.loadtxt("./data_base.csv", delimiter=";", usecols=np.arange(0, n_cols-1))
    print(X.shape)

    y = np.loadtxt("./data_base.csv", delimiter=";", usecols= n_cols)
    print(y.shape)



if __name__ == '__main__':
    run()
