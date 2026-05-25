from PIL import Image
import os

from z3 import Not, Or, And, IntNumRef, BoolRef
from constants import *

s_int = IntNumRef | int

def Xnor(a, b):
    return Or(And(a, b), And(Not(a), Not(b)))

def are_adjacent(x_1: s_int, y_1: s_int, x_2: s_int, y_2: s_int, n: s_int) -> BoolRef:
    return Or(
        A_below_B(x_1, y_1, x_2, y_2, n),
        A_below_B(x_2, y_2, x_1, y_1, n),
        A_before_B(x_1, y_1, x_2, y_2, n),
        A_before_B(x_2, y_2, x_1, y_1, n),
    )

def A_before_B(x_1: s_int, y_1: s_int, x_2: s_int, y_2: s_int, n: s_int) -> BoolRef:
    return And(x_1 + 1 == x_2, y_1 == y_2, x_1 < n - 1)

def A_below_B(x_1: s_int, y_1: s_int, x_2: s_int, y_2: s_int, n: s_int) -> BoolRef:
    return And(y_1 + 1 == y_2, x_1 == x_2, y_1 < n - 1)


class ImageGen:
    baba_sprite = Image.open(os.path.join('assets', 'baba.png'))
    goal_sprite = Image.open(os.path.join('assets', 'goal.png'))
    wall_sprite = Image.open(os.path.join('assets', 'wall.png'))
    box_sprite = Image.open(os.path.join('assets', 'box.png'))
    wall_text_sprite = Image.open(os.path.join('assets', 'wall_text.png'))
    stop_text_sprite = Image.open(os.path.join('assets', 'stop_text.png'))
    
    def generate(self, model, z3_array, player_pos, n):
        level = Image.new('RGBA', size=(24*n, 24*n), color='#54a54b')

        for i in range(n**2):
            x = i % n
            y = i // n
        
            e = model.evaluate(z3_array[i]).as_long()
            img = None
            
            if e != EMPTY:
                if e == GOAL:
                    img = self.goal_sprite
                elif e == WALL:
                    img = self.wall_sprite
                elif e == BOX:
                    img = self.box_sprite
                elif e == WALL_TXT:
                    img = self.wall_text_sprite
                elif e == STOP_TXT:
                    img = self.stop_text_sprite
                
                level.paste(img, box=(24*x, 24*y), mask=img)
        
        x, y = player_pos
        level.paste(self.baba_sprite, box=(24*x, 24*y), mask=self.baba_sprite)
        
        return level

    # model: z3 model from solver.model()
    # n: length of level grid
    # k: num of steps
    def generate_sequence(self, model, n, k):
        imgs = []

        for i in range(k + 1):
            env_z3 = None
            pos_x = None
            pos_y = None

            for decl in model.decls():
                name = decl.name()
                if name == f'env_{i}':
                    env_z3 = model[decl]
                elif name == f'player_pos_x_{i}':
                    pos_x = model[decl].as_long()
                elif name == f'player_pos_y_{i}':
                    pos_y = model[decl].as_long()

            imgs.append(self.generate(model, env_z3, (pos_x, pos_y), n))
        
        return imgs
