import pyglet
import numpy as np
import os
import time
from lists import *
import random
import sys
from typing import List
random.seed(0)
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# In pyglet, coordinates are defined as the caritisan coordinate system, with the origin in the bottom left corner. 
# The y-axis points up, the x-axis points right.


def define_grid(n,m, size=100,x_offset=0,y_offset=0):
	
	grid = []
	for i in range(n):
		for j in range(m):
			line1 = pyglet.shapes.Line(i*size+x_offset, j*size+y_offset, (i+1)*size+x_offset, j*size+y_offset, width=1)
			line2 = pyglet.shapes.Line((i+1)*size+x_offset, j*size+y_offset, (i+1)*size+x_offset, (j+1)*size+y_offset, width=1)
			line3 = pyglet.shapes.Line((i+1)*size+x_offset, (j+1)*size+y_offset, i*size+x_offset, (j+1)*size+y_offset, width=1)
			line4 = pyglet.shapes.Line(i*size+x_offset, (j+1)*size+y_offset, i*size+x_offset, j*size+y_offset, width=1)
			grid.append((line1, line2, line3, line4))
	return grid

	# line 1 up-horizontal
	# line 2 right-vertical
	# line 3 down-horizontal
	# line 4 left-vertical
	# definded in clockwise order

def draw_grid(grid):
	for lines in grid:
		for line in lines:
			line.draw()

class Piece:


	def __init__(self,type, starting_position, board_size) -> None:
		self.x = starting_position[0]
		self.y = starting_position[1]
		self.type = type
		self.color = color_pieces[type]
		self.rotation = 90
		self.shape = codes_pieces[type][self.rotation]
		self.board_size = board_size

		self.empty: bool = False

		self.max_x=max(self.shape[:,0])
		self.min_x=min(self.shape[:,0])
		self.max_y=max(self.shape[:,1])
		self.min_y=min(self.shape[:,1])

		self.grounded = False


		# print(f"{types_pieces[self.type]} created at {self.x},{self.y}")

	def x_up_bound(self):
		return max(self.shape[:,0])+self.x
	def x_down_bound(self):
		return min(self.shape[:,0])+self.x
	def y_up_bound(self):
		return max(self.shape[:,1])+self.y
	def y_down_bound(self):
		return min(self.shape[:,1])+self.y

	def __str__(self) -> str:
		return str(types_pieces[self.type])
	
	def board_position(self, original_shape=False):
		squares=np.copy(self.shape)
		squares[:,0]+=self.x
		squares[:,1]+=self.y

		indices=tuple(squares.T)
		if original_shape:
			return squares
		
		return indices
	
	def assing_shape(self, shape):
		shape[:,0] -= self.x
		shape[:,1] -= self.y
		  

	
	def rotate(self):
		self.rotation = (self.rotation+ 90) % 360
		self.shape = codes_pieces[self.type][self.rotation]
		self.max_x=max(self.shape[:,0])
		self.min_x=min(self.shape[:,0])
		self.max_y=max(self.shape[:,1])
		self.min_y=min(self.shape[:,1])

		if (self.y_down_bound()<0 ):
			self.y = -self.min_y

		if (self.y_up_bound()>self.board_size[1]-1):
			self.y = self.board_size[1]-1-self.max_y

		if (self.x_down_bound()<0 ):
			self.x = -self.min_x

		if (self.x_up_bound()>self.board_size[0]-1):
			self.x = self.board_size[0]-1-self.max_x




