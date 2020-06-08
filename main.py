import cv2
import math
import numpy as np
import pytesseract as pt
from sys import platform
from extract_knowledge import *
if platform == "linux" or platform == "linux2":
    pt.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
elif platform == "darwin":
    pt.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
elif platform == "win32":
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
    previous_VerCoord = H_List[0]['details']['center'][1]
    if abs(center_VerCoord-previous_VerCoord) < 12:
      print("Same Line", center_VerCoord, previous_VerCoord, patchDict['text'], H_List[0]['text'])
      H_List.append(patchDict)
    else:
      V_List.append(H_List)
      print("New Line", center_VerCoord, previous_VerCoord, patchDict['text'], H_List[0]['text'])
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


def filter_segments(gs):
	gs1 = []
	for g in gs:
		gs2 = []
		for i in g:
			gs3 = []
			for j in i:
				if (j['text'] is not ''):
					gs3.append(j)
			if (gs3 != []):
				gs2.append(gs3)
		if (gs2 != []):
			gs1.append(gs2)
	return gs1

import extract_knowledge
print(SegmentList)

def filter_result(kn):
	kl = dict()
	for k in kn.keys():
		kl[k] = kn[k]['text']
	return kl
def filter_group(gs):
	gs1 = []
	for g in gs:
		gs2 = []
		for i in g:
			gs2.append(i['text'])
		gs1.append(gs2)
	return gs1

def filter_knowledge(kn):
	gs1 = []
	for g in gs:
		# gs2 = []
		if (g.__class__==str):
			gs1.append(g['text'])
		elif (g.__class__==tuple):
			gs1.append((g[0]['text'],g[1]['text']))
		else:
			gs2 = []
			for i in g:
				gs2.append(i['text'])
			gs1.append(gs2)
	return gs1

def filter_knowledge2(kn):
	gs1 = []
	for g in gs:
		# gs2 = []
		if (g.__class__==str):
			gs1.append(g['text'])
		elif (g.__class__==tuple):
			gs1.append((g[0]['text'],g[1]['text']))
		else:
			gs2 = []
			output = False
			for i in g:
				gs2.append(i['text'])
				if (i['details']['isNumber']):
					output = True
				elif (output):
					break
			if (output):
				gs1.append(gs2)
	return gs1

def filter_list(gs):
	gs1 = []
	for g in gs:
		gs2 = []
		for i in g:
			gs3 = []
			for j in i:
				gs3.append(j['text'])
			gs2.append(gs3)
		gs1.append(gs2)
	return gs1

gs,kn  = extract_knowledge.extract(filter_segments(SegmentList))
gsf = filter_group(gs)

import io
def write_out(kn,file):
	with io.open(file,'w') as fl:
		for g in kn:
			if (g.__class__==str):
				fl.write(g)
				fl.write('\n')
			elif (g.__class__==tuple):
				fl.write('{'+g[0]['text'] + ' : ' + g[1]['text']+ '}')
				fl.write('\n')
			else:
				fl.write(g[0])
				for i in g[1:]:
					fl.write(',' + i)
				fl.write('\n')


write_out(filter_knowledge(kn),"output_all.txt")
write_out(filter_knowledge2(kn),"output_selected.txt")
## ========== For Results Show ===================

# MaskImg3 = np.repeat(MaskImg[...,None],3,axis=2)
# ResultMask =  np.where(MaskImg3, IMG, 0)
# segMask = GetColoredSegmentationMask(segLabel, segmentCount)

Rect_segLabel = getRectSegments(segLabel_Positions, maskShape = segLabel.shape)
# Rect_MaskImg = np.where(Rect_segLabel, 255, 0).astype(np.uint8)
# Rect_MaskImg3 = np.repeat(Rect_MaskImg[...,None],3,axis=2)
# Rect_ResultMask =  np.where(Rect_MaskImg3, IMG, 0)
Rect_segMask = GetColoredSegmentationMask(Rect_segLabel, segmentCount)

for V_List in SegmentList:
  for H_List in V_List:
    for patchDict in H_List:
        pos_coord = PatchInfo.getPosCoord(patchDict)
        text = patchDict['text']
        cv2.putText(Rect_segMask, text, (pos_coord[0], pos_coord[3]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (209, 80, 0, 255))
        
## ============= Save Image ==========================

saveImage([IMG, Rect_segMask], f'Visualizations/segMask{IMG_NO}')

### Clean Up ###
cv2.destroyAllWindows()