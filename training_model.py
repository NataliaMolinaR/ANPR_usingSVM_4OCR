import numpy as np
from sklearn import svm


def run():
    with open("./data_base.csv") as file:
        n_cols = len(file.readline().split(";"))
        print(n_cols)

    X = np.loadtxt("./data_base.csv", delimiter=";", usecols= np.arange(0, n_cols - 1))

    # a = np.arange(0, n_cols-1)
    # print(a)
    # print(X.shape)
    # print(X[:, n_cols - 2])

    Y = np.loadtxt("./data_base.csv", delimiter=";", usecols= n_cols-1)
    # print(y.shape, n_cols - 1)
    # print(y)

    recon_char = svm.SVC(Kernel='linear', decision_function_shape='ovr')
    recon_char.fit(X, Y)

    w = recon_char.coef_[0]
    b = recon_char.intercept_[0]

    num_suportv = recon_char.n_support_

    ind_suportv = recon_char.support_

    suport_vec = recon_char.support_vectors_

if __name__ == '__main__':
    run()