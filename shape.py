import cv2

def getDimension (IMG) :
  height = IMG.shape[0]
  width = IMG.shape[1]
  area = height*width
  print("Image Shape: ",IMG.shape)
  return height, width, area