class Tetris_board:
	def __init__(self,n,m, size=100,x_offset=0,y_offset=0) -> None:
		self.grid_dimensions = (10,25)
		self.base_grid = np.zeros(self.grid_dimensions,dtype=int)
		self.grounded_grid = np.copy(self.base_grid)
		self.future_grid = np.copy(self.base_grid)
		self.grid_drawing = define_grid(n,m, size,x_offset,y_offset)
		self.pieces: List[Piece] = []
		self.square_size = size
		self.selected_piece = None

		self.x_offset = x_offset
		self.y_offset = y_offset

		

		self.remaining_pieces = [1,2,3,4,5,6,7]

	def start_game(self,starting_height: int = 22):
		self.add_piece(
			Piece(self.Generate_next_piece(),(5,starting_height),self.base_grid.shape)
			)

	def draw(self)->None:
		draw_grid(self.grid_drawing)
		self.draw_pieces()

	def add_piece(self, piece: Piece):
		self.pieces.append(piece)
		self.selected_piece = len(self.pieces)-1

		self.base_grid[piece.board_position()] = piece.type

	def draw_pieces(self):
		for piece in self.pieces:
			for coord in piece.shape:
				x,y=self.grid_position_to_pixels(piece.x,piece.y)
				square = pyglet.shapes.Rectangle(x+coord[0]*self.square_size, y+coord[1]*self.square_size, self.square_size, self.square_size, color=piece.color)
				square.draw()

		# clear_terminal()
		# print(np.flipud((self.base_grid+self.grounded_grid).T))
		# time.sleep(0.05)
		# print("-------------------\n")

	def grid_position_to_pixels(self,x,y):
		x_px = x*self.square_size+self.x_offset
		y_px = y*self.square_size+self.y_offset


		return (x_px,y_px)
	
	def check_within_bounds(self, piece, axis, direction):
		if axis == "x":
			if piece.x + direction + piece.min_x < 0:
				return False
			if piece.x + direction + piece.max_x > 9:
				return False
			
			piece.x+=direction
			self.future_grid=self.base_grid*0
			self.future_grid[piece.board_position()] = piece.type
			result, flag = add_arrays_no_intersection(self.future_grid, self.grounded_grid)
			if flag:
				self.intersection = True
				piece.x-=direction
				return False
			piece.x-=direction
			

		if axis == "y":
			if piece.y + direction + piece.min_y < 0:
				piece.grounded = True
				return False
			
			piece.y+=direction
			self.future_grid=self.base_grid*0
			self.future_grid[piece.board_position()] = piece.type
			result, flag = add_arrays_no_intersection(self.future_grid, self.grounded_grid)
			if flag:
				piece.grounded = True
				self.intersection = True
				piece.y-=direction
				return False
			piece.y-=direction
			

		
		return True
	
	def update_piece_position(self, axis, direction):
		self.intersection = False
		try:
			self.pieces[self.selected_piece]
		except TypeError:
			if self.selected_piece == None:
				print("There are no pieces on the board.")
			else:
				raise
			return 
		except IndexError:
			if self.selected_piece < 0 or self.selected_piece > len(self.pieces):
				print("Invalid piece index.-----------")
				print("Selected piece:", self.selected_piece)
				print("Pieces on the board:", len(self.pieces))
				raise

		if axis == "x" and self.check_within_bounds(self.pieces[self.selected_piece], axis, direction):
			self.pieces[self.selected_piece].x += direction
			self.base_grid=self.base_grid*0
			self.base_grid[self.pieces[self.selected_piece].board_position()] = self.pieces[self.selected_piece].type
		try:
			if axis == "y" and self.check_within_bounds(self.pieces[self.selected_piece], axis, direction):
				self.pieces[self.selected_piece].y += direction
				self.base_grid=self.base_grid*0
				self.base_grid[self.pieces[self.selected_piece].board_position()] = self.pieces[self.selected_piece].type
		except IndexError:
			print(len(self.pieces),self.selected_piece)
			print("Error-line229")


	def check_piece_grounded(self, starting_height: int ):

		if self.pieces[self.selected_piece].grounded:
			self.grounded_grid[self.pieces[self.selected_piece].board_position()]=self.pieces[self.selected_piece].type
			r_int=self.Generate_next_piece()
			self.add_piece(Piece(r_int,(5,starting_height),self.base_grid.shape))
			return True
		self.check_lost()
		self.check_line_cleared()
		
	def check_lost(self):
		if np.any(self.grounded_grid[:,20:]!=0):
			self.pieces=[]
			self.base_grid = np.zeros(self.grid_dimensions,dtype=int)
			self.grounded_grid = np.copy(self.base_grid)
			self.future_grid = np.copy(self.base_grid)
			self.start_game()

	def check_line_cleared(self):
		# for piece in self.pieces:
		# 	print(piece)
		# time.sleep(0.1)
		lines_with_no_zeros = np.where(np.all(self.grounded_grid[:,:20] != 0, axis=0))[0]
		line_cleared = False
		
		if lines_with_no_zeros.size != 0:
			print("lines cleared",lines_with_no_zeros)
			pieces_removed=0
			line_cleared = True
			for piece in self.pieces:

				indices = piece.board_position(True)
				piece_y = indices[:,1]

				remaining_blocks=np.empty(0,dtype=int)
				print(piece.type,'-----------------------------------')
				print(piece_y)
				if np.any(np.isin(piece_y, lines_with_no_zeros)):
					remaining_blocks = np.where(~np.isin(piece_y, lines_with_no_zeros))

					piece.shape = piece.shape[remaining_blocks]
					line_cleared = True

					if piece.shape.size == 0:
						piece.empty = True
						print('piece removed', piece.type)

				indices = piece.board_position(True)
				piece_y = indices[:,1]
				if np.any(piece_y > np.max(lines_with_no_zeros)):
					print(piece.shape)
					print('piece moved down')
					print(piece_y)
					drop_blocks=np.where(piece_y > np.max(lines_with_no_zeros))
					piece.shape[:,1][drop_blocks] -= len(lines_with_no_zeros)
					print(piece.board_position(True))

			for piece in self.pieces:
				if piece.empty:
					self.pieces.remove(piece)
					pieces_removed+=1
			self.selected_piece=len(self.pieces)-1

			self.recalculate_ground()

		# if line_cleared:
		# 	print(np.flipud((self.grounded_grid[:,:6]).T))
			
		# 	sys.exit()
		clear_terminal()
		print(np.flipud((self.grounded_grid+self.base_grid).T))







	
	def Generate_next_piece(self)-> int:
		piece = random.choice(self.remaining_pieces)
		self.remaining_pieces.remove(piece)
		if len(self.remaining_pieces) == 0:
			self.remaining_pieces = [1,2,3,4,5,6,7]


		return piece
	
	def rotate_piece(self):
		self.pieces[self.selected_piece].rotate()

	def recalculate_ground(self):
		self.grounded_grid=self.base_grid*0
		for piece in self.pieces:
			if piece.grounded:
				print(piece.board_position(True),piece.type)
				self.grounded_grid[piece.board_position()]=piece.type

		np.savetxt("last_ground.csv", np.flipud(self.grounded_grid).T, fmt='%d', delimiter=",")







def pieces_to_string(pieces):
	return '[' + ', '.join(str(piece) for piece in pieces) + ']'	
		
def add_arrays_no_intersection(z, q):
    if z.shape != q.shape:
        raise ValueError("Arrays must have the same shape")

    mask = np.logical_and(z != 0, q != 0)
    flag = np.any(mask)
    q_masked = np.where(mask, 0, q)
    result = z + q_masked

    return result, flag	
