from z3 import Array, IntSort, Int, Select, Implies, And, Solver, sat, ArrayRef, IntNumRef

### env encoding
# 0: empty
# 1: goal
# 2: obstacle
def reachable(n: IntNumRef, env: ArrayRef, start_pos: IntNumRef | int, goal_pos: IntNumRef, max_steps : int = 20, meta_index: int = 0):
    constraints = []
    
    step_count = Int(f'step_count_{meta_index}')
    constraints.append(step_count >= 0)
    constraints.append(step_count <= max_steps)
    
    ### positions
    #player_positions = [Int(f'pos_{meta_index}_{i}') for i in range(num_steps + 1)]
    x_positions = [Int(f'x_{meta_index}_{i}') for i in range(max_steps + 1)]
    y_positions = [Int(f'y_{meta_index}_{i}') for i in range(max_steps + 1)]
    
    constraints.append(x_positions[0] == start_pos % n)
    constraints.append(y_positions[0] == start_pos / n)
    
    for i in range(max_steps + 1):
        constraints.append(x_positions[i] >= 0)
        constraints.append(x_positions[i] < n)
        constraints.append(y_positions[i] >= 0)
        constraints.append(y_positions[i] < n)
        
        # player must be able to reach the goal position in at most max_steps steps
        # solver will find step_count for us
        constraints.append(Implies(i == step_count, x_positions[i] + n*y_positions[i] == goal_pos))
    
    ### movement
    # 0: stay
    # 1: left
    # 2: right
    # 3: up
    # 4: down
    moves = [Int(f'move_{meta_index}_{i}') for i in range(max_steps)]
    
    for i,move in enumerate(moves):
        constraints.append(move >= 0)
        constraints.append(move < 5)
        
        prev_x = x_positions[i]
        prev_y = y_positions[i]
        
        # if the player is at the goal position, don't bother moving
        constraints.append(Implies(prev_x + n*prev_y == goal_pos, move == 0))
        
        # movement conditions
        constraints.append(Implies(move == 0, And(
            x_positions[i+1] == prev_x, y_positions[i+1] == prev_y
        )))
        
        constraints.append(Implies(move == 1, And(
            x_positions[i+1] == prev_x - 1, y_positions[i+1] == prev_y, prev_x >= 1
        )))
        
        constraints.append(Implies(move == 2, And(
            x_positions[i+1] == prev_x + 1, y_positions[i+1] == prev_y, prev_x < n - 1
        )))
        
        constraints.append(Implies(move == 3, And(
            y_positions[i+1] == prev_y + 1, x_positions[i+1] == prev_x, prev_y < n - 1
        )))
        
        constraints.append(Implies(move == 4, And(
            y_positions[i+1] == prev_y - 1, x_positions[i+1] == prev_x, prev_y >= 1
        )))
        
        # player cannot move through walls
        constraints.append(Select(env, x_positions[i+1] + n*y_positions[i+1]) < 2)
    
    return And(constraints), (x_positions, y_positions), step_count

### start_pos: index of the player's starting position 0 <= start_pos < n_sq
def findPath(environment: list[list[int]], start_pos: int, max_steps: int):
    n = len(environment)
    n_sq = n**2
    
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
    s.add(Select(env, goal) == 1)
    s.add(goal >= 0)
    s.add(goal < n_sq)
    
    is_reachable, (x_positions, y_positions), step_count = reachable(n_z3, env, start_pos, goal, max_steps)
    s.add(is_reachable)
    
    ### check satisfiability and return appropriate data
    result = s.check()
    
    if result == sat:
        m = s.model()
        
        n_steps = m[step_count].as_long()
        return [(m[x_positions[i]].as_long(), m[y_positions[i]].as_long()) for i in range(n_steps + 1)]
    else:
        return None
        
