import cv2
import numpy as np
import pandas as pd
import pytesseract as pt
import utilities as utl
import infoRepo as ir

class PatchInfo:
	def __init__(self, img, pos_coord = None):
		minX, maxX, minY, maxY = pos_coord
		self.details = {
			'center': ((minX+maxX)/2, (minY+maxY)/2),
			'height': img.shape[0],
			'width': img.shape[1],
			'isLine': False,
			'isCurrency': False,
			'isNumber': False,
			'isDate': False,
			'isKeyword': False,
		}
		self.pos_coord = {
			'minX': minX,
			'maxX': maxX,
			'minY': minY,
			'maxY': maxY
		}
		self.text = self.extractText(img, pos_coord)
		self.findTextInfo()
		self.findDetails()

	@staticmethod
	def getPosCoord(patchDict):
		pos_coord_dict = patchDict['point']
		minX = pos_coord_dict['minX']
		maxX = pos_coord_dict['maxX']
		minY = pos_coord_dict['minY']
		maxY = pos_coord_dict['maxY']
		return (minX, maxX, minY, maxY)

	def getPatchDict(self):
		res = dict()
		res['text'] = self.text
		res['details'] = self.details
		res['point'] = self.pos_coord
		return res

	def extractText(self, img, pos_coord):
		""" Extract Patch => Try Different Padding => Equilize"""
		for pad in range(1,9):
			img_ = utl.getPatch(img, pos_coord, pad)
			equ = cv2.equalizeHist(img_)
			text = utl.getText(equ)
			if text is not "": return text
		return ""

	def findDetails(self):
		if self.text == "":
			self.checkLine()

	def findTextInfo(self):
		if self.text is not "":
			self.checkKeyword()
			self.checkNumber()

	def checkLine(self):
		isLine = self.details['width'] > 100 * self.details['height']
		self.details['isLine'] = isLine

	def checkKeyword(self):
		if self.text[-1] == ":":
			self.text = self.text[:-1]
			self.details['isKeyword'] = True
		if (self.text.lower() in ir.Keywords):
			self.details['isKeyWord'] = True

	def checkNumber(self):
		charsDate = set('0123456789/-')
		charsNumeric = set('0123456789.')
		charsCurrency = set('$₹¥€£0123456789,.')
		self.details['isCurrency'] = all((c in charsCurrency) for c in self.text)
		self.details['isDate'] = all((c in charsDate) for c in self.text)
		self.details['isNumber'] = all((c in charsNumeric) for c in self.text) or self.details['isCurrency']






