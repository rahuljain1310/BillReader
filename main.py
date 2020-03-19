import cv2
import numpy as np
from utilities import saveImage, GetColoredSegmentationMask
from segTask import getSegments, getMask, getSegmentPositions, getRectSegments
from collections import deque

## Read Image
for IMG_NO in range(5,11):
	img = cv2.imread(f'Invoices/invoices ({IMG_NO}).jpg')
	print("Image Shape: ",img.shape)

	MaskImg = getMask(img, fSize=3)
	MaskImg3 = np.repeat(MaskImg[...,None],3,axis=2)
	ResultMask =  np.where(MaskImg3, img, 0)
	segLabel, segmentCount = getSegments(MaskImg)
	segMask = GetColoredSegmentationMask(segLabel, segmentCount)
	# saveImage([img,MaskImg3,ResultMask, segMask], f'segMask{IMG_NO}')

	segLabel_Pos = getSegmentPositions(segLabel, segmentCount)
	Rect_segLabel = getRectSegments(segLabel_Pos, maskShape = segLabel.shape)
	Rect_MaskImg = np.where(Rect_segLabel, 255, 0).astype(np.uint8)
	Rect_MaskImg3 = np.repeat(Rect_MaskImg[...,None],3,axis=2)
	Rect_ResultMask =  np.where(Rect_MaskImg3, img, 0)
	Rect_segMask = GetColoredSegmentationMask(Rect_segLabel, segmentCount)
	saveImage([img, segMask, ResultMask, Rect_segMask], f'Visualizations/segMask{IMG_NO}')

### Clean Up ###
cv2.destroyAllWindows()