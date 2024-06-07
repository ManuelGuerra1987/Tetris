import pygame, sys, random


class Colors:
    dark_grey = (26, 31, 40) # grid
    green = (47, 230, 23) # id 1
    red = (232, 18, 18) # id 2
    orange = (226, 116, 17) # id 3
    yellow = (237, 234, 4) # id 4
    purple = (166, 0, 247) # id 5
    cyan = (21, 204, 209) # id 6
    blue = (13, 64, 216) # id 7

    @classmethod
    def get_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)] # 20x10 zero matrix
        self.colours = Colors.get_colors()
                       
 
    def draw(self,screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column] 
                cell_rect = pygame.Rect(column*self.cell_size + 1,row*self.cell_size + 1,self.cell_size - 1,self.cell_size - 1) # x,y,w,h
                pygame.draw.rect(screen,self.colours[cell_value],cell_rect) # display surface,color,rect object 

    def is_inside(self, row, column): # check if position given is inside grid
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False 
    
    def is_empty(self, row, column): # check if grid position given is empty
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True    

    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self): # check all rows from bottom to top, eliminate full rows, move down incomplete rows
        completed = 0
        for row in range(self.num_rows - 1, 0, -1): # from bottom to top
            if self.is_row_full(row): 
                self.clear_row(row) 
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed) # move down incomplete rows
        return completed       

    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0 

class Block:
    def __init__(self,id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.colours = Colors.get_colors()
        self.row_offset = 0
        self.column_offset = 0

    def move(self,rows,column):
        self.row_offset += rows
        self.column_offset += column

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state > 3:
            self.rotation_state = 0   

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == -1:
            self.rotation_state = 3

    def get_cell_positions(self): #calculate actual position of each block cell after the offset is applied
        tiles = self.cells[self.rotation_state] # default cell position
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles        

    def draw(self,screen, offset_x, offset_y): #offset is necesary for drawing next block
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column*self.cell_size + 1,offset_y + tile.row*self.cell_size + 1,self.cell_size - 1,self.cell_size - 1) 
            pygame.draw.rect(screen,self.colours[self.id],tile_rect)
    

class Position: # in order to represent a position in the grid with a single object
    def __init__(self,row,column):
        self.row = row
        self.column = column


class LBlock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0,2), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(2,1), Position(2,2)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,0)],
            3: [Position(0,0), Position(0,1), Position(1,1), Position(2,1)],
        }
        self.move(0,3) # so that it starts centered

class JBlock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0,3)

class IBlock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }     
        self.move(-1,3)   

class OBlock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            1: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            2: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)],
            3: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.move(0,4)

class SBlock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }  
        self.move(0,3)

class TBlock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0,3)

class ZBlock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }   
        self.move(0,3)     


class Game: # container for all the elements of the game
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(),ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 0, 0)  
        self.next_block.draw(screen, 270, 270) 

    def get_random_block(self):  
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(),ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block) 
        return block   
    
    def block_inside(self): # check if the block is inside the screen
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row,tile.column) == False: # check for each cell in the block if it is inside the screen
                return False
        return True    

    def block_fits(self): # for each cell of the tetrimino check if it collides with something or not
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True  

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()  

    def move_left(self):
        self.current_block.move(0, -1)  
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1) # If it leaves the screen or collides with another block, undo the move

    def move_right(self):
        self.current_block.move(0, 1)  
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)   

    def move_down(self):
        self.current_block.move(1, 0)  
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0) 
            self.lock_block() 
            self.check_full_rows()
            self.spawn()
           
    def lock_block(self): # upgrade grid values with location of each cell of the block at the time it touches the bottom
        tiles = self.current_block.get_cell_positions()
        for position in tiles: 
            self.grid.grid[position.row][position.column] = self.current_block.id 
        
    def check_full_rows(self): 
        rows_creared = self.grid.clear_full_rows()  
        self.update_score(rows_creared)
        
    def spawn(self): # New spawn of block. If the new spawn block does not fits, the game is over
        self.current_block = self.next_block 
        self.next_block = self.get_random_block() 
        if self.block_fits() == False: 
            self.game_over = True 

    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 200 
        elif lines_cleared == 3:
            self.score += 300  
        elif lines_cleared > 3:
            self.score += 500     

    def reset(self):
        self.grid.reset()    
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(),ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0



# Game Loop: Event handling, updating positions and drawing objects

pygame.init()    
screen = pygame.display.set_mode((500,605)) # w, h
pygame.display.set_caption("Tetris")
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score: ", True, (255,255,255))
score_rect = pygame.Rect(320, 55, 170, 60)
next_surface = title_font.render("Next: ", True, (255,255,255))
next_rect = pygame.Rect(320, 215, 170, 180)
game_over_surface = title_font.render("GAME OVER", True, (255,255,255))
clock = pygame.time.Clock()
game = Game()

GAME_UPDATE = pygame.USEREVENT # to control the speed of falling blocks. Triggers an event every 400ms
pygame.time.set_timer(GAME_UPDATE,400) # updates every 400 milliseconds

while True:

    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game.game_over == True:
                game.game_over = False
                game.reset()

            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down() 
                game.score += 1
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()   

        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()       

    #drawing

    screen.fill((44,44,127))   # (red, green, blue)
    screen.blit(score_surface, (365, 20, 50, 50)) # draw score text
    pygame.draw.rect(screen, (59, 85, 162), score_rect, 0, 10) # draw score rect
    screen.blit(next_surface, (365, 180, 50, 50)) # draw next text
    pygame.draw.rect(screen, (59, 85, 162), next_rect, 0, 10) # draw next rect
    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50, 50)) # draw game over text
    score_value_surface = title_font.render(str(game.score), True, (255, 255, 255)) 
    screen.blit(score_value_surface, (365, 70, 50, 50))   
    game.draw(screen)
    pygame.display.update() # This line takes all the changes we made in the game objects and draws a pic for them    
    clock.tick(60) # 60 frames per second. All the code inside the while loop will run 60 times per second