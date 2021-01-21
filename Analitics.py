import csv
import numpy as np
import cv2


def str2num(character, counting_list):
    if ord(character) < ord('A'):
        counting_list[ord(character) - 48] += 1
    else:
        counting_list[ord(character) - 55] += 1


with open('./Pruebas1_DB.csv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter=";")
    fields = next(reader)
    notDetect = next(reader)
    db = list(reader)
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

        if len(plate) != len(char_detect):          #ID detection mistake
            diff = len(plate) - len(char_detect)
            detection_mistake.append(ID)

        for i in range(0, len(char_detect)):
            str2num(char_detect[i], characters_detected)

            if char_detect[i] == char_recon[i]:
                str2num(char_recon[i], characters_recognized)

    for i in range(0, len(characters_detected)-1):
        if characters_detected[i] != 0:
            error[i] = round((characters_detected[i] - characters_recognized[i])/characters_detected[i], 3)
            success_perchar[i] = 1 - error[i]

    recogn_success = sum(characters_recognized)/sum(characters_detected)
    detection_success_rate = round(1-len(detection_mistake)/len(db), 3)

    # print(characters_detected)
    print("Recognition sucess rate:", recogn_success)
    print("Recognition sucess char detected", characters_detected)
    print("Recognition sucess char reconigzed", characters_recognized)
    print("Recognition sucess rate p/char:", success_perchar)
    print("Detection sucess rate:", detection_success_rate, "IDs not detected:", detection_mistake)





