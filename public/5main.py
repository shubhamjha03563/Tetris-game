import pygame
import random
import time

pygame.init() #initiates pygame and all modules that come with it(compulsory)

move_sound = pygame.mixer.Sound("move.mp3")
game_over_sound = pygame.mixer.Sound("over.mp3")
clear_sound = pygame.mixer.Sound("clear.mp3")
pygame.mixer.music.load("start.mp3")


# creating the data structure for shapes
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 500
s_height = 600
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = 0
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class shape(object):
    def  __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[(128, 128, 128)for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range (len(grid[i])):
            if (j, i) in locked_pos: 
                grid[i][j] = locked_pos[(j, i)]
    return grid

def convert_shape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x+j, shape.y+i))
    for i, pos in enumerate(positions):
        positions[i] = pos[0] - 2, pos[1] - 4

    return positions

def valid_space(shape, grid):
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (128, 128, 128)] for i in range(20)]
    valid_pos = [j for sub in valid_pos for j in sub]
    formatted = convert_shape(shape)

    for pos in formatted:
        if pos not in valid_pos:
            if pos[1] > -1:
                return False
    return True

def game_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False 

def random_shape():
    return shape(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):  
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x+ play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))  
   
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (255, 255, 255), (sx, sy+ i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (255, 255, 255), (sx + j*block_size, sy), (sx + j*block_size, sy+play_height))
    
def clear_rows(grid, locked):
    global speed
    inc = 0
    for i in range(len(grid)-1, -1, -1): # https://www.w3schools.com/python/ref_func_range.asp
        row = grid[i]
        if (128, 128, 128) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    pygame.mixer.Sound.play(clear_sound)
                    speed += 0.04
                    del locked[(j, i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[:: -1]: 
            #https://www.geeksforgeeks.org/sorted-function-python/
            #https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
            x, y = key                                               
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key) #https://www.geeksforgeeks.org/python-dictionary-pop-method/

    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j* block_size, sy + i * block_size, block_size -1, block_size-1))
    
    surface.blit(label, (sx+10, sy-30))

def draw_window(surface, grid, score = 0):
    surface.fill((0, 0, 0))
    pygame.font.init()

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score:' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)): 
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x+j*block_size, top_left_y+i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)

def main(win):
    game = True
    while True:    
        global speed
        locked_positions = {}
        grid = create_grid(locked_positions)

        change_shape = False
        run = True
        current_shape = random_shape()
        next_shape = random_shape()
        clock = pygame.time.Clock()
        score = 0
        speed = 4
        pygame.mixer.music.play(-1)

        while run:
            grid = create_grid(locked_positions)
            clock.tick(speed)
            current_shape.y += 1
            if not(valid_space(current_shape, grid)) and current_shape.y > 0:
                current_shape.y -= 1
                change_shape = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pygame.mixer.Sound.play(move_sound)
                        current_shape.x -= 1
                        if not(valid_space(current_shape, grid)):
                            current_shape.x +=1
                    if event.key == pygame.K_RIGHT:
                        pygame.mixer.Sound.play(move_sound)
                        current_shape.x += 1
                        if not(valid_space(current_shape, grid)):
                            current_shape.x -=1
                    if event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(move_sound)
                        current_shape.y += 1
                        if not(valid_space(current_shape, grid)):
                            current_shape.y -=1
                    if event.key == pygame.K_UP:
                        pygame.mixer.Sound.play(move_sound)
                        current_shape.rotation += 1
                        if not(valid_space(current_shape, grid)):
                            current_shape.rotation -=1

            shape_pos = convert_shape(current_shape)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_shape.color
            
            if change_shape:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_shape.color
                current_shape = next_shape
                next_shape = random_shape()
                change_shape = False
                score += clear_rows(grid, locked_positions)

            draw_window(win, grid, score)
            draw_next_shape(next_shape, win)
            pygame.display.update()

            if game_lost(locked_positions):
                draw_text_middle(win, "GAME OVER!", 50, (255, 255, 255))
                pygame.display.update()
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(game_over_sound)
                pygame.time.delay(4000)
                run = False
             
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TETRIS')
main(win)  # start game
pygame.quit()
quit()







