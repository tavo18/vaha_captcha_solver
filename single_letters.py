import cv2
import imutils
import sys
import numpy as np
import glob
import os
import os.path

CAPTCHA_IMAGE_FOLDER = "dataset/correct_tagged_captchas/"
OUTPUT_FOLDER = "dataset/extracted_letter_images"

captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*.png"))

counts = {}

for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))

    # Since the filename contains the captcha text (i.e. "2A2X2Q.png" has the text "2A2X2Q"),
    # grab the base filename as the text
    filename = os.path.basename(captcha_image_file)
    captcha_correct_text = os.path.splitext(filename)[0]

    image = cv2.imread(captcha_image_file)

    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

    # gray = cv2.copyMakeBorder(gray, 3, 3, 3, 3, cv2.BORDER_REPLICATE)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    # Dilate image in order to delete sliced parts
    kernel = np.ones((2,1), np.uint8)
    img_dilate = cv2.dilate(thresh,kernel,iterations = 1)

    # Find all contours
    contours = cv2.findContours(img_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[1] if imutils.is_cv3() else contours[0]


    letter_image_regions = []
    # Now we can loop through each of the four contours and extract the letter
    # inside of each one
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        if w / h > 1.25:
            # This contour is too wide to be a single letter!
            # Split it in half into two letter regions!
            half_width = int(w / 2)
            letter_image_regions.append((x, y, half_width, h))
            letter_image_regions.append((x + half_width, y, half_width, h))
        else:
            # This is a normal letter by itself
            letter_image_regions.append((x, y, w, h))

    if len(letter_image_regions) != 6:
    	continue

    # Sort the detected letter images based on the x coordinate to make sure
    # we are processing them from left-to-right so we match the right image
    # with the right letter
    letter_image_regions = sorted(letter_image_regions, key=lambda x: x[0])


    for letter_bounding_box, letter_text in zip(letter_image_regions, captcha_correct_text):
        # Grab the coordinates of the letter in the image
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 2:y + h + 2, x - 2:x + w + 2]

        # Get the folder to save the image in
        save_path = os.path.join(OUTPUT_FOLDER, letter_text)

        # if the output directory does not exist, create it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, letter_image)

        # increment the count for the current key
        counts[letter_text] = count + 1


