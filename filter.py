
from utilities import saveImage, GetColoredSegmentationMask, isText, getArea

def applyAreaFilter(segPositions, area, threshold = 0.5):
  """ Requires a list of pos_coord tuples """
  """ Output THose segmentations With Less Area """
  segPositions = segPositions[[getArea(pos_coord) < threshold *area for pos_coord in segPositions]]
  print("Segments After Eliminating Big Segments: ", len(segPositions))
  return segPositions
