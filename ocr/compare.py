import math
import time

import easyocr
import numpy as np
import pyautogui
from PIL import ImageGrab
from matplotlib import pyplot as plt


class FormulaRecognition:

	def __init__(self, im: np.ndarray):
		self.im = im
		self.reader = easyocr.Reader(['en'])

	def get_lhs_and_result(self, logging=True) -> str:
		bbox1 = (260, 300, 420, 340)
		im1 = FormulaLocator(bbox1).get_formula_area(logging=False)
		result = self.reader.readtext(im1)
		if logging:
			print(f"{result=}")
		res = []
		for item in result:
			res.append(item[-2])
		return " ".join(res)


class FormulaLocator:

	def __init__(self, binding_box):
		self.bbox = binding_box

	def get_formula_area(self, logging=True) -> np.ndarray:
		screenshot = ImageGrab.grab(bbox=self.bbox)
		# screenshot = screenshot.resize((500, 300))
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


class DrawLine:

	def __init__(self, start_pos: tuple[int, int], line_length: int, radians: int):
		self.start_pos = start_pos
		self.end_pos = (start_pos[0] + line_length * math.cos(math.radians(radians)),
						start_pos[1] + line_length * math.sin(math.radians(radians)))

	def write(self):
		x1, y1 = self.start_pos
		x2, y2 = self.end_pos
		pyautogui.moveTo(x1, y1)
		pyautogui.mouseDown()
		pyautogui.dragTo(x2, y2, button='left')
		pyautogui.mouseUp()


def greater(origin_x=350, origin_y=500, size=20, draw_duration=0.0):
	pyautogui.mouseDown(origin_x, origin_y)
	pyautogui.moveTo(origin_x + size, origin_y + size, duration=draw_duration)
	pyautogui.moveTo(origin_x, origin_y + size, duration=draw_duration)
	pyautogui.mouseUp()


def less(origin_x=350, origin_y=500, size=20, draw_duration=0.0):
	pyautogui.mouseDown(origin_x + size, origin_y)
	pyautogui.moveTo(origin_x, origin_y + size, duration=draw_duration)
	pyautogui.moveTo(origin_x + size, origin_y + size, duration=draw_duration)
	pyautogui.mouseUp()


if __name__ == '__main__':
	# for i in range(6):
	last = None
	while True:
		try:
			bbox1 = (260, 300, 420, 340)
			im1 = FormulaLocator(bbox1).get_formula_area(logging=False)
			plt.imshow(im1)
			plt.show()
			data = FormulaRecognition(im1).get_lhs_and_result().split()
			if data == last:
				time.sleep(1)
				last = None
				continue
			last = data
			print(f"{data=}")
			if len(data) == 2:
				lhs, rhs = data
				if int(lhs) > int(rhs):
					greater()
				else:
					less()
			elif len(data) > 2:
				lhs = data[0]
				rhs = data[-1]
				if int(lhs) > int(rhs):
					greater()
				else:
					less()
			elif len(data) == 1:
				lhs, rhs = map(int, (str(data[0]).split('7')))
				if lhs > rhs:
					greater()
				else:
					less()
			else:
				print("识别失败")
		except Exception as e:
			plt.show()
			print(e, flush=True)
		finally:
			time.sleep(0.2)
