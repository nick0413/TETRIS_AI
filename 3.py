import os
import time
import numpy as np

z=np.ones((10,10))
def clear_terminal():
    os.system('cls')

while True:
	print(np.flipud((z).T))
	print("-------------------\n")

	# Wait for 2 seconds
	time.sleep(0.1)

	# Clear the terminal
	clear_terminal()