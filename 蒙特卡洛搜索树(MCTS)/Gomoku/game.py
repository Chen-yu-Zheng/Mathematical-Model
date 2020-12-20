# encoding:utf-8
import pygame
import random
import os
from settings import *
from sprites import *
from status import *
import ai2
import ai1
import sys
import copy





class Game:
    def __init__(self):
        #// initialize pygame and create window
        #initialize the game
        pygame.init()
        #tackle the music of soundEffect
        pygame.mixer.init()
        #create a game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #set a title
        pygame.display.set_caption(TITLE)
        #to make a time clock
        #which used to control the speed , monitor the process and ensure the fps runing normally 
        self.clock =  pygame.time.Clock()
        pygame.key.set_repeat(500, 100)  # hold on for half a second and you will have a keytype repeat , when repeat, keeping time is 0.1s
        self.load_data()
        self.clock =  pygame.time.Clock()
        self.running = True
        # self.game_over = False
        self.result = 2
        self.font_name = pygame.font.match_font(FONT_NAME)

    def load_data(self):
        pass

    def new(self):
        # Initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 1, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        self.run()

    def run(self):
        # game loop - set self playing = False to end the game
        self.playing = True
        while self.playing:
            # self.dt = self.clock.tick(FPS) / 1000
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(X_MIN_BOUND, X_MAX_BOUND + 1, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, X_MIN_BOUND), (x, X_MAX_BOUND))
        for y in range(Y_MIN_BOUND, Y_MAX_BOUND + 1, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (Y_MIN_BOUND, y), (Y_MAX_BOUND, y))


    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

        
   
        
    def add_to_matrix(self):
        # add the player's step to the status_matrix
        status_matrix[self.player.x][self.player.y] = 1
        self.judge_double_4(self.player.x, self.player.y)
        self.judge_double_3()
        
        

    def add_to_matrix_enemy(self):
        status_matrix[self.enemy.x][self.enemy.y] = 2


    def search_live_3(self, matrix):
        live_3_count = 0

        # ooo style 3
        for i in range(1, SIZE - 3):
            for j in range(1, SIZE - 3):
                if (matrix[i][j] == 0 and matrix[i + 1][j] == 1 and matrix[i + 2][j] == 1 and matrix[i + 3][j] == 1 and matrix[i + 4][j] == 0) or \
                    (matrix[i][j] == 0 and matrix[i][j + 1] == 1 and matrix[i][j + 2] == 1 and matrix[i][j + 3] == 1 and matrix[i][j + 4] == 0) or \
                    (matrix[i][j] == 0 and matrix[i + 1][j + 1] == 1 and matrix[i + 2][j + 2] == 1 and matrix[i + 3][j + 3] == 1 and matrix[i + 4][j + 4] == 0):
                    live_3_count += 1
                    
                    

        for i in range(SIZE - 3, SIZE + 1):
            for j in range(1, SIZE - 3):
                if matrix[i][j] == 0 and matrix[i][j + 1] == 1 and matrix[i][j + 2] == 1 and matrix[i][j + 3] == 1 and matrix[i][j + 4] == 0:
                    live_3_count += 1

        for j in range(SIZE - 3, SIZE + 1):
            for i in range(1, SIZE - 3):
                if matrix[i][j] == 0 and matrix[i + 1][j] == 1 and matrix[i + 2][j] == 1 and matrix[i + 3][j] == 1 and matrix[i + 4][j] == 0:            
                    live_3_count += 1

        for i in range(1, SIZE - 3):
            for j in range(5, SIZE + 1):
                if matrix[i][j] == 0 and matrix[i + 1][j - 1] == 1 and matrix[i + 2][j - 2] == 1 and matrix[i + 3][j - 3] == 1 and matrix[i + 4][j - 4] == 0:
                    live_3_count += 1


        # oo_o style 3
        for i in range(1, SIZE - 4):
            for j in range(1, SIZE - 4):
                if (matrix[i][j] == 0 and matrix[i + 1][j] == 1 and matrix[i + 2][j] == 0 and matrix[i + 3][j] == 1 and matrix[i + 4][j] == 1 and matrix[i + 5][j] == 0) or \
                    (matrix[i][j] == 0 and matrix[i][j + 1] == 1 and matrix[i][j + 2] == 0 and matrix[i][j + 3] == 1 and matrix[i][j + 4] == 1 and matrix[i][j + 5] == 0) or \
                    (matrix[i][j] == 0 and matrix[i + 1][j + 1] == 1 and matrix[i + 2][j + 2] == 0 and matrix[i + 3][j + 3] == 1 and matrix[i + 4][j + 4] == 1 and matrix[i + 5][j + 5] == 0):
                    live_3_count += 1
                if (matrix[i][j] == 0 and matrix[i + 1][j] == 1 and matrix[i + 2][j] == 1 and matrix[i + 3][j] == 0 and matrix[i + 4][j] == 1 and matrix[i + 5][j] == 0) or \
                    (matrix[i][j] == 0 and matrix[i][j + 1] == 1 and matrix[i][j + 2] == 1 and matrix[i][j + 3] == 0 and matrix[i][j + 4] == 1 and matrix[i][j + 5] == 0) or \
                    (matrix[i][j] == 0 and matrix[i + 1][j + 1] == 1 and matrix[i + 2][j + 2] == 1 and matrix[i + 3][j + 3] == 0 and matrix[i + 4][j + 4] == 1 and matrix[i + 5][j + 5] == 0):
                    live_3_count += 1
                    
                    

        for i in range(SIZE - 4, SIZE + 1):
            for j in range(1, SIZE - 4):
                if matrix[i][j] == 0 and matrix[i][j + 1] == 1 and matrix[i][j + 2] == 0 and matrix[i][j + 3] == 1 and matrix[i][j + 4] == 1 and matrix[i][j + 4] == 0:
                    live_3_count += 1
                if matrix[i][j] == 0 and matrix[i][j + 1] == 1 and matrix[i][j + 2] == 1 and matrix[i][j + 3] == 0 and matrix[i][j + 4] == 1 and matrix[i][j + 4] == 0:
                    live_3_count += 1

        for j in range(SIZE - 4, SIZE + 1):
            for i in range(1, SIZE - 4):
                if matrix[i][j] == 0 and matrix[i + 1][j] == 1 and matrix[i + 2][j] == 0 and matrix[i + 3][j] == 1 and matrix[i + 4][j] == 1 and matrix[i + 5][j] == 0:            
                    live_3_count += 1
                if matrix[i][j] == 0 and matrix[i + 1][j] == 1 and matrix[i + 2][j] == 1 and matrix[i + 3][j] == 0 and matrix[i + 4][j] == 1 and matrix[i + 5][j] == 0:            
                    live_3_count += 1

        for i in range(1, SIZE - 4):
            for j in range(6, SIZE + 1):
                if matrix[i][j] == 0 and matrix[i + 1][j - 1] == 1 and matrix[i + 2][j - 2] == 0 and matrix[i + 3][j - 3] == 1 and matrix[i + 4][j - 4] == 1 and matrix[i + 5][j - 5] == 0:
                    live_3_count += 1
                if matrix[i][j] == 0 and matrix[i + 1][j - 1] == 1 and matrix[i + 2][j - 2] == 1 and matrix[i + 3][j - 3] == 0 and matrix[i + 4][j - 4] == 1 and matrix[i + 5][j - 5] == 0:
                    live_3_count += 1

        return live_3_count

    def judge_double_3(self):
        # judge double 3 balance breaker
        
        temp_matrix = copy.deepcopy(status_matrix)
        # print(status_matrix)
        # temp_matrix[a][b] = 1
        if self.search_live_3(temp_matrix) >= 2:
            self.result = 3
                    
            if self.playing:
                self.playing = False
            self.running = False

        
    def judge_double_4(self, a, b):
        # judge double 4 balance breaker
        live_4_flag = 0
        temp_matrix = copy.deepcopy(status_matrix)
        # print(status_matrix)
        temp_matrix[a][b] = 1
        if a == 1 and b == 1:
            if temp_matrix[a + 1][b + 1] == 0:
                temp_matrix[a + 1][b + 1] = 1
            if temp_matrix[a][b + 1] == 0:
                temp_matrix[a][b + 1] = 1
            if temp_matrix[a + 1][b] == 0:
                temp_matrix[a + 1][b] = 1

        elif a == SIZE and b == SIZE:
            if temp_matrix[a - 1][b - 1] == 0:
                temp_matrix[a - 1][b - 1] = 1
            if temp_matrix[a][b - 1] == 0:
                temp_matrix[a][b - 1] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1

        elif a == 1 and b == SIZE:
            if temp_matrix[a][b - 1] == 0:
                temp_matrix[a][b - 1] = 1
            if temp_matrix[a + 1][b - 1] == 0:
                temp_matrix[a + 1][b - 1] = 1
            if temp_matrix[a + 1][b] == 0:
                temp_matrix[a + 1][b] = 1

        elif a == SIZE and b == 1:
            if temp_matrix[a][b + 1] == 0:
                temp_matrix[a][b + 1] = 1
            if temp_matrix[a - 1][b + 1] == 0:
                temp_matrix[a - 1][b + 1] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1

        elif a == 1 and b != 1 and b != SIZE:
            if temp_matrix[a][b - 1] == 0:
                temp_matrix[a][b - 1] = 1
            if temp_matrix[a][b + 1] == 0:
                temp_matrix[a][b + 1] = 1
            if temp_matrix[a + 1][b] == 0:
                temp_matrix[a + 1][b] = 1
            if temp_matrix[a + 1][b - 1] == 0:
                temp_matrix[a + 1][b - 1] = 1
            if temp_matrix[a + 1][b + 1] == 0:
                temp_matrix[a + 1][b + 1] = 1

        elif a != 1 and b == 1 and a != SIZE:
            if temp_matrix[a][b + 1] == 0:
                temp_matrix[a][b + 1] = 1
            if temp_matrix[a - 1][b+ 1] == 0:
                temp_matrix[a - 1][b + 1] = 1
            if temp_matrix[a + 1][b + 1] == 0:
                temp_matrix[a + 1][b + 1] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1
            if temp_matrix[a + 1][b] == 0:
                temp_matrix[a + 1][b] = 1

        elif a != SIZE and b == SIZE and a != 1:
            if temp_matrix[a][b - 1] == 0:
                temp_matrix[a][b - 1] = 1
            if temp_matrix[a - 1][b - 1] == 0:
                temp_matrix[a - 1][b - 1] = 1
            if temp_matrix[a + 1][b - 1] == 0:
                temp_matrix[a + 1][b - 1] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1
            if temp_matrix[a + 1][b] == 0:
                temp_matrix[a + 1][b] = 1

        elif b != SIZE and a == SIZE and b != 1:
            if temp_matrix[a][b - 1] == 0:
                temp_matrix[a][b - 1] = 1
            if temp_matrix[a - 1][b - 1] == 0:
                temp_matrix[a - 1][b - 1] = 1
            if temp_matrix[a][b + 1] == 0:
                temp_matrix[a][b + 1] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1

        else:
            if temp_matrix[a - 1][b - 1] == 0:
                temp_matrix[a - 1][b - 1] = 1
            if temp_matrix[a - 1][b] == 0:
                temp_matrix[a - 1][b] = 1
            if temp_matrix[a - 1][b + 1] == 0:
                temp_matrix[a - 1][b + 1] = 1
            if temp_matrix[a][b + 1] == 0:
                temp_matrix[a][b + 1] = 1
            if temp_matrix[a][b - 1] == 0:
                temp_matrix[a][b - 1] = 1
            if temp_matrix[a + 1][b - 1] == 0:
                temp_matrix[a + 1][b - 1] = 1
            if temp_matrix[a + 1][b] == 0:
                temp_matrix[a + 1][b] = 1
            if temp_matrix[a + 1][b + 1] == 0:
                temp_matrix[a + 1][b + 1] = 1
   
        # print(temp_matrix)

        for i in range(1, SIZE - 3):
            for j in range(1, SIZE - 3):
                if (temp_matrix[i][j] == 1 and temp_matrix[i + 1][j] == 1 and temp_matrix[i + 2][j] == 1 and temp_matrix[i + 3][j] == 1 and temp_matrix[i + 4][j] == 1) or \
                    (temp_matrix[i][j] == 1 and temp_matrix[i][j + 1] == 1 and temp_matrix[i][j + 2] == 1 and temp_matrix[i][j + 3] == 1 and temp_matrix[i][j + 4] == 1) or \
                    (temp_matrix[i][j] == 1 and temp_matrix[i + 1][j + 1] == 1 and temp_matrix[i + 2][j + 2] == 1 and temp_matrix[i + 3][j + 3] == 1 and temp_matrix[i + 4][j + 4] == 1):
                    live_4_flag += 1
                    

        for i in range(SIZE - 3, SIZE + 1):
            for j in range(1, SIZE - 3):
                if temp_matrix[i][j] == 1 and temp_matrix[i][j + 1] == 1 and temp_matrix[i][j + 2] == 1 and temp_matrix[i][j + 3] == 1 and temp_matrix[i][j + 4] == 1:
                    live_4_flag += 1
                    

        for j in range(SIZE - 3, SIZE + 1):
            for i in range(1, SIZE - 3):
                if temp_matrix[i][j] == 1 and temp_matrix[i + 1][j] == 1 and temp_matrix[i + 2][j] == 1 and temp_matrix[i + 3][j] == 1 and temp_matrix[i + 4][j] == 1:            
                    live_4_flag += 1

        for i in range(1, SIZE - 3):
            for j in range(5, SIZE + 1):
                if temp_matrix[i][j] == 1 and temp_matrix[i + 1][j - 1] == 1 and temp_matrix[i + 2][j - 2] == 1 and temp_matrix[i + 3][j - 3] == 1 and temp_matrix[i + 4][j - 4] == 1:
                    live_4_flag += 1

        
                    
        if live_4_flag >= 2:
            self.result = 3
                    
            if self.playing:
                self.playing = False
            self.running = False
        # long connection judge (because 7 or longer connection must have a stage of 6 connection, so we only need to judge 6 connection situation)
        for i in range(1, SIZE - 4):
            for j in range(1, SIZE - 4):
                if (temp_matrix[i][j] == 1 and temp_matrix[i + 1][j] == 1 and temp_matrix[i + 2][j] == 1 and temp_matrix[i + 3][j] == 1 and temp_matrix[i + 4][j] == 1 and temp_matrix[i + 5][j] == 1) or \
                    (temp_matrix[i][j] == 1 and temp_matrix[i][j + 1] == 1 and temp_matrix[i][j + 2] == 1 and temp_matrix[i][j + 3] == 1 and temp_matrix[i][j + 4] == 1 and temp_matrix[i][j + 5] == 1) or \
                    (temp_matrix[i][j] == 1 and temp_matrix[i + 1][j + 1] == 1 and temp_matrix[i + 2][j + 2] == 1 and temp_matrix[i + 3][j + 3] == 1 and temp_matrix[i + 4][j + 4] == 1 and temp_matrix[i + 5][j + 5] == 1):
                    self.result = 0
                    
                    if self.playing == False:
                        self.playing = True
                    self.running = True

        for i in range(SIZE - 4, SIZE + 1):
            for j in range(1, SIZE - 4):
                if temp_matrix[i][j] == 1 and temp_matrix[i][j + 1] == 1 and temp_matrix[i][j + 2] == 1 and temp_matrix[i][j + 3] == 1 and temp_matrix[i][j + 4] == 1 and temp_matrix[i][j + 5] == 1:
                    self.result = 0
                    
                    if self.playing == False:
                        self.playing = True
                    self.running = True

        for j in range(SIZE - 4, SIZE + 1):
            for i in range(1, SIZE - 4):
                if temp_matrix[i][j] == 1 and temp_matrix[i + 1][j] == 1 and temp_matrix[i + 2][j] == 1 and temp_matrix[i + 3][j] == 1 and temp_matrix[i + 4][j] == 1 and temp_matrix[i + 5][j] == 1:            
                    self.result = 0
                    
                    if self.playing == False:
                        self.playing = True
                    self.running = True

        for i in range(1, SIZE - 4):
            for j in range(4, SIZE + 1):
                if temp_matrix[i][j] == 1 and temp_matrix[i + 1][j - 1] == 1 and temp_matrix[i + 2][j - 2] == 1 and temp_matrix[i + 3][j - 3] == 1 and temp_matrix[i + 4][j - 4] == 1 and temp_matrix[i + 5][j - 5] == 1:
                    self.result = 0
                    
                    if self.playing == False:
                        self.playing = True
                    self.running = True



    def judge_player(self):
        for i in range(1, SIZE - 3):
            for j in range(1, SIZE - 3):
                if (status_matrix[i][j] == 1 and status_matrix[i + 1][j] == 1 and status_matrix[i + 2][j] == 1 and status_matrix[i + 3][j] == 1 and status_matrix[i + 4][j] == 1) or \
                    (status_matrix[i][j] == 1 and status_matrix[i][j + 1] == 1 and status_matrix[i][j + 2] == 1 and status_matrix[i][j + 3] == 1 and status_matrix[i][j + 4] == 1) or \
                    (status_matrix[i][j] == 1 and status_matrix[i + 1][j + 1] == 1 and status_matrix[i + 2][j + 2] == 1 and status_matrix[i + 3][j + 3] == 1 and status_matrix[i + 4][j + 4] == 1):
                    self.result = 1
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for i in range(SIZE - 3, SIZE + 1):
            for j in range(1, SIZE - 3):
                if status_matrix[i][j] == 1 and status_matrix[i][j + 1] == 1 and status_matrix[i][j + 2] == 1 and status_matrix[i][j + 3] == 1 and status_matrix[i][j + 4] == 1:
                    self.result = 1
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for j in range(SIZE - 3, SIZE + 1):
            for i in range(1, SIZE - 3):
                if status_matrix[i][j] == 1 and status_matrix[i + 1][j] == 1 and status_matrix[i + 2][j] == 1 and status_matrix[i + 3][j] == 1 and status_matrix[i + 4][j] == 1:            
                    self.result = 1
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for i in range(1, SIZE - 3):
            for j in range(5, SIZE + 1):
                if status_matrix[i][j] == 1 and status_matrix[i + 1][j - 1] == 1 and status_matrix[i + 2][j - 2] == 1 and status_matrix[i + 3][j - 3] == 1 and status_matrix[i + 4][j - 4] == 1:
                    self.result = 1
                    
                    if self.playing:
                        self.playing = False
                    self.running = False


        
        # balance breaker judge
        # long connection judge (because 7 or longer connection must have a stage of 6 connection, so we only need to judge 6 connection situation)
        for i in range(1, SIZE - 4):
            for j in range(1, SIZE - 4):
                if (status_matrix[i][j] == 1 and status_matrix[i + 1][j] == 1 and status_matrix[i + 2][j] == 1 and status_matrix[i + 3][j] == 1 and status_matrix[i + 4][j] == 1 and status_matrix[i + 5][j] == 1) or \
                    (status_matrix[i][j] == 1 and status_matrix[i][j + 1] == 1 and status_matrix[i][j + 2] == 1 and status_matrix[i][j + 3] == 1 and status_matrix[i][j + 4] == 1 and status_matrix[i][j + 5] == 1) or \
                    (status_matrix[i][j] == 1 and status_matrix[i + 1][j + 1] == 1 and status_matrix[i + 2][j + 2] == 1 and status_matrix[i + 3][j + 3] == 1 and status_matrix[i + 4][j + 4] == 1 and status_matrix[i + 5][j + 5] == 1):
                    self.result = 3
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for i in range(SIZE - 4, SIZE + 1):
            for j in range(1, SIZE - 4):
                if status_matrix[i][j] == 1 and status_matrix[i][j + 1] == 1 and status_matrix[i][j + 2] == 1 and status_matrix[i][j + 3] == 1 and status_matrix[i][j + 4] == 1 and status_matrix[i][j + 5] == 1:
                    self.result = 3
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for j in range(SIZE - 4, SIZE + 1):
            for i in range(1, SIZE - 4):
                if status_matrix[i][j] == 1 and status_matrix[i + 1][j] == 1 and status_matrix[i + 2][j] == 1 and status_matrix[i + 3][j] == 1 and status_matrix[i + 4][j] == 1 and status_matrix[i + 5][j] == 1:            
                    self.result = 3
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for i in range(1, SIZE - 4):
            for j in range(4, SIZE + 1):
                if status_matrix[i][j] == 1 and status_matrix[i + 1][j - 1] == 1 and status_matrix[i + 2][j - 2] == 1 and status_matrix[i + 3][j - 3] == 1 and status_matrix[i + 4][j - 4] == 1 and status_matrix[i + 5][j - 5] == 1:
                    self.result = 3
                    
                    if self.playing:
                        self.playing = False
                    self.running = False





                    
    def judge_computer(self):
        for i in range(1, SIZE - 3):
            for j in range(1, SIZE - 3):
                if (status_matrix[i][j] == 2 and status_matrix[i + 1][j] == 2 and status_matrix[i + 2][j] == 2 and status_matrix[i + 3][j] == 2 and status_matrix[i + 4][j] == 2) or \
                    (status_matrix[i][j] == 2 and status_matrix[i][j + 1] == 2 and status_matrix[i][j + 2] == 2 and status_matrix[i][j + 3] == 2 and status_matrix[i][j + 4] == 2) or \
                    (status_matrix[i][j] == 2 and status_matrix[i + 1][j + 1] == 2 and status_matrix[i + 2][j + 2] == 2 and status_matrix[i + 3][j + 3] == 2 and status_matrix[i + 4][j + 4] == 2):
                    self.result = 2
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for i in range(SIZE - 3, SIZE + 1):
            for j in range(1, SIZE - 3):
                if status_matrix[i][j] == 2 and status_matrix[i][j + 1] == 2 and status_matrix[i][j + 2] == 2 and status_matrix[i][j + 3] == 2 and status_matrix[i][j + 4] == 2:               
                    self.result = 2
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for j in range(SIZE - 3, SIZE + 1):
            for i in range(1, SIZE - 3):
                if status_matrix[i][j] == 2 and status_matrix[i + 1][j] == 2 and status_matrix[i + 2][j] == 2 and status_matrix[i + 3][j] == 2 and status_matrix[i + 4][j] == 2:
                    self.result = 2
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

        for i in range(1, SIZE - 3):
            for j in range(5, SIZE + 1):
                if status_matrix[i][j] == 2 and status_matrix[i + 1][j - 1] == 2 and status_matrix[i + 2][j - 2] == 2 and status_matrix[i + 3][j - 3] == 2 and status_matrix[i + 4][j - 4] == 2:
                    self.result = 2
                    
                    if self.playing:
                        self.playing = False
                    self.running = False

    '''
    def events(self):
        # catch all events here
        # Process input (events)
        for event in pygame.event.get():
            #check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                    # self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT:
                    self.player.move(dx = -1)
                if event.key == pygame.K_RIGHT:
                    self.player.move(dx = 1)
                if event.key == pygame.K_UP:
                    self.player.move(dy = -1)
                if event.key == pygame.K_DOWN:
                    self.player.move(dy = 1)
                if event.key == pygame.K_SPACE:
                    self.player.mov = 0
                    self.add_to_matrix()
                    # print(status_matrix)
                    # print()
                    self.judge_player()
                    x1, y1 = ai2.computer_strategy()
                    self.enemy = Enemy(self, x1, y1)
                    # self.enemy = Enemy(self, 2, 1)

                    self.add_to_matrix_enemy()
                    # for i in range(1,16):
                    #     for j in range(1,16):
                    #         print(status_matrix[j][i], end= ' ')
                    #     print()
                        
                    self.judge_computer()
                    self.player = Player(self, 1, 1, 1)

    '''

                     
     
    def events(self):
        # catch all events here
        # Process input (events)
        for event in pygame.event.get():
            #check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                    # self.quit()
            else:

                x1, y1 = ai1.computer_strategy()
                self.player = Player(self, x1, y1, 0)
                self.add_to_matrix()
                # print(status_matrix)
                # print()
                self.judge_player()

                x2, y2 = ai2.computer_strategy()
                self.enemy = Enemy(self, x2, y2)
                # self.enemy = Enemy(self, 2, 1)

                self.add_to_matrix_enemy()
                # for i in range(1,16):
                #     for j in range(1,16):
                #         print(status_matrix[j][i], end= ' ')
                #     print()
                        
                self.judge_computer()        

    def show_start_screen(self):
        self.draw_text("Press KEY_S to Start!", 19, WHITE, WIDTH / 2, HEIGHT / 3)
        self.draw_text("Press arrows to move", 15, WHITE, WIDTH / 2, HEIGHT / 1.5)
        self.draw_text("Press space to determine", 15, WHITE, WIDTH / 2, HEIGHT / 1.3)
        waiting = True
        while waiting:
            # self.clock.tick(FPS)
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         waiting = False
            #         self.running = False
            #     if event.type == pygame.KEYUP:
            #         waiting = False   
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        waiting = False

    def show_go_screen(self):
        # if not self.game_over:
        #     # this return means to end up with nothing of this function
        #     return
        
        if self.result == 2:
            self.draw_text("YOU LOSE!", 32, WHITE, WIDTH / 2, HEIGHT / 4)
        if self.result == 1:
            self.draw_text("YOU WIN!", 32, WHITE, WIDTH / 2, HEIGHT / 4)
        if self.result == 3:
            self.draw_text("RESTRICTED MOVE LOSE!", 17, WHITE, WIDTH / 2, HEIGHT / 4)
        pygame.display.flip()

        self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text , True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        # at the start of the game, used to keep the tips on the screen until player tapping a key
        waiting = True
        while waiting:
            # self.clock.tick(FPS)
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         waiting = False
            #         self.running = False
            #     if event.type == pygame.KEYUP:
            #         waiting = False
            self.draw_text("Please push esc to escape!", 15, WHITE, WIDTH / 2, HEIGHT / 1.5)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                    







