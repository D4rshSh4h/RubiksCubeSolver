import numpy as np
import random

class RubiksCube:
    #Cubesize as a param
    #State as a param - takes a string representation of a state and converts it to a 3D numpy array
    def __init__(self, cubesize, state=None):
        self.cubesize = cubesize
        if state is None:
            self.state = np.array([np.full((cubesize, cubesize), i) for i in range(6)])
        else:
            self.state = self.parse_string(state)
        self.color_map = {0: 'W', 1: 'B', 2: 'G', 3: 'R', 4: 'O', 5: 'Y'}
        
        
    def parse_string(self, state):
        value_map = {'W': 0, 'B': 1, 'G': 2, 'R': 3, 'O': 4, 'Y': 5}
        vals = [value_map[i] for i in state]
        num_faces = 6
        
        # Each face is a cubesize x cubesize matrix
        face_size = self.cubesize * self.cubesize
        
        # Initialize a list to hold each face's matrix
        faces = [np.zeros((self.cubesize, self.cubesize), dtype=int) for _ in range(num_faces)]
        
        # Populate each face's matrix
        for i in range(num_faces):
            start_index = i * face_size
            end_index = start_index + face_size
            face_vals = vals[start_index:end_index]
            
            # Reshape face_vals to a 2D matrix and assign it to the appropriate face
            faces[i] = np.array(face_vals).reshape((self.cubesize, self.cubesize))
        
        # Stack the faces into a 3D array
        result = np.stack(faces, axis=0)
        
        return result

    def shuffle(self, moves, display=True):
        actions = ['U','D','R','L','F','B','U_prime', 'D_prime', 'R_prime', 'L_prime', 'F_prime', 'B_prime']
        for i in range(moves):
            a = random.choice(actions)
            if display:
                
                print(a)
            method = getattr(self, a)
            method()


    def __repr__(self):
        repr_str = ""
        for face in self.state:
            for row in face:
                repr_str += " ".join(self.color_map[int(color)] for color in row) + "\n"
            repr_str += "\n"
        return repr_str

    def rotate_face(self):
        #Only front face can turn (index 0)
        
        self.state[0] = np.rot90(self.state[0], 1, axes=(1,0))
        
        #Adjust edges
        top_edge = self.state[3][-1, :].copy()
        self.state[3][-1, :] = self.state[1][:, -1][::-1]
        self.state[1][:, -1] = self.state[4][0, :].copy()
        self.state[4][0, :] = self.state[2][:, 0][::-1]
        self.state[2][:, 0] = top_edge
    
    def rotate_cube_down(self):
        # Rotate around the X-axis (top -> front -> bottom -> back)
        front = self.state[0].copy()
        bottom = self.state[4].copy()
        self.state[0], self.state[3], self.state[4], self.state[5] = (
            self.state[3], 
            np.rot90(self.state[5], 2),
            front, 
            np.rot90(bottom, 2)
        )
        # Swap top and bottom rows of left and right faces
        self.state[1] = np.rot90(self.state[1], 1, axes=(1,0))
        self.state[2] = np.rot90(self.state[2], 1,)

    def rotate_cube_up(self):
        # Rotate around the X-axis (bottom -> front -> top -> back)
        bottom = self.state[5].copy()
        front = self.state[0].copy()
        self.state[0], self.state[5], self.state[4], self.state[3] = (
            self.state[4], 
            np.rot90(self.state[3],2), 
            np.rot90(bottom, 2), 
            front
        )
        # Swap top and bottom rows of left and right faces
        self.state[1] = np.rot90(self.state[1], 1 )
        self.state[2] = np.rot90(self.state[2], 1, axes=(1,0))

    def rotate_cube_counterclockwise(self):
        # Rotate around the Y-axis (left -> front -> right -> back)
        back = self.state[5].copy()
        front = self.state[0].copy()
        self.state[0], self.state[5], self.state[2], self.state[1] = (
            self.state[1], 
            self.state[2], 
            front,
            back
        )
        # Rotate left and right columns of top and bottom faces
        self.state[3] = np.rot90(self.state[3], 1)
        self.state[4] = np.rot90(self.state[4], -1)

    def rotate_cube_clockwise(self):
        # Rotate around the Y-axis (right -> front -> left -> back)
        front = self.state[0].copy()
        left = self.state[1].copy()
        self.state[0], self.state[1], self.state[2], self.state[5] = (
            self.state[2], 
            front, 
            self.state[5], 
            left
        )
        # Rotate left and right columns of top and bottom faces
        self.state[3] = np.rot90(self.state[3], -1)
        self.state[4] = np.rot90(self.state[4], 1)
    
    def rotate_face_counterclockwise(self):
        self.rotate_face()
        self.rotate_face()
        self.rotate_face()

    #Common moves
    #Return cube to original orientation
    def U(self): self.rotate_cube_down(), self.rotate_face(), self.rotate_cube_up()
    def U_prime(self): self.rotate_cube_down(), self.rotate_face_counterclockwise(), self.rotate_cube_up()
    
    def D(self): self.rotate_cube_up(), self.rotate_face(), self.rotate_cube_down()
    def D_prime(self): self.rotate_cube_up(), self.rotate_face_counterclockwise(), self.rotate_cube_down()
    
    def R(self): self.rotate_cube_clockwise(), self.rotate_face(), self.rotate_cube_counterclockwise()
    def R_prime(self): self.rotate_cube_clockwise(), self.rotate_face_counterclockwise(), self.rotate_cube_counterclockwise()
    
    def L(self): self.rotate_cube_counterclockwise(), self.rotate_face(), self.rotate_cube_clockwise()
    def L_prime(self): self.rotate_cube_counterclockwise(), self.rotate_face_counterclockwise(), self.rotate_cube_clockwise()
    
    def F(self): self.rotate_face()
    def F_prime(self): self.rotate_face_counterclockwise()
    
    def B(self): self.rotate_cube_clockwise(), self.rotate_cube_clockwise(), self.rotate_face(), self.rotate_cube_counterclockwise(), self.rotate_cube_counterclockwise()
    def B_prime(self): self.rotate_cube_clockwise(), self.rotate_cube_clockwise(), self.rotate_face_counterclockwise(), self.rotate_cube_counterclockwise(), self.rotate_cube_counterclockwise()
    
    def string(self):
        return "".join(
            "".join(self.color_map[int(color)] for color in row)
            for face in self.state
            for row in face
        )
    
    def solved(self):
        for i in self.state:
            i = i.flatten()
            
            set_check = set(i)
            if len(set_check) > 1:
                return False
        return True


