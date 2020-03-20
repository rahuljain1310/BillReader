import cv2
import numpy as np
import pandas as pd
import pytesseract as pt
import utilities as utl
import infoRepo as ir

class PatchInfo:
	def __init__(self, img, pos_coord = None, idx=None):
		minX, maxX, minY, maxY = pos_coord
		self.idx = idx
		self.img = img
		self.pos_coord = pos_coord
		self.Height = self.img.shape[0]
		self.Width = self.img.shape[1]
		self.text = self.extractText()
		self.isLine = None
		self.isBetweenLines = False
		self.parent = None
		self.siblings = None
		self.isNumber = None

	def extractText(self):
		""" Extract Patch, Equilize The Image, Try With Different Padding Size """
		for pad in range(1,9):
			img_ = utl.getPatch(self.img, self.pos_coord, pad)
			equ = cv2.equalizeHist(img_)
			self.text = utl.getText(equ)
			if self.text is not None: break

	def isText(self):
		return (self.text is not "")

	def checkKeyword(self):
		if self.text[-1] == ":":
			self.text = self.text[:-1]
			self.isKeyword = True
			return
		self.isKeyword = False

	def checkHeader(self):
		self.isHeader = False

	def findTextInfo(self):
		""" Extract Information """
		if self.text == "": return
		self.checkKeyword()
		self.checkHeader()




