import pyglet
import numpy as np
import os
import time
import sys

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# In pyglet, coordinates are defined as the caritisan coordinate system, with the origin in the bottom left corner. 
# The y-axis points up, the x-axis points right.
I_piece = np.array([[0,0],[1,0],[2,0],[3,0]])
O_piece = np.array([[0,0],[1,0],[0,1],[1,1]])
L_piece = np.array([[0,0],[0,1],[1,1],[2,1]])
P_piece = np.array([[0,0],[1,0],[2,0],[2,1]])
q_piece = np.array([[0,0]])

codes_pieces = {
	1:I_piece,
	2:O_piece,
	3:L_piece,
	4:q_piece,
}

salmon = (253, 63, 89)
orange = (255, 200, 46)
yellow = (254, 251, 52)
green_ = (83, 218, 63)
cyan   = (1, 237, 250)

color_pieces = {
	1:cyan,
	2:yellow,
	3:green_,
	4:salmon,
}
types_pieces = {
	1:"I_piece",
	2:"O_piece",
	3:"L_piece",
	4:"q_piece",
}
 



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


class piece:
	def __init__(self,type, starting_position) -> None:
		self.x = starting_position[0]
		self.y = starting_position[1]
		self.type = type
		self.color = color_pieces[type]
		self.shape = codes_pieces[type]


		self.max_x=max(self.shape[:,0])
		self.min_x=min(self.shape[:,0])
		self.max_y=max(self.shape[:,1])
		self.min_y=min(self.shape[:,1])

		self.grounded = False

		# print(f"{types_pieces[self.type]} created at {self.x},{self.y}")

	def __str__(self) -> str:
		return str(types_pieces[self.type])
	
	def board_position(self):
		squares=np.copy(self.shape)
		squares[:,0]+=self.x
		squares[:,1]+=self.y

		indices=tuple(squares.T)

		return indices


class Tetris_board:
	def __init__(self,n,m, size=100,x_offset=0,y_offset=0) -> None:
		self.base_grid = np.zeros((10,30),dtype=int)
		self.grounded_grid = np.zeros((10,30),dtype=int)
		self.future_grid = np.zeros((10,30),dtype=int)
		self.grid_drawing = define_grid(n,m, size,x_offset,y_offset)
		self.pieces =[]
		self.square_size = size
		self.selected_piece = None

		self.x_offset = x_offset
		self.y_offset = y_offset

		self.intersection = False



	def draw(self)->None:
		draw_grid(self.grid_drawing)
		self.draw_pieces()

	def add_piece(self, piece: piece):
		self.pieces.append(piece)
		self.selected_piece = len(self.pieces)-1

		self.base_grid[piece.board_position()] = piece.type

	def draw_pieces(self):
		# clear_terminal()
		for piece in self.pieces:
			for coord in piece.shape:
				x,y=self.grid_position_to_pixels(piece.x,piece.y)
				square = pyglet.shapes.Rectangle(x+coord[0]*self.square_size, y+coord[1]*self.square_size, self.square_size, self.square_size, color=piece.color)
				square.draw()

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
				# print('intersection')
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
				# print('intersection')
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
				print("Invalid piece index.")
				raise
		# print("=====================================")
		# print(self.pieces[self.selected_piece].y)
		if axis == "x" and self.check_within_bounds(self.pieces[self.selected_piece], axis, direction):
			self.pieces[self.selected_piece].x += direction
			self.base_grid=self.base_grid*0
			self.base_grid[self.pieces[self.selected_piece].board_position()] = self.pieces[self.selected_piece].type

		if axis == "y" and self.check_within_bounds(self.pieces[self.selected_piece], axis, direction):
			self.pieces[self.selected_piece].y += direction
			self.base_grid=self.base_grid*0
			self.base_grid[self.pieces[self.selected_piece].board_position()] = self.pieces[self.selected_piece].type
		# print(self.pieces[self.selected_piece].y)
	


	def check_piece_grounded(self, starting_height: int ):
		# generate random int
		r_int=np.random.randint(1,len(codes_pieces)+1)
		if self.pieces[self.selected_piece].grounded:
			self.grounded_grid[self.pieces[self.selected_piece].board_position()]=self.pieces[self.selected_piece].type
			# clear_terminal()
			# print(np.flipud((self.grounded_grid).T))
			self.add_piece(piece(r_int,(5,starting_height)))
			return True






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
