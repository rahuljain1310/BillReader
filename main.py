import cv2
import math
import numpy as np
import pytesseract as pt

pt.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

from utilities import saveImage, GetColoredSegmentationMask, isText, getArea, getPostionFromFilter
from segTask import getSegments, getMask, getSegmentPositions, getRectSegments
from filter import applyAreaFilter
from collections import deque
from patchInfo import PatchInfo
from shape import getDimension

## ===================== Read Image ========================
IMG_NO  = 2
IMG = cv2.imread(f'Invoices/invoices ({IMG_NO}).jpg')
IMG_GRAY = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
IMG_HEIGHT, IMG_WIDTH, IMG_AREA = getDimension(IMG)


## ========= Create Segments AND Get Coordinates ===========

MaskImg = getMask(IMG, fSize=3)
segLabel, segmentCount = getSegments(MaskImg)
segLabel_Positions = getSegmentPositions(segLabel, segmentCount)
segLabel_Positions = applyAreaFilter(segLabel_Positions, IMG_AREA)

PatchInfoList = [PatchInfo(IMG_GRAY, segment) for segment in segLabel_Positions]
segLabelPatchList = [patch.getPatchDict() for patch in PatchInfoList ]
sorted(segLabelPatchList, key = lambda patchDict: patchDict['details']['center'][0])
segLabel_Positions = getPostionFromFilter(segLabelPatchList)

def get2DSorted(Segment):
  V_List = list()
  H_List = list()
  H_List.append(Segment[0])
  for patchDict in Segment[1:]:
    center_VerCoord = patchDict['details']['center'][1]
    previous_VerCoord = H_List[-1]['details']['center'][1]
    if abs(center_VerCoord-previous_VerCoord) < 4:
      H_List.append(patchDict)
    else:
      V_List.append(H_List)
      H_List = [patchDict]
  if (len(H_List) > 0):
    V_List.append(H_List)
  return V_List

SegmentList = list()
Segment = list()
for patchDict in segLabelPatchList:
  if patchDict['details']['isLine'] == True:
    if (len(Segment) > 0):
      Segment2D = get2DSorted(Segment)
      SegmentList.append(Segment2D)
      Segment = list()
  else:
    Segment.append(patchDict)

if (len(Segment) > 0):
  Segment2D = get2DSorted(Segment)
  SegmentList.append(Segment2D)

print(SegmentList)

## ========== For Results Show ===================

# MaskImg3 = np.repeat(MaskImg[...,None],3,axis=2)
# ResultMask =  np.where(MaskImg3, IMG, 0)
# segMask = GetColoredSegmentationMask(segLabel, segmentCount)

Rect_segLabel = getRectSegments(segLabel_Positions, maskShape = segLabel.shape)
# Rect_MaskImg = np.where(Rect_segLabel, 255, 0).astype(np.uint8)
# Rect_MaskImg3 = np.repeat(Rect_MaskImg[...,None],3,axis=2)
# Rect_ResultMask =  np.where(Rect_MaskImg3, IMG, 0)
Rect_segMask = GetColoredSegmentationMask(Rect_segLabel, segmentCount)

## ============= Save Image ==========================

saveImage([IMG, Rect_segMask], f'Visualizations/segMask{IMG_NO}')

### Clean Up ###
cv2.destroyAllWindows()