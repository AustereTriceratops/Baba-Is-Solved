from z3 import Array, IntSort, Int, Select, ForAll, And, Implies, If, Solver, sat, ArrayRef, IntNumRef, BoolRef

from constants import *

### env encoding
# 0: empty
# 1: goal
# 2: wall
# >= 3: pushable/obstacle
def reachable(
    n: IntNumRef,
    env: ArrayRef,
    x_pos: IntNumRef | int,
    y_pos: IntNumRef | int,
    goal_pos: IntNumRef,
    wall_is_stop: BoolRef | bool,
    max_steps : int = 20,
    meta_index: int = 0
):
    constraints = []
    
    step_count = Int(f'step_count_{meta_index}')
    constraints.append(step_count >= 0)
    constraints.append(step_count <= max_steps)
    
    ### positions
    x_positions = [Int(f'x_{meta_index}_{i}') for i in range(max_steps + 1)]
    y_positions = [Int(f'y_{meta_index}_{i}') for i in range(max_steps + 1)]
    
    constraints.append(x_positions[0] == x_pos)
    constraints.append(y_positions[0] == y_pos)
    
    for i in range(max_steps + 1):
        constraints.append(x_positions[i] >= 0)
        constraints.append(x_positions[i] < n)
        constraints.append(y_positions[i] >= 0)
        constraints.append(y_positions[i] < n)
        
        # player must be able to reach the goal position in at most max_steps steps
        # solver will find step_count for us
        constraints.append(If(i == step_count, x_positions[i] + n*y_positions[i] == goal_pos, True))
    
    ### movement
    # 0: left
    # 1: right
    # 2: up
    # 3: down
    moves = [Int(f'move_{meta_index}_{i}') for i in range(max_steps)]
    
    for i, move in enumerate(moves):
        constraints.append(move >= 0)
        constraints.append(move < 4)
        
        prev_x = x_positions[i]
        prev_y = y_positions[i]
        
        move_len = Int(f'move_len_{meta_index}_{i}')
        constraints.append(And(move_len >= 0, move_len < n))
        mv = Int(f'move_intermediate_{meta_index}_{i}')
        
        # if the player is at the goal position, don't bother moving
        constraints.append(If(
            prev_x + n*prev_y == goal_pos, move_len == 0, move_len != 0
        ))
        
        # movement conditions
        # constraints.append(If(move == 0, And(
        #     x_positions[i+1] == prev_x, y_positions[i+1] == prev_y, 
        # ), True))
        
        constraints.append(If(move == 0, And(
            x_positions[i+1] == prev_x - move_len,
            y_positions[i+1] == prev_y,
            prev_x >= move_len,
            ForAll([mv],
                Implies(
                    And(mv >= x_positions[i+1], mv < prev_x),
                    If(wall_is_stop,
                        Select(env, mv + n*y_positions[i+1]) < WALL,
                        Select(env, mv + n*y_positions[i+1]) < BOX
                    )
                )
            )
        ), True))
        
        constraints.append(If(move == 1, And(
            x_positions[i+1] == prev_x + move_len,
            y_positions[i+1] == prev_y,
            prev_x + move_len < n,
            ForAll([mv],
                Implies(
                    And(mv <= x_positions[i+1], mv > prev_x),
                    If(wall_is_stop,
                        Select(env, mv + n*y_positions[i+1]) < WALL,
                        Select(env, mv + n*y_positions[i+1]) < BOX
                    )
                )
            )
        ), True))
        
        constraints.append(If(move == 2, And(
            y_positions[i+1] == prev_y + move_len,
            x_positions[i+1] == prev_x,
            prev_y + move_len < n,
            ForAll([mv],
                Implies(
                    And(mv <= y_positions[i+1], mv > prev_y),
                    If(wall_is_stop,
                        Select(env, x_positions[i+1] + n*mv) < WALL,
                        Select(env, x_positions[i+1] + n*mv) < BOX
                    )
                )
            )
        ), True))
        
        constraints.append(If(move == 3, And(
            y_positions[i+1] == prev_y - move_len,
            x_positions[i+1] == prev_x,
            prev_y >= move_len,
            ForAll([mv],
                Implies(
                    And(mv >= y_positions[i+1], mv < prev_y), 
                    If(wall_is_stop,
                        Select(env, x_positions[i+1] + n*mv) < WALL,
                        Select(env, x_positions[i+1] + n*mv) < BOX
                    )
                )
            )
        ), True))
    
    return And(constraints), (x_positions, y_positions), step_count

### start_pos: index of the player's starting position 0 <= start_pos < n_sq
def findPath(environment: list[list[int]], start_pos: int, max_steps: int, wall_is_stop=True):
    n = len(environment)
    n_sq = n**2
    start_x = start_pos % n
    start_y = start_pos // n
    
    s = Solver()
    
    n_z3 = Int('n')
    s.add(n_z3 == n)
    
    ### environment states
    env = Array(f'env', IntSort(), IntSort())
    
    # initialize the environment
    for i in range(n):
        for j in range(n):
            s.add(Select(env, n*i + j) == environment[i][j])
    
    # initialize goal tile
    goal = Int(f'goal_pos_{0}')
    s.add(Select(env, goal) == GOAL)
    s.add(goal >= 0)
    s.add(goal < n_sq)
    
    is_reachable, (x_positions, y_positions), step_count = reachable(n_z3, env, start_x, start_y, goal, wall_is_stop, max_steps)
    s.add(is_reachable)
    
    ### check satisfiability and return appropriate data
    result = s.check()
    
    if result == sat:
        m = s.model()
        
        n_steps = m[step_count].as_long()
        return [(m[x_positions[i]].as_long(), m[y_positions[i]].as_long()) for i in range(n_steps + 1)]
    else:
        return None
