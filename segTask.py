import numpy as np
import cv2
from collections import deque

def getMask(img, fSize = 7):
	filter2D_n = -1*np.ones((fSize,fSize))
	filter2D_n[fSize//2][fSize//2] = fSize*fSize-1
	morphKernel = np.ones((3,3), np.uint8)
	morphKernel_Hor = np.array([[1,1,1]])

	MaskImg = cv2.filter2D(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), -1, filter2D_n)
	MaskImg[MaskImg!=0] == 1
	# MaskImg = cv2.morphologyEx(MaskImg, cv2.MORPH_CLOSE, morphKernel, iterations=1)
	MaskImg = cv2.morphologyEx(MaskImg, cv2.MORPH_CLOSE, morphKernel_Hor, iterations=2)
	MaskImg = cv2.dilate(MaskImg, morphKernel_Hor, iterations=3)
	return MaskImg

def getSegments(masks):
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
	h, w = masks.shape
	segLabel = np.where(masks,-1, 0)
	segLabel[0,:] = 0
	segLabel[h-1,:] = 0
	segLabel[:,0] = 0
	segLabel[:,w-1] = 0
	for i in range(1,h-1):
		for j in range(1,w-1):
			if segLabel[i][j] == -1:
				segmentCount += 1
				MarkSegment(segLabel, i, j ,segmentCount)
	print("Total Segments Found: ", segmentCount)
	return segLabel, segmentCount

def getSegmentPositions(segLabel, segmentCount):
	h,w = segLabel.shape
	minX = np.repeat(w,segmentCount)
	maxX = np.repeat(0,segmentCount)
	minY = np.repeat(h,segmentCount)
	maxY = np.repeat(0,segmentCount)
	for i in range(1,h-1):
		for j in range(1,w-1):
			if segLabel[i][j] > 0:
				label = segLabel[i][j]
				if j<minX[label-1]: minX[label-1]=j
				if j>maxX[label-1]: maxX[label-1]=j
				if i<minY[label-1]: minY[label-1]=i
				if i>maxY[label-1]: maxY[label-1]=i
	pos = np.column_stack((minX, maxX, minY, maxY))
	return pos
	
def getRectSegments(segLabel_Pos, maskShape):
	segLabelMask = np.zeros(maskShape)
	for segmentCount in range(0,segLabel_Pos.shape[0]):
		minX, maxX, minY, maxY = segLabel_Pos[segmentCount]
		segLabelMask[minY:maxY+1,minX: maxX+1] = segmentCount+1
	return segLabelMask
	 