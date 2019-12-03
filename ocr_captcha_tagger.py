import pytesseract
import os
import os.path
import glob
import cv2
import re


CAPTCHA_IMAGE_FOLDER = "dataset/examples/"
OUTPUT_FOLDER = "dataset/tagged_samples2/"

def text_pp(captcha_text):
	# Text pre-processing

	# Replace O because captcha only contains 0
	captcha_text = captcha_text.replace('O','0')

	# Remove any whitespace generated by the OCR 
	captcha_text = captcha_text.replace(' ','') 

	# Remove any non-alphanumeric character
	r = re.compile('[^a-zA-Z0-9]')
	captcha_text = r.sub('',captcha_text)

	# Convert any lowercase into uppercase
	captcha_text = captcha_text.upper() 

	return captcha_text

# Create output folder if not exist
if not os.path.exists(OUTPUT_FOLDER):
    	os.makedirs(OUTPUT_FOLDER)

# Obtain every image from source folder
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*.png"))

# Iterate over the images
for captcha_image_file in captcha_image_files:
	# Read the each image
	image = cv2.imread(captcha_image_file)

	# Obtain tesseract text prediction
	captcha_text = pytesseract.image_to_string(captcha_image_file)

	# Pre-process to avoid lowercase, whitespaces, etc
	captcha_text = text_pp(captcha_text)

	# Check if the OCR detects 6 characters, otherwise is not clean
	if len(captcha_text) != 6:
		continue

	# Create saving path with the predicted text as file name
	save_path = os.path.join(OUTPUT_FOLDER, captcha_text+".png")
	
	# Save the image
	cv2.imwrite(save_path, image)

	# Print image name
	print(save_path)