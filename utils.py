from PIL import Image
import os

from z3 import Or, And, IntNumRef, BoolRef

s_int = IntNumRef | int

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
    box_sprite = Image.open(os.path.join('assets', 'box.png'))
    wall_sprite = Image.open(os.path.join('assets', 'wall.png'))
    goal_sprite = Image.open(os.path.join('assets', 'goal.png'))
    
    def generate(self, model, z3_array, n):
        level = Image.new('RGB', size=(24*n, 24*n), color='#54a54b')

        for i in range(n**2):
            x = i % n
            y = i // n
        
            e = model.evaluate(z3_array[i]).as_long()
            img = None
            
            if e != 0:
                if e == 1:
                    img = self.goal_sprite
                elif e == 2:
                    img = self.wall_sprite
                elif e == 3:
                    img = self.box_sprite
                
                level.paste(img, box=(24*x, 24*y))
        
        return level

    # model: z3 model from solver.model()
    # n: length of level grid
    # k: num of steps
    def generate_sequence(self, model, n, k):
        imgs = []

        for i in range(k + 1):
            env_z3 = None

            for decl in model.decls():
                if decl.name() == f'env_{i}':
                    env_z3 = model[decl]

            imgs.append(self.generate(model, env_z3, n))
        
        return imgs
