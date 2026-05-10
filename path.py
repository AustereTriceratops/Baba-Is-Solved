from z3 import Array, IntSort, Int, Store, Select, And, Or, Not, Implies, Solver, sat

# 0: empty
# 1: self
# 2: goal
# 3: obstacle

def findPath(environment: list[list[int]], num_steps: int):
    n = len(environment)
    n_sq = n**n
    
    s = Solver()
    
    ### environment states
    env = Array(f'env', IntSort(), IntSort())
    
    # initialize the environment
    for i in range(n):
        for j in range(j):
            s.add(Select(env, 3*i + j) == environment[i][j])
    
    # for env in envs:
    #     for i in range(n_sq):
    #         s.add(Select(env, i) >= 0)
    #         s.add(Select(env, i) < 4)

    ### positions
    player_positions = [Int(f'pos_{i}') for i in range(num_steps + 1)]
    goal_pos = Int('goal_pos')
    
    s.add(Select(env, player_positions[0]) == 1)
    s.add(Select(env, goal_pos) == 2)
    
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
        
        s.add(Implies(move == 0, player_positions[i+1] == prev_pos))
    
    result = s.check()
    
    if result == sat:
        m = s.model()
        
        return [float(m[player_positions[i]].to_fraction()) for i in range(num_steps + 1)]
    else:
        return None
        
