import cv2
import PIF as pif


def detecting_plate(imagen, number_car):

    plate = []
    num_file = number_car

    plate_detected = False
    cv2.destroyAllWindows()

    src = imagen

    cut_src = pif.resizing_image(src)

    s_noise = pif.softing_noise(cut_src, 5)

    thresh_image, _ = pif.threshold_image(s_noise)

    contour = pif.finding_contours(thresh_image)

    for c in contour:  # FIRST CASE SEARCHING THE PLATE RECTANGLE

        plate_detected, plate = pif.searching_plate(contour, cut_src, plate_detected, num_file)
        break

    for kn in [3, 5, 7]:         # SECOND CASE: THE IMAGE CONTOURS ARE EXPANDED TO FIND THE PLATE

        dilation = pif.dilating_image(thresh_image, kn, 1)

        contour_dilated = pif.finding_contours(dilation)

        for c in contour_dilated:

            x, y, w, h = cv2.boundingRect(c)

            plate_detected, plate = pif.searching_plate(contour_dilated, cut_src, plate_detected, num_file)
            break

        if plate_detected:
            break

    if not plate_detected:                     # THIRD CASE: REMOVE THE NOISE SMOOTHING AND DILATING TO SEARCH THE PLATE

        thresh_image, _ = pif.threshold_image(cut_src)
        contour = pif.finding_contours(thresh_image)

        for c in contour:
            x, y, w, h = cv2.boundingRect(c)

            plate_detected, plate = pif.searching_plate(contour, cut_src, plate_detected, num_file)
            print('Tercer caso')
            break

    return plate










