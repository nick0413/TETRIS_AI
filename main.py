import pyglet
from pyglet.window import key
import tetris_engine as tr
window_size = (700, 1200)
window = pyglet.window.Window(window_size[0], window_size[1], "Grid")

grid_x = 10
grid_y = 20
square_size = 50

grid_with=grid_x*square_size
grid_height=grid_y*square_size
grid_position = (window_size[0]/2-grid_with/2,window_size[1]/2-grid_height/2)

board=tr.Tetris_board(grid_x,grid_y,square_size,grid_position[0],grid_position[1])

@window.event
def on_draw():
    window.clear()
    board.draw()

starting_height = 22
pieces=False
def on_key_press(symbol, modifiers):
	global pieces
	if symbol == key.RETURN:
		board.start_game(starting_height)
		pieces=True
	if symbol == key.R or symbol == key.SPACE:
		board.rotate_piece()



dropping_piece=False

def update(dt):
	
	global dropping_piece
	dropping_piece=False

	if pieces:
		board.check_piece_grounded(starting_height)


	if keys[key.LEFT]:
		board.update_piece_position("x",-1)
	if keys[key.RIGHT]:
		board.update_piece_position("x",1)

	if keys[key.DOWN]:
		dropping_piece=True
		board.update_piece_position("y",-1)

	


	
def drop_piece(dt):
	if pieces and not dropping_piece:
		board.update_piece_position("y",-1)


pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.clock.schedule_interval(drop_piece, 1/2.0)

keys = key.KeyStateHandler()
window.push_handlers(keys)
window.push_handlers(on_key_press)
pyglet.app.run()
