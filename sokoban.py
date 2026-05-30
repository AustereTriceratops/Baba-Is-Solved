from typing import List

from z3 import Array, IntSort, Int, Select, ForAll, And, Or, If, Solver, sat, IntNumRef, ArrayRef, BoolRef

from path import reachable
from utils import A_before_B, check_solver
from constants import *


### level: an (n, n) tile grid. Every entry should be a tile id number from consts.py
### k: number of steps to try
### r: max search length for pathfinding subproblem
def find_solution(level: list[list[int]], start_pos: int, k: int, r = 10):
    n = len(level)
    n_sq = n*n
    
    s = Solver()
    
    n_z3 = Int('n')
    s.add(n_z3 == n)
    
    ### level
    envs = add_level_constraints(s, n_sq, k)
    
    wall_is_stop = add_text_block_constraints(s, n, envs, level, k)
    
    goal_pos = add_goal_constraints(s, n_sq, envs)
    
    ### player positions
    x_positions, y_positions = add_position_constraints(s, n_z3, start_pos, k)
    
    ### moves
    moves = [Int(f'move_{i}') for i in range(k)]
    src_x_arr = [Int(f'src_x_{i}') for i in range(k)]
    src_y_arr = [Int(f'src_y_{i}') for i in range(k)]
    
    # limits on these values and indices
    for i in range(k):
        s.add(moves[i] >= 0)
        s.add(moves[i] < 4)
        
        s.add(And(src_x_arr[i] >= 0, src_x_arr[i] < n))
        s.add(And(src_y_arr[i] >= 0, src_y_arr[i] < n))
    
    for i in range(k):
        add_step_constraints(s, i, n_z3, n_sq, r, envs, moves, x_positions, y_positions, src_x_arr, src_y_arr, wall_is_stop)
    
    ### satisfiability: goal is reachable for player
    is_reachable, _, _ = reachable(
        n_z3, envs[k], x_positions[k], y_positions[k], goal_pos, wall_is_stop[k], max_steps=r, meta_index=k+1
    )
    
    s.add(is_reachable)
    
    return check_solver(s)


def add_goal_constraints(s: Solver, n_sq: int, envs: List[ArrayRef]):
    goal_pos = Int('goal_pos')
    
    s.add(goal_pos >= 0)
    s.add(goal_pos < n_sq)
    
    s.add(Select(envs[0], goal_pos) == GOAL)
    
    return goal_pos


def add_position_constraints(s: Solver, n_z3: IntNumRef, start_pos: int, k: int):
    x_positions = [Int(f'player_pos_x_{i}') for i in range(k + 1)]
    y_positions = [Int(f'player_pos_y_{i}') for i in range(k + 1)]
    
    # basic limits on the range of these indices
    for i in range(k + 1):
        s.add(x_positions[i] >= 0)
        s.add(y_positions[i] >= 0)
        s.add(x_positions[i] < n_z3)
        s.add(y_positions[i] < n_z3)
    
    # init player's starting position and mark goal position
    s.add(x_positions[0] == start_pos % n_z3)
    s.add(y_positions[0] == start_pos / n_z3)
    
    return (x_positions, y_positions)


def add_level_constraints(s: Solver, n_sq: int, k: int):
    envs = [Array(f'env_{i}', IntSort(), IntSort()) for i in range(k + 1)]

    # basic limits on what levels can contain (based on the env names at the top)
    for env in envs:
        for i in range(n_sq):
            s.add(Select(env, i) >= 0)
            s.add(Select(env, i) < TILE_CAP)
    
    return envs


def add_text_block_constraints(s: Solver, n: int, envs: List[ArrayRef], level: List[List[int]],  k: int):
    wall_text_x = [Int(f'wall_text_x_{i}') for i in range(k + 1)]
    wall_text_y = [Int(f'wall_text_y_{i}') for i in range(k + 1)]
    wall_text_present = False
    isstop_text_x = [Int(f'isstop_text_x_{i}') for i in range(k + 1)]
    isstop_text_y = [Int(f'isstop_text_y_{i}') for i in range(k + 1)]
    isstop_text_present = False
    wall_is_stop = [A_before_B(wall_text_x[i], wall_text_y[i], isstop_text_x[i], isstop_text_y[i], n) for i in range(k + 1)]
    
    # init the starting level state
    for i in range(n):
        for j in range(n):
            s.add(Select(envs[0], n*i + j) == level[i][j])
            
            if level[i][j] == WALL_TXT:
                wall_text_present = True
                s.add(wall_text_x[0] == j)
                s.add(wall_text_y[0] == i)
            elif level[i][j] == STOP_TXT:
                isstop_text_present = True
                s.add(isstop_text_x[0] == j)
                s.add(isstop_text_y[0] == i)
    
    if not wall_text_present:
        [s.add(wall_text_x[i] == -2) for i in range(k+1)]
        [s.add(wall_text_y[i] == -1) for i in range(k+1)]
        
    if not isstop_text_present:
        [s.add(isstop_text_x[i] == -1) for i in range(k+1)]
        [s.add(isstop_text_y[i] == -1) for i in range(k+1)]
    
    return wall_is_stop


