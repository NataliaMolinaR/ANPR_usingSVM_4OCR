import numpy as np
from sklearn import svm
import joblib
from time import time

def run():

    with open("./data_base1.csv") as file:
        n_cols = len(file.readline().split(";"))
        print(n_cols)

    X = np.loadtxt("./data_base1.csv", delimiter=";", usecols= np.arange(0, n_cols - 1))
    Y = np.loadtxt("./data_base1.csv", delimiter=";", usecols= n_cols-1)

    recon_char = svm.SVC(kernel='linear', decision_function_shape='ovr')
    print('Entrenando')
    start_time = time()
    recon_char.fit(X, Y)
    time_lapse = time() - start_time
    print(time_lapse)

    w = recon_char.coef_[0]
    b = recon_char.intercept_[0]

    num_suportv = recon_char.n_support_
    ind_suportv = recon_char.support_
    suport_vec = recon_char.support_vectors_


    # print(w, b, num_suportv, suport_vec)

    joblib.dump(recon_char, 'modelo_entrenado1.pkl')
    modelo_cargado = joblib.load('modelo_entrenado1.pkl')

    print('Probando la prediccion sobre la base de datos', recon_char.score(X, Y))
    print('Probando el modelo cargando sobre la base de datos', modelo_cargado.score(X, Y))


if __name__ == '__main__':
    run()
