
from utilities import saveImage, GetColoredSegmentationMask, isText, getArea

def applyAreaFilter(segPositions, area, threshold = 0.3):
  """ Requires a list of pos_coord tuples """
  """ Output THose segmentations With Less Area """
  segPositions = segPositions[[getArea(pos_coord) < threshold *area for pos_coord in segPositions]]
  print("Segments After Eliminating Big Segments: ", len(segPositions))
  return segPositions

def applyCoverFilter(segPositions):
  length = len(segPositions)
  res = list()
  for i in range(length):
    minX, maxX, minY, maxY = segPositions[i]
    for f in segPositions:
      minX1, maxX1, minY1, maxY1 = f
      if (minX1>=minX and maxX1<=maxX and minY1>=minY and maxY1<=maxY):
        res.append(segPositions[i])
        break
  return res

def filterHlist(H_List):
  length = len(H_List)
  sumArea = 0
  for i in range(length):
    sumArea = sumArea + H_List[i]['details']['area']
  res = list()
  for c in H_List:
    area = c['details']['area']
    if (area < sumArea/2): res.append(c)
  return res