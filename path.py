from z3 import Array, IntSort, Int, Select, Implies, Solver, sat

### env encoding
# 0: empty
# 1: obstacle
# 2: goal

### start_pos: index of the player's starting position 0 <= start_pos < n_sq
def findPath(environment: list[list[int]], start_pos: int, num_steps: int):
    n = len(environment)
    n_sq = n*n
    
    s = Solver()
    
    ### environment states
    env = Array(f'env', IntSort(), IntSort())
    
    # initialize the environment
    for i in range(n):
        for j in range(n):
            s.add(Select(env, n*i + j) == environment[i][j])

    ### positions
    player_positions = [Int(f'pos_{i}') for i in range(num_steps + 1)]
    goal_pos = Int('goal_pos')
    
    s.add(player_positions[0] == start_pos)
    s.add(Select(env, goal_pos) == 2)
    
    for i in range(num_steps + 1):
        s.add(player_positions[i] >= 0)
        s.add(player_positions[i] < n_sq)
    
    s.add(goal_pos >= 0)
    s.add(goal_pos < n_sq)
    
    # player must be able to reach the goal position after num_steps steps
    s.add(player_positions[num_steps] == goal_pos)
    
    ### movement
    # 0: stay
    # 1: left
    # 2: right
    # 3: up
    # 4: down
    moves = [Int(f'move_{i}') for i in range(num_steps)]
    
    for i,move in enumerate(moves):
        s.add(move >= 0)
        s.add(move < 5)
        
        prev_pos = player_positions[i]
        
        # if the player is at the goal position, don't bother moving
        s.add(Implies(prev_pos == goal_pos, move == 0))
        
        # movement conditions
        s.add(Implies(move == 0, player_positions[i+1] == prev_pos))
        
        s.add(Implies(move == 1, player_positions[i+1] == prev_pos - 1))
        s.add(Implies(move == 1, Select(env, prev_pos - 1) != 1))
        s.add(Implies(move == 1, prev_pos % n >= 1))
        
        s.add(Implies(move == 2, player_positions[i+1] == prev_pos + 1))
        s.add(Implies(move == 2, Select(env, prev_pos + 1) != 1))
        s.add(Implies(move == 2, prev_pos % n < n - 1))
        
        s.add(Implies(move == 3, player_positions[i+1] == prev_pos + n))
        s.add(Implies(move == 3, Select(env, prev_pos + n) != 1))
        s.add(Implies(move == 3, prev_pos < n_sq - n))
        
        s.add(Implies(move == 4, player_positions[i+1] == prev_pos - n))
        s.add(Implies(move == 4, Select(env, prev_pos - n) != 1))
        s.add(Implies(move == 4, prev_pos >= n))
    
    ### check satisfiability and return appropriate data
    result = s.check()
    
    if result == sat:
        m = s.model()
        
        # for d in m.decls():
        #     if d.name() == 'pos_0':
        #         print(m[d])
        
        return [m[player_positions[i]].as_long() for i in range(num_steps + 1)]
    else:
        return None
        
