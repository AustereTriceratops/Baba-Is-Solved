from z3 import Array, IntSort, Int, Select, Implies, And, Solver, sat

### env
# 0: empty
# 1: wall
# 2: goal
# 3: pushable

def findSolution(level: list[list[int]], start_pos: int, num_steps: int):
    n = len(level)
    n_sq = n*n
    
    s = Solver()
    
    ### level
    envs = [Array(f'env_{i}', IntSort(), IntSort()) for i in range(num_steps + 1)]

    # basic limits on what levels can contain (based on the env names at the top)
    for env in envs:
        for i in range(n_sq):
            s.add(Select(env, i) >= 0)
            s.add(Select(env, i) < 4)
            
    # init the starting level state
    for i in range(n):
        for j in range(n):
            s.add(Select(envs[0], n*i + j) == level[i][j])
            
    ### player positions
    player_positions = [Int(f'pos_{i}') for i in range(num_steps + 1)]
    goal_pos = Int('goal_pos')
    
    # basic limits on the range of these indices
    for i in range(num_steps + 1):
        s.add(player_positions[i] >= 0)
        s.add(player_positions[i] < n_sq)
    
    s.add(goal_pos >= 0)
    s.add(goal_pos < n_sq)
    
    # init player's starting position and mark goal position
    s.add(player_positions[0] == start_pos)
    s.add(Select(envs[0], goal_pos) == 2)
    
    ### moves
    # 0: stay
    # 1: left
    # 2: right
    # 3: up
    # 4: down
    moves = [Int(f'move_{i}') for i in range(num_steps)]
    moves_src = [Int(f'src_{i}') for i in range(num_steps)]
    moves_dst = [Int(f'dst_{i}') for i in range(num_steps)]
    
    for i in range(num_steps):
        s.add(moves[i] >= 0)
        s.add(moves[i] < 5)
        s.add(moves_src[i] >= 0)
        s.add(moves_src[i] < n_sq)
        s.add(moves_dst[i] >= 0)
        s.add(moves_dst[i] < n_sq)
    
    # satisfiability: goal is reachable for player
    # TODO: add this condition
    # s.add(Reachable(envs[num_steps], player_positions[num_steps], goal_pos))
    
    # for now, only worry about specifying single pushables (no stacks, only one pushable gets pushed)
    # TODO: generalize to stacks
    for i in range(num_steps):
        src = moves_src[i]
        dst = moves_dst[i]
        opp = Int(f'opp_{i}') # tile opposite from dst
        
        # only a box/pushable object gets moved
        s.add(Select(envs[i], src) == 3)
        # pushables can only be moved to empty tiles
        s.add(Select(envs[i], dst) == 0)
        # opposite tile must be traversible and TODO: reachable
        s.add(Select(envs[i], opp) == 0)
        # s.add(Reachable(envs[i], player_positions[i], opp))
        
        # search should effectively stop and set all upcoming moves to 0 as soon as the goal positoon is reachable
        #s.add(Implies(Reachable(envs[i], player_positions[i], goal_pos), moves[i] == 0))
        
        # TODO: add rules relating src and dst according to moves[i]
        # TODO: set opp appropriately too
    
        # level state update
        for j in range(n_sq):
            s.add(Implies(And(j != src, j != dst)), Select(envs[i+1], j) == Select(envs[i], j))
        
        s.add(Select(envs[i+1], dst) == 3)
        s.add(Select(envs[i+1], src) == 0)
        s.add(player_positions[i+1] == src)
    
    result = s.check()
    
    if result == sat:
        m = s.model()
        return m
    else:
        return None        
        