# for now, only worry about specifying single pushables (no stacks, only one pushable gets pushed)
# TODO: generalize to stacks
def add_step_constraints(s: Solver,
    i: int,
    n_z3: IntNumRef,
    n_sq: int,
    r: int,
    envs: List[ArrayRef],
    moves: List[IntNumRef],
    x_positions: List[IntNumRef],
    y_positions: List[IntNumRef],
    src_x_arr: List[IntNumRef],
    src_y_arr: List[IntNumRef],
    wall_is_stop: List[BoolRef]
):
    src_x = src_x_arr[i]
    src_y = src_y_arr[i]
    src = src_x + n_z3*src_y
    
    dst_x = Int(f'dst_x_{i}')
    dst_y = Int(f'dst_y_{i}')
    dst = dst_x + n_z3*dst_y
    
    opp_x = Int(f'opp_x_{i}') # x of the tile opposite from dst
    opp_y = Int(f'opp_y_{i}') # y of the tile opposite from dst
    opp = opp_x + n_z3*opp_y # tile opposite from dst
    
    src_tile = Select(envs[i], src)
    dst_tile = Select(envs[i], dst)
    opp_tile = Select(envs[i], opp)
    
    # only a box/pushable object gets moved
    s.add(src_tile >= BOX)
    
    # pushables can only be moved to empty tiles
    s.add(dst_tile == EMPTY)
    
    # opposite tile must be traversible and reachable
    s.add(If(
        wall_is_stop[i],
        opp_tile == EMPTY,
        Or(opp_tile == EMPTY, opp_tile == WALL)
    ))
    
    is_reachable, _, _ = reachable(n_z3, envs[i], x_positions[i], y_positions[i], opp, wall_is_stop[i], max_steps=r, meta_index=i)
    s.add(is_reachable)
    
    apply_move(s, i, n_z3, moves, envs, src_x, src_y, dst_x, dst_y, opp_x, opp_y, x_positions, y_positions)

    for j in range(n_sq):
        s.add(If(
            And(j != src, j != dst),
            Select(envs[i+1], j) == Select(envs[i], j),
            True
        ))
    
    s.add(Select(envs[i+1], dst) == src_tile)
    s.add(Select(envs[i+1], src) == EMPTY)
    

### moves
    # 0: left
    # 1: right
    # 2: up
    # 3: down
def apply_move(
    s: Solver,
    i: int,
    n_z3: IntNumRef,
    moves: List[IntNumRef],
    envs: List[ArrayRef],
    src_x, src_y, dst_x, dst_y, opp_x, opp_y, x_positions, y_positions
):
    m_len = Int(f'move_len_{i}')
    s.add(And(m_len > 0, m_len < n_z3))
    m_fa = Int(f'move_forall_{i}')
    
    m0_forall = ForAll([m_fa],
        If(
            And(m_fa >= dst_x, m_fa < src_x),
            Select(envs[i], m_fa + n_z3*dst_y) == EMPTY,
            True
        )
    )
    
    s.add(If(moves[i] == 0,
        And(
            dst_x == src_x - m_len, dst_x >= 0, dst_y == src_y,
            opp_x == src_x + 1, opp_x < n_z3, opp_y == src_y,
            y_positions[i+1] == dst_y, x_positions[i+1] == dst_x + 1,
            m0_forall
        ),
        True
    ))
    
    m1_forall = ForAll([m_fa],
        If(
            And(m_fa > src_x, m_fa <= dst_x),
            Select(envs[i], m_fa + n_z3*dst_y) == EMPTY,
            True
        )
    )
    
    s.add(If(moves[i] == 1,
        And(
            dst_x == src_x + m_len, dst_x < n_z3, dst_y == src_y, 
            opp_x == src_x - 1, opp_x >= 0, opp_y == src_y,
            y_positions[i+1] == dst_y, x_positions[i+1] == dst_x - 1,
            m1_forall
        ),
        True
    ))
    
    m2_forall = ForAll([m_fa],
        If(
            And(m_fa > src_y, m_fa <= dst_y),
            Select(envs[i], dst_x + n_z3*m_fa) == EMPTY,
            True
        )
    )
    
    s.add(If(moves[i] == 2,
        And(
            dst_y == src_y + m_len, dst_y < n_z3, dst_x == src_x,
            opp_y == src_y - 1, opp_y >= 0, opp_x == src_x,
            x_positions[i+1] == dst_x, y_positions[i+1] == dst_y - 1,
            m2_forall
        ),
        True
    ))
    
    m3_forall = ForAll([m_fa],
        If(
            And(m_fa >= dst_y, m_fa < src_y),
            Select(envs[i], dst_x + n_z3*m_fa) == EMPTY,
            True
        )
    )
    
    s.add(If(moves[i] == 3,
        And(
            dst_y == src_y - m_len, dst_y >= 0, dst_x == src_x,
            opp_y == src_y + 1, opp_y < n_z3, opp_x == src_x,
            x_positions[i+1] == dst_x, y_positions[i+1] == dst_y + 1,
            m3_forall
        ),
        True
    ))
