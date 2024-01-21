import numpy as np

# https://www.researchgate.net/figure/Different-rotations-1-2-3-and-4-denote-0-90-180-and-270-degree-respectively-in_fig3_282476297
	


I_piece = np.array([[-2,0],[-1,0],[0,0],[1,0]])
I_piece_90 = np.array([[0,-2],[0,-1],[0,0],[0,1]])

L_piece = np.array([[0,0],[0,1],[1,1],[2,1]])
S_piece = np.array([[0,0],[1,0],[1,1],[2,1]])
Z_piece = np.array([[0,1],[1,1],[1,0],[2,0]])
J_piece = np.array([[0,1],[1,1],[2,1],[2,0]])
O_piece = np.array([[0,0],[1,0],[0,1],[1,1]])
T_piece = np.array([[0,1],[1,1],[1,0],[2,1]])

codes_pieces = {
	1:I_piece,
	2:L_piece,
	3:S_piece,
	4:Z_piece,
	5:J_piece,
	6:O_piece,
	7:T_piece,

}
cyan   = (1, 237, 250)
orange = (246, 153, 4)
green = (83, 218, 63)
salmon = (253, 63, 89)
blue= (0, 119, 211)
yellow = (254, 251, 52)
purple = (120, 37, 111)


color_pieces = {
	1:cyan,
	2:orange,
	3:green,
	4:salmon,
	5:blue,
	6:yellow,
	7:purple,
}
types_pieces = {
	1:"I_piece",
	2:"L_piece",
	3:"S_piece",
	4:"Z_piece",
	5:"J_piece",
	6:"O_piece",
	7:"T_piece",
}
 