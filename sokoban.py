from z3 import Array, IntSort, Int, Select, Implies, And, Solver, sat

from path import reachable

### env
# 0: empty
# 1: goal
# 2: wall
# 3: pushable
# k: number of steps to try
def findSolution(level: list[list[int]], start_pos: int, k: int):
    n = len(level)
    n_sq = n*n
    
    s = Solver()
    
    n_z3 = Int('n')
    s.add(n_z3 == n)
    
    ### level
    envs = [Array(f'env_{i}', IntSort(), IntSort()) for i in range(k + 1)]

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
    x_positions = [Int(f'player_pos_x_{i}') for i in range(k + 1)]
    y_positions = [Int(f'player_pos_y_{i}') for i in range(k + 1)]
    goal_pos = Int('goal_pos')
    
    # basic limits on the range of these indices
    for i in range(k + 1):
        s.add(x_positions[i] >= 0)
        s.add(y_positions[i] >= 0)
        s.add(x_positions[i] < n_z3)
        s.add(y_positions[i] < n_z3)
    
    s.add(goal_pos >= 0)
    s.add(goal_pos < n_sq)
    
    # init player's starting position and mark goal position
    s.add(x_positions[0] == start_pos % n_z3)
    s.add(y_positions[0] == start_pos / n_z3)
    s.add(Select(envs[0], goal_pos) == 1)
    
    ### moves
    moves = [Int(f'move_{i}') for i in range(k)]
    src_x_arr = [Int(f'src_x_{i}') for i in range(k)]
    src_y_arr = [Int(f'src_y_{i}') for i in range(k)]
    dst_x_arr = [Int(f'dst_x_{i}') for i in range(k)]
    dst_y_arr = [Int(f'dst_y_{i}') for i in range(k)]
    
    # limits on these values and indices
    for i in range(k):
        s.add(moves[i] >= 0)
        s.add(moves[i] < 4)
        
        s.add(And(src_x_arr[i] >= 0, src_x_arr[i] < n))
        s.add(And(src_y_arr[i] >= 0, src_y_arr[i] < n))
        
        s.add(And(dst_x_arr[i] >= 0, dst_x_arr[i] < n))
        s.add(And(dst_y_arr[i] >= 0, dst_y_arr[i] < n))
    
    # for now, only worry about specifying single pushables (no stacks, only one pushable gets pushed)
    # TODO: generalize to stacks
    for i in range(k):
        src_x = src_x_arr[i]
        src_y = src_y_arr[i]
        src = src_x + n*src_y
        
        dst_x = dst_x_arr[i]
        dst_y = dst_y_arr[i]
        dst = dst_x + n*dst_y
        
        opp_x = Int(f'opp_x_{i}') # x of the tile opposite from dst
        opp_y = Int(f'opp_y_{i}') # y of the tile opposite from dst
        opp = opp_x + n*opp_y # tile opposite from dst
        
        # only a box/pushable object gets moved
        s.add(Select(envs[i], src) == 3)
        # pushables can only be moved to empty tiles
        s.add(Select(envs[i], dst) == 0)
        # opposite tile must be traversible and reachable
        s.add(Select(envs[i], opp) == 0)
        is_reachable, _, _ = reachable(n_z3, envs[i], x_positions[i], y_positions[i], opp, 20, meta_index=i+1)
        s.add(is_reachable)
        
        # # search should effectively stop and set all upcoming moves to 0 as soon as the goal positoon is reachable
        # # TODO: implement early stopping in some way like in path.py?
        # is_reachable, _ = reachable(n, envs[i], player_positions[i], opp, 20, meta_index=k+i+1)
        # s.add(Implies(is_reachable, moves[i] == 0))
        
        ### moves
        # 0: left
        # 1: right
        # 2: up
        # 3: down
        s.add(Implies(moves[i] == 0,
            And(
                dst_x == src_x - 1, dst_y == src_y,
                src_x > 0, src_x < n - 1,
                opp_x == src_x + 1, opp_y == src_y
            )
        ))
        
        s.add(Implies(moves[i] == 1,
            And(
                dst_x == src_x + 1, dst_y == src_y, 
                src_x > 0, src_x < n - 1, 
                opp_x == src_x - 1, opp_y == src_y
            )   
        ))
        
        s.add(Implies(moves[i] == 2,
            And(
                dst_y == src_y + 1, dst_x == src_x,
                src_y > 0, src_y < n - 1,
                opp_y == src_y - 1, opp_x == src_x,
            )
        ))
        
        s.add(Implies(moves[i] == 3,
            And(
                dst_y == src_y - 1, dst_x == src_x,
                src_y > 0, src_y < n - 1,
                opp_y == src_y + 1, opp_x == src_x,
            )
        ))
    
        for j in range(n_sq):
            s.add(Implies(And(j != src, j != dst), Select(envs[i+1], j) == Select(envs[i], j)))
        
        s.add(Select(envs[i+1], dst) == 3)
        s.add(Select(envs[i+1], src) == 0)
        s.add(x_positions[i+1] == src_x)
        s.add(y_positions[i+1] == src_y)
    
    ### satisfiability: goal is reachable for player
    is_reachable, _, _ = reachable(
        n_z3, envs[k], x_positions[k], y_positions[k], goal_pos, 20, meta_index=0
    )
    
    s.add(is_reachable)
    
    result = s.check()
    
    if result == sat:
        m = s.model()
        return m
    else:
        return None        
        
