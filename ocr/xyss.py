import re

import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import ImageGrab
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


class FormulaRecognition:

	def __init__(self, im: np.ndarray):
		self.im = im

	def get_lhs_and_result(self, logging=True) -> tuple[int, int]:
		gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
		text = pytesseract.image_to_string(gray, config='--psm 7 --oem 3 -c tessedit_char_whitelist==x-0123456789')
		if logging:
			print(f"{text = } ")
		return int(re.findall(r'\d+', text)[0]), int(re.findall(r'\d+', text)[1])


class FormulaLocator:

	def __init__(self, binding_box):
		self.bbox = binding_box

	def get_formula_area(self, logging=True) -> np.ndarray:
		screenshot = ImageGrab.grab(bbox=self.bbox)
		if logging:
			plt.imshow(np.array(screenshot))
			plt.show()
		return np.array(screenshot)


class HorizontalLine:

	def __init__(self, pos: tuple[int, int], length: int):
		self.pos = pos
		self.length = length

	def write(self):
		x, y = self.pos
		pyautogui.moveTo(x, y)
		pyautogui.mouseDown()
		ex, ey = x + self.length, y
		pyautogui.dragTo(ex, ey, duration=0.01, button='left')
		pyautogui.mouseUp()


class VerticalLine:

	def __init__(self, pos: tuple[int, int], length: int):
		self.pos = pos
		self.length = length

	def write(self):
		x, y = self.pos
		pyautogui.moveTo(x, y)
		pyautogui.mouseDown()
		ex, ey = x, y + self.length
		pyautogui.dragTo(ex, ey, duration=0.01, button='left')
		pyautogui.mouseUp()


class SingleNumberWriter:

	def __init__(self, n, pos: tuple[int, int], box: tuple[int, int]):
		self.n = n
		self.box = box
		self.pos = pos

	def write(self):
		sx, sy = self.pos
		W, L = self.box
		match self.n:
			case 1:
				VerticalLine((sx + W // 2, sy), L).write()
			case 2:
				HorizontalLine((sx, sy), W).write()
				VerticalLine((sx + W, sy), L // 2).write()
				HorizontalLine((sx, sy + L // 2), W).write()
				VerticalLine((sx, sy + L // 2), L // 2).write()
				HorizontalLine((sx, sy + L), W).write()
			case 3:
				HorizontalLine((sx, sy), W).write()
				VerticalLine((sx, sy + W), L).write()
				HorizontalLine((sx + L, sy), W).write()


class ResultWriter:

	def __init__(self, bbox, num):
		self.bbox = bbox
		self.num = str(num)

	def write(self):
		pass


if __name__ == '__main__':
	bbox = (200, 300, 500, 350)
	im = FormulaLocator(bbox).get_formula_area(logging=False)
	plt.imshow(im)
	plt.show()
	print(FormulaRecognition(im).get_lhs_and_result())

# HorizontalLine((250, 300), 40).write()
# VerticalLine((250, 300), 40).write()
# SingleNumberWriter(2, (250, 450), (40, 40)).write()
