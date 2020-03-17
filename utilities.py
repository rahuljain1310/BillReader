import cv2
import numpy as np

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