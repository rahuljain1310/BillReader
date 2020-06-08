import cv2
import numpy as np
import pytesseract as pt

pt.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

from utilities import saveImage, GetColoredSegmentationMask, isText, getArea
from segTask import getSegments, getMask, getSegmentPositions, getRectSegments
from collections import deque
from patchInfo import PatchInfo
from shape import getDimension

## Read Image
IMG_NO  = 2
IMG = cv2.imread(f'Invoices/invoices ({IMG_NO}).jpg')
IMG_GRAY = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
IMG_HEIGHT, IMG_WIDTH, IMG_AREA = getDimension(IMG)

MaskImg = getMask(IMG, fSize=3)
MaskImg3 = np.repeat(MaskImg[...,None],3,axis=2)
ResultMask =  np.where(MaskImg3, IMG, 0)
segLabel, segmentCount = getSegments(MaskImg)
segMask = GetColoredSegmentationMask(segLabel, segmentCount)

segLabel_Positions = getSegmentPositions(segLabel, segmentCount)

infoDict = dict()

## We need to remove the boxes which cover the entire Page, Maybe Neglect Them
segLabel_Positions = segLabel_Positions[[getArea(pos_coord) < 0.5 *IMG_AREA for pos_coord in segLabel_Positions]]
print("Segments After Eliminating Big Segments: ", len(segLabel_Positions))

Rect_segLabel = getRectSegments(segLabel_Positions, maskShape = segLabel.shape)
Rect_MaskImg = np.where(Rect_segLabel, 255, 0).astype(np.uint8)
Rect_MaskImg3 = np.repeat(Rect_MaskImg[...,None],3,axis=2)
Rect_ResultMask =  np.where(Rect_MaskImg3, IMG, 0)
Rect_segMask = GetColoredSegmentationMask(Rect_segLabel, segmentCount)

PatchInfoList = [PatchInfo(IMG_GRAY, segLabel_Positions[idx], idx) for idx in range(len(segLabel_Positions))]
segLabel_Pos_filter = segLabel_Positions[[ x.isText() for x in PatchInfoList ]]
print("Segments After Eliminating Segments With No Text: ", len(segLabel_Pos_filter))

Rect_segLabel_filter = getRectSegments(segLabel_Pos_filter, maskShape = segLabel.shape)
Rect_segMask_filter = GetColoredSegmentationMask(Rect_segLabel_filter, segmentCount)
saveImage([IMG, Rect_ResultMask, Rect_segMask_filter], f'Visualizations/segMask{IMG_NO}')

### Clean Up ###
cv2.destroyAllWindows()