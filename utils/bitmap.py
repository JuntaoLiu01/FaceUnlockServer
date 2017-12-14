import cv2
import numpy as np
import struct

def img_to_bit(image):
	rows = image.shape[0]
	cols = image.shape[1]
	channels = image.shape[2]

	fileSave = open('patch.bin','wb')
	for i in range(0,rows):
		for j in range(0,cols):
			fileSave.write(image[i,j,2])
	for i in range(0,rows):
		for j in range(0,cols):
			fileSave.write(image[i,j,1])
	for i in range(0,rows):
		for j in range(0,cols):
			fileSave.write(image[i,j,0])
	fileSave.close()

def bit_to_img(imageRead):
	rows = imageRead.shape[0]
	cols = imageRead.shape[1]
	fileReader = open('patch.bin','rb')
	for i in range(0,rows):
		for j in range(0,cols):
			a = struct.unpack("B",fileReader.read(1))
			imageRead[i,j,2] = a[0]
	for i in range(0,rows):
		for j in range(0,cols):
			a = struct.unpack("B",fileReader.read(1))
			imageRead[i,j,1] = a[0]
	for i in range(0,rows):
		for j in range(0,cols):
			a = struct.unpack("B",fileReader.read(1))
			imageRead[i,j,0] = a[0]
	fileReader.close()



image = cv2.imread("2.jpg")
imageRead = np.zeros(image.shape,np.uint8)
img_to_bit(image)
bit_to_img(imageRead)

cv2.imshow("src",image)
cv2.imshow("dst",imageRead)
cv2.waitKey(0)
cv2.destroyAllWindows()