import cv2
import numpy as np
import utilities as utl
from collections import deque

def showImage(img, imgName):
	resimg = img[0]
	for idx in range(1,len(img)):
		resimg = cv2.hconcat((resimg,img[idx]))
	cv2.imwrite(f'{imgName}.png', resimg)

## Read Image
IMG_NO = 2
img = cv2.imread(f'Invoices/invoices ({IMG_NO}).jpg')
print("Image Shape: ",img.shape)

## Filters
n = 7
filter2D_n = -1*np.ones((n,n))
filter2D_n[n//2][n//2] = n*n-1
morphKernel = np.ones((5,5), np.uint8)

## Apply Filter
filterImg = cv2.filter2D(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), -1, filter2D_n)
filterImg[filterImg==0] == 0
filterImg[filterImg!=0] == 1
filterImg = cv2.morphologyEx(filterImg, cv2.MORPH_CLOSE, morphKernel)

## Save Image
imgFil3 = np.repeat(filterImg[...,None],3,axis=2)
img1 =  np.where(imgFil3, img, 0)
showImage([img,imgFil3,img1], 'img')


def MarkSegment(seg, i, j, segmentCount):
	queue = deque()
	queue.append((i,j))
	while len(queue):
		i, j = queue.pop()
		seg[i][j] = segmentCount
		if seg[i-1][j] == -1: queue.append((i-1,j))
		if seg[i+1][j] == -1: queue.append((i+1,j))
		if seg[i][j+1] == -1: queue.append((i,j+1))
		if seg[i][j-1] == -1: queue.append((i,j-1))
	return 

segmentCount = 0
h, w = filterImg.shape
segLabel = np.where(filterImg,-1, 0)
for i in range(1,h-1):
	for j in range(1,w-1):
		if segLabel[i][j] == -1:
			segmentCount += 1
			print(segmentCount, end='\r', flush = True)
			MarkSegment(segLabel, i, j ,segmentCount)



print(np.any(segLabel<0), np.any(segLabel>255), segmentCount)
seg = utl.GetColoredSegmentationMask(segLabel, segmentCount)
showImage([seg], 'seg')

### Clean Up ###
cv2.destroyAllWindows()