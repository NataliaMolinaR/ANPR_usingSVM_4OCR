import csv
import numpy as np
import cv2


def cualquiervaina(character, counting_list):
    if ord(character) < ord('A'):
        counting_list[ord(character) - 48] += 1
    else:
        counting_list[ord(character) - 55] += 1


with open('./Pruebas1_DB.csv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter=";")
    fields = next(reader)
    notDetect = next(reader)
    db = list(reader);
    detection_mistake = []
    characters_detected = [0] * 36
    characters_recognized = [0] * 36
    error = [0] * 36
    success_perchar = [0] * 36
    for row in db:
        data = row
        ID = data[0]
        plate = data[1]
        char_detect = data[2]
        char_recon = data[3]
        # print(data, len(data))

        # if int(ID) == 229:
        #     print(plate, char_detect, char_recon)
        #     if char_detect == char_recon:
        #         print('son iguales')

        if len(plate) != len(char_detect):  # ID detection mistake
            diff = len(plate) - len(char_detect)
            detection_mistake.append(ID)

        for i in range(0, len(char_detect)):
            cualquiervaina(char_detect[i], characters_detected)
            if char_detect[i] == char_recon[i]:
                cualquiervaina(char_recon[i], characters_recognized)

    for i in range(0, len(characters_detected)):
        if characters_detected[i] != 0:
            error[i] = round((characters_detected[i] - characters_recognized[i]) / characters_detected[i], 3)
            success_perchar[i] = 1 - error[i]

    recogn_success = sum(characters_recognized) / sum(characters_detected)
    detection_success_rate = round(1 - len(detection_mistake) / len(db), 3)

    # print(detection_mistake)
    # print(characters_detected)
    print("Recognition success rate:", recogn_success)
    print("Recognition success rate p/char:", success_perchar)
    print("Detection success rate:", detection_success_rate, "IDs not detected:", detection_mistake)

    print('''\\begin{table}
\centering
\caption{Ejemplo}\label{Tab:producion}
\\begin{tabular}{lrrr}
\\toprule
Character & Success & Detected & Recognized \\\\
\midrule''')

    for i in range(0, 36):
        if i < 10:
            cadena = f' {chr(i+48)} & {success_perchar[i]} & {characters_detected[i]} & {characters_recognized[i]} \\\\'
        else:
            cadena = f' {chr(i + 55)} & {success_perchar[i]} & {characters_detected[i]} & {characters_recognized[i]} \\\\'

        print(cadena)
    print('''\\bottomrule
\end{tabular}
\end{table}''')
