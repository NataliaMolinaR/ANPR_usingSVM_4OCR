import csv
import numpy as np


def reading_data():
    with open('./data_base1.csv', 'r', newline='') as file:
        reader = csv.reader(file, delimiter=";")
        examples_count = np.zeros(36, dtype=np.int16)
        for row in reader:
            index = int(row[405])
            if index <= 35:
                examples_count[index] += 1

        for i in range(0, 36):
            if i < 10:
                print(i, examples_count[i])
            else:
                print(chr(55+i), examples_count[i])

    return examples_count


def run():
    examples_count = reading_data()



if __name__ == '__main__':
    run()
