import PPIF as pf
import cv2


def extraction(source):

    character_kn = []

    for n_char in [7, 6]:
        for kn_blr in [11, 15, 9, 1]:

            no_noise = pf.softing_noise(source, kn_blr)
            resize, image_tocut = pf.resizing(no_noise, source, 150)
            to_detect, to_cut = pf.threshold_image(resize)
            contour, _ = cv2.findContours(to_detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            detecting, character = pf.detecting_characters(contour, resize, _)

            if len(character) == n_char:
                print('kernel es', kn_blr)
                break
        if not len(character) == n_char:
            continue

        break

    character = pf.org_character(character)
    to_cut = pf.preparing_tocut(image_tocut)
    segmented = pf.cutting_characters(character, to_cut)

    # for img in segmented:
    #
    #     # cv2.imwrite('./Base_datos/' + str(name_number) + '.jpg', img)
    #     name_number = name_number + 1

    return segmented

if __name__ == '__main__':
    extraction()