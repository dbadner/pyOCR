# import the necessary packages
from PIL import Image
from pytesseract import Output
import pytesseract
import argparse
import cv2
import os

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files/Tesseract-OCR'

#custom options
custom_config = '--psm 6' #11

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#hack temporary hard code for debugging
ap.add_argument("-i", "--image", required=False, default="input/17316.png",
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="stdout",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)
# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)



# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(Image.open(filename), config=custom_config)
os.remove(filename)
print(text)
file1 = open(r"output/TessOut.txt","w+")
file1.write(text)
file1.close()

# show the input image
cv2.imshow("image.jpg", image)

d = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
n_boxes = len(d['left'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

#write text output
file2 = open(r"output/TessOutData.txt","w+")
for i in range(len(d['text'])):
	file2.write('{0}: '.format(i)+d['text'][i]+'\n')
file2.close()

# show the output image
                   # Read image
cv2.namedWindow("Output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
imS = cv2.resize(gray, (960, 540))                    # Resize image
cv2.imshow("Output", imS)                            # Show image
#cv2.imshow("Output", gray)



img = cv2.imread(args["image"])

h, w, c = img.shape
boxes = pytesseract.image_to_boxes(img, config=custom_config)
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

cv2.imshow('img', img)

cv2.waitKey(0)

