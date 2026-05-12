from z3 import Array, IntSort, Int, Select, Implies, And, Solver, sat, ArrayRef, IntNumRef

### env encoding
# 0: empty
# 1: obstacle
# 2: goal
def reachable(n: int, env: ArrayRef, start_pos: IntNumRef | int, goal_pos: IntNumRef, num_steps : int = 20, meta_index: int = 0):
    constraints = []
    n_sq = n**2
    
    ### positions
    player_positions = [Int(f'pos_{meta_index}_{i}') for i in range(num_steps + 1)]
    
    constraints.append(player_positions[0] == start_pos)
    
    for i in range(num_steps + 1):
        constraints.append(player_positions[i] >= 0)
        constraints.append(player_positions[i] < n_sq)
    
    # player must be able to reach the goal position after num_steps steps
    constraints.append(player_positions[num_steps] == goal_pos)
    
    ### movement
    # 0: stay
    # 1: left
    # 2: right
    # 3: up
    # 4: down
    moves = [Int(f'move_{meta_index}_{i}') for i in range(num_steps)]
    
    for i,move in enumerate(moves):
        constraints.append(move >= 0)
        constraints.append(move < 5)
        
        prev_pos = player_positions[i]
        
        # if the player is at the goal position, don't bother moving
        constraints.append(Implies(prev_pos == goal_pos, move == 0))
        
        # movement conditions
        constraints.append(Implies(move == 0, player_positions[i+1] == prev_pos))
        
        constraints.append(Implies(move == 1, player_positions[i+1] == prev_pos - 1))
        constraints.append(Implies(move == 1, Select(env, prev_pos - 1) != 1))
        constraints.append(Implies(move == 1, prev_pos % n >= 1))
        
        constraints.append(Implies(move == 2, player_positions[i+1] == prev_pos + 1))
        constraints.append(Implies(move == 2, Select(env, prev_pos + 1) != 1))
        constraints.append(Implies(move == 2, prev_pos % n < n - 1))
        
        constraints.append(Implies(move == 3, player_positions[i+1] == prev_pos + n))
        constraints.append(Implies(move == 3, Select(env, prev_pos + n) != 1))
        constraints.append(Implies(move == 3, prev_pos < n_sq - n))
        
        constraints.append(Implies(move == 4, player_positions[i+1] == prev_pos - n))
        constraints.append(Implies(move == 4, Select(env, prev_pos - n) != 1))
        constraints.append(Implies(move == 4, prev_pos >= n))
    
    return And(constraints), player_positions

### start_pos: index of the player's starting position 0 <= start_pos < n_sq
def findPath(environment: list[list[int]], start_pos: int, num_steps: int):
    n = len(environment)
    n_sq = n**2
    
    s = Solver()
    
    ### environment states
    env = Array(f'env', IntSort(), IntSort())
    
    # initialize the environment
    for i in range(n):
        for j in range(n):
            s.add(Select(env, n*i + j) == environment[i][j])
    
    # initialize goal tile
    goal = Int(f'goal_pos_{0}')
    s.add(Select(env, goal) == 2)
    s.add(goal >= 0)
    s.add(goal < n_sq)
    
    is_reachable, player_positions = reachable(n, env, start_pos, goal, num_steps)
    s.add(is_reachable)
    
    ### check satisfiability and return appropriate data
    result = s.check()
    
    if result == sat:
        m = s.model()
        
        return [m[player_positions[i]].as_long() for i in range(num_steps + 1)]
    else:
        return None
        
