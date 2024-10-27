import json
import os.path

from Cube import *
from Solver import IDA_star, build_heuristic_db

MAX_MOVES = 5
NEW_HEURISTICS = False
HEURISTIC_FILE = 'heuristic.json'

#--------------------------------
cube = RubiksCube(3)
print(f"First cube: {cube}")
print('-----------')
#--------------------------------

if os.path.exists(HEURISTIC_FILE):
    with open(HEURISTIC_FILE) as f:
        h_db = json.load(f)
else:
    h_db = None

if h_db is None or NEW_HEURISTICS is True:
    actions = ['U','D','R','L','F','B','U_prime', 'D_prime', 'R_prime', 'L_prime', 'F_prime', 'B_prime']
    h_db = build_heuristic_db(
        cube.string(),
        actions,
        max_moves = MAX_MOVES,
        heuristic = h_db
    )

    with open(HEURISTIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(
            h_db,
            f,
            ensure_ascii=False,
            indent=4
        )
#--------------------------------
cube = RubiksCube(3)
cube.shuffle(5)
print('----------')
#--------------------------------
solver = IDA_star(h_db)
moves = solver.run(cube.string())
print(moves)
print(cube)
for m in moves:
    print(m)
    action_method = getattr(cube, m)
    action_method()
    print(cube)
    

#print(cube)