import math
import random
import pickle
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
SIZE = 40 # Grid unit size
SPEED = 10 # Higher is faster

window = pygame.display.set_mode((SCREEN_WIDTH - SCREEN_WIDTH%SIZE, SCREEN_HEIGHT - SCREEN_HEIGHT%SIZE))


class block(object):
	def __init__(self, index_x, index_y, color):
		self.index_x = index_x
		self.index_y = index_y
		self.color = color

	def draw(self, win):
		x_coor = self.index_x * SIZE
		y_coor = self.index_y * SIZE
		pygame.draw.rect(win, self.color, (int(x_coor), int(y_coor), SIZE, SIZE))


class snake(object):
	body = []
	body_info = []
	def __init__(self, start_x, start_y, color=(0,255,0)):
		self.color = color
		self.body.append(block(start_x, start_y, self.color))
		self.body_info.append([start_x, start_y])
		self.x_dir = 1
		self.y_dir = 0

	def move(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] and self.x_dir == 0:
			self.y_dir = 0
			self.x_dir = -1
		elif keys[pygame.K_RIGHT] and self.x_dir == 0:
			self.y_dir = 0
			self.x_dir = 1
		elif keys[pygame.K_UP] and self.y_dir == 0:
			self.x_dir = 0
			self.y_dir = -1
		elif keys[pygame.K_DOWN] and self.y_dir == 0:
			self.x_dir = 0
			self.y_dir = 1

		head_x = self.body[-1].index_x
		head_y = self.body[-1].index_y
		new_head_x = head_x + self.x_dir
		new_head_y = head_y + self.y_dir

		if new_head_x >= int(SCREEN_WIDTH / SIZE):
			new_head_x = 0
		if new_head_x < 0:
			new_head_x = int(SCREEN_WIDTH / SIZE) -1
		if new_head_y >= int(SCREEN_HEIGHT / SIZE):
			new_head_y = 0
		if new_head_y < 0:
			new_head_y = int(SCREEN_HEIGHT / SIZE) - 1

		return new_head_x, new_head_y

	def grow(self, new_head_x, new_head_y):
		self.body.append(block(new_head_x, new_head_y, self.color))
		self.body_info.append([new_head_x, new_head_y])

	def draw(self, win):
		for block in self.body:
			block.draw(win)

	def reset(self, reset_x, reset_y, color=(0, 255, 0)):
		self.color = color
		self.body = [block(reset_x, reset_y, self.color)]
		self.body_info = [[reset_x, reset_y]]


def randomFood(player_snake, screen_w, screen_h, length):
	while True:
		x_max = int(screen_w / length) - 1
		y_max = int(screen_h / length) - 1
		x = random.randint(0, x_max)
		y = random.randint(0, y_max)

		new_food = block(x, y, (0,255,0))
		if new_food not in player_snake.body:
			break

	new_food.color = (255,0,0)
	return new_food


def sendMessage(title, message):
	root = tk.Tk()
	root.withdraw()
	messagebox.showerror(title, message)
	try:
		root.destroy()
	except:
		pass


def drawWindow(s, food, win):
	win.fill((0, 0, 0))
	s.draw(win)
	food.draw(win)
	pygame.display.update()


if __name__ == '__main__':
	clock = pygame.time.Clock()
	run = True
	s = snake(10, 10)
	food = randomFood(s, SCREEN_WIDTH, SCREEN_HEIGHT, SIZE)

	while run:
		clock.tick(60 * SPEED / SIZE)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		x, y = s.move()

		if [x, y] in s.body_info and len(s.body) > 1:
			sendMessage('Snake Game', f'You have died at score {len(s.body)}')
			s.reset(x, y)
			continue

		s.grow(x, y)

		if [food.index_x, food.index_y] in s.body_info:
			food = randomFood(s, SCREEN_WIDTH, SCREEN_HEIGHT, SIZE)
		else:
			s.body.pop(0)
			s.body_info.pop(0)

		food.draw(window)
		drawWindow(s, food, window)

	pygame.quit()
