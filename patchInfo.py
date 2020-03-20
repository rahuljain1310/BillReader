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
		self.textDict = dict()

	def extractText(self):
		""" Extract Patch, Equilize The Image, Try With Different Padding Size """
		for pad in range(1,9):
			print(self.pos_coord)
			img_ = utl.getPatch(self.img, self.pos_coord, pad)
			print(img_.shape)
			cv2.imshow('img_', img_)
			equ = cv2.equalizeHist(img_)
			cv2.imshow('eqy', equ)
			cv2.waitKey(2000)
			self.text = utl.getText(equ)
			if self.text is not None: break

	def isText(self): return (self.text is not "")
	def isHeader(self): return (self.text in ir.HeaderBag)

	def findTextInfo(self):
		""" Extract Information """
		if self.text == "": return
		self.textDict['isKeyword'] = self.isKeyword()
		self.textDict['isHeader'] = self.isHeader()
		self.textDict['isKeyword'] = self.isKeyWord()



