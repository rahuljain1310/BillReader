import cv2
import numpy as np
import pytesseract as pt

def saveImage(img, imgName):
	""" Concates horizontally Images: Save as PNG """
	resimg = img[0]
	for idx in range(1,len(img)):
		resimg = cv2.hconcat((resimg,img[idx]))
	cv2.imwrite(f'{imgName}.png', resimg)

def GetColoredSegmentationMask(seg, segmentCount):
	""" Return a colored segmented image """
	colors = [tuple(np.random.randint(256, size=3)) for _ in range(256)]
	seg = seg%256
	seg = cv2.cvtColor(seg.astype(np.uint8), cv2.COLOR_GRAY2RGB)
	seg_img = np.zeros_like(seg)
	for c in range(1,len(colors)):
			seg_img[:, :, 0] += ((seg[:, :, 0] == c) * (colors[c][0])).astype('uint8')
			seg_img[:, :, 1] += ((seg[:, :, 0] == c) * (colors[c][1])).astype('uint8')
			seg_img[:, :, 2] += ((seg[:, :, 0] == c) * (colors[c][2])).astype('uint8')
	return seg_img

def getArea(pos_coord):
  minX, maxX, minY, maxY = pos_coord
  return (maxX-minX)*(maxY-minY)

def getPatch(img, pos_coord, pad=2):
	""" Get Patch from Image and Coordinates Positions """
	minX, maxX, minY, maxY = pos_coord
	return img[minY-pad:maxY+1+pad,minX-pad: maxX+1+pad]
	
def getText(img): return pt.image_to_string(img)
def getPatchText(img,pos_coord,pad=2): return getText(getPatch(img,pos_coord,pad))
def isText(img, pos_coord, pad=2): return (getPatchText(img,pos_coord,pad) is not "")
