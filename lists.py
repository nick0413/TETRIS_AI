import numpy as np

# https://www.researchgate.net/figure/Different-rotations-1-2-3-and-4-denote-0-90-180-and-270-degree-respectively-in_fig3_282476297
	


I_piece_0 = np.array([[-2,0],[-1,0],[0,0],[1,0]])
I_piece_90 = np.array([[0,-2],[0,-1],[0,0],[0,1]])
I_piece_180 = np.array([[-2,-1],[-1,-1],[0,-1],[1,-1]])
I_piece_270 = np.array([[-1,-2],[-1,-1],[-1,0],[-1,1]])

L_piece_0 = np.array([[-1,0],[-1,1],[0,1],[1,1]])
L_piece_90 = np.array([[-1,2],[0,2],[0,1],[0,0]])
L_piece_180 = np.array([[-1,1],[0,1],[1,1],[1,2]])
L_piece_270 = np.array([[0,2],[0,1],[0,0],[1,0]])

S_piece_0 = np.array([[-1,0],[0,0],[0,1],[1,1]])
S_piece_90 = np.array([[0,1],[0,0],[1,0],[1,-1]])
S_piece_180 = np.array([[-1,-1],[0,-1],[0,0],[1,0]])
S_piece_270 = np.array([[-1,1],[-1,0],[0,0],[0,-1]])


Z_piece = np.array([[-1,1],[0,1],[0,0],[1,0]])
Z_piece_90 = np.array([[0,-1],[0,0],[1,0],[1,1]])
Z_piece_180 = np.array([[-1,0],[0,0],[0,-1],[1,-1]])
Z_piece_270 = np.array([[-1,-1],[-1,0],[0,0],[0,1]])



J_piece = np.array([[-1,1],[-1,0],[0,0],[1,0]])
J_piece_90 = np.array([[0,1],[0,0],[0,-1],[1,1]])
J_piece_180 = np.array([[-1,0],[0,0],[1,0],[1,-1]])
J_piece_270 = np.array([[-1,-1],[0,-1],[0,0],[0,1]])

O_piece = np.array([[0,0],[1,0],[0,1],[1,1]])

T_piece_0 = np.array([[-1,0],[0,0],[0,1],[1,0]])
T_piece_90 = np.array([[0,1],[0,0],[0,-1],[1,0]])
T_piece_180 = np.array([[-1,0],[0,0],[0,-1],[1,0]])
T_piece_270 = np.array([[-1,0],[0,0],[0,1],[0,-1]])





I_piece_rotations = {
	0:I_piece_0,
	90:I_piece_90,
	180:I_piece_180,
	270:I_piece_270,
}
L_piece_rotations = {
	0:L_piece_0,
	90:L_piece_90,
	180:L_piece_180,
	270:L_piece_270,
}
S_piece_rotations = {
	0:S_piece_0,
	90:S_piece_90,
	180:S_piece_180,
	270:S_piece_270,
}
Z_piece_rotations = {
	0:Z_piece,
	90:Z_piece_90,
	180:Z_piece_180,
	270:Z_piece_270,

}
J_piece_rotations = {
	0:J_piece,
	90:J_piece_90,
	180:J_piece_180,
	270:J_piece_270,

}
O_piece_rotations = {
	0:O_piece,
	90:O_piece,
	180:O_piece,
	270:O_piece,
}
T_piece_rotations = {
	0:T_piece_0,
	90:T_piece_90,
	180:T_piece_180,
	270:T_piece_270,
}


codes_pieces = {
	1:I_piece_rotations,
	2:L_piece_rotations,
	3:S_piece_rotations,
	4:Z_piece_rotations,
	5:J_piece_rotations,
	6:O_piece_rotations,
	7:T_piece_rotations,
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
 