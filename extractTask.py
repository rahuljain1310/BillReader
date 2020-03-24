import cv2
import numpy as np
import pytesseract as pt

from utilities import saveImage, GetColoredSegmentationMask, isText
from segTask import getSegments, getMask, getSegmentPositions, getRectSegments
from collections import deque
from patchInfo import PatchInfo

""" 1. Remove Patches With Large Fonts
    2. Sort Patches With Coordinate of the center of the patch
    3. Remove Patches With Icons - Make a list of Patches from given Bills
    4. Histogram Equilize Image for better clarity and OCR reading
    5. Join All Texts and check for Details - Currency
"""

def getCurrencyType(TextList):
  return None