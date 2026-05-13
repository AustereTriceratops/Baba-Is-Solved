from z3 import Array, IntSort, Int, Select, Implies, And, Solver, sat

from path import reachable

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
    # 0: left
    # 1: right
    # 2: up
    # 3: down
    moves = [Int(f'move_{i}') for i in range(num_steps)]
    moves_src = [Int(f'src_{i}') for i in range(num_steps)]
    moves_dst = [Int(f'dst_{i}') for i in range(num_steps)]
    
    # limits on these values and indices
    for i in range(num_steps):
        s.add(moves[i] >= 0)
        s.add(moves[i] < 4)
        s.add(moves_src[i] >= 0)
        s.add(moves_src[i] < n_sq)
        s.add(moves_dst[i] >= 0)
        s.add(moves_dst[i] < n_sq)
    
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
        # opposite tile must be traversible and reachable
        s.add(Select(envs[i], opp) == 0)
        is_reachable, _ = reachable(n, envs[i], player_positions[i], opp, 20, meta_index=i+1)
        s.add(is_reachable)
        
        # # search should effectively stop and set all upcoming moves to 0 as soon as the goal positoon is reachable
        # # TODO: implement early stopping in some way like in path.py?
        # is_reachable, _ = reachable(n, envs[i], player_positions[i], opp, 20, meta_index=num_steps+i+1)
        # s.add(Implies(is_reachable, moves[i] == 0))
        
        ### moves
        s.add(Implies(moves[i] == 0, dst == src - 1))
        s.add(Implies(moves[i] == 0, opp == src + 1))
        s.add(Implies(moves[i] == 0, src % n > 0))
        s.add(Implies(moves[i] == 0, src % n < n - 1))
        
        s.add(Implies(moves[i] == 1, dst == src + 1))
        s.add(Implies(moves[i] == 1, opp == src - 1))
        s.add(Implies(moves[i] == 1, src % n > 0))
        s.add(Implies(moves[i] == 1, src % n < n - 1))
        
        s.add(Implies(moves[i] == 2, dst == src + n))
        s.add(Implies(moves[i] == 2, opp == src - n))
        s.add(Implies(moves[i] == 2, src > n - 1))
        s.add(Implies(moves[i] == 2, src < n_sq - n))
        
        s.add(Implies(moves[i] == 3, dst == src - n))
        s.add(Implies(moves[i] == 3, opp == src + n))
        s.add(Implies(moves[i] == 3, src > n - 1))
        s.add(Implies(moves[i] == 3, src < n_sq - n))
    
        # level state update
        for j in range(n_sq):
            s.add(Implies(And(j != src, j != dst), Select(envs[i+1], j) == Select(envs[i], j)))
        
        s.add(Select(envs[i+1], dst) == 3)
        s.add(Select(envs[i+1], src) == 0)
        s.add(player_positions[i+1] == src)
    
    ### satisfiability: goal is reachable for player
    is_reachable, _ = reachable(n, envs[num_steps], player_positions[num_steps], goal_pos, 20, meta_index=0)
    s.add(is_reachable)
    
    result = s.check()
    
    if result == sat:
        m = s.model()
        return m
    else:
        return None        
        
