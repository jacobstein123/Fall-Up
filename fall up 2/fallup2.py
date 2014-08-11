import pygame
import sys
import random
from pygame.locals import *
import time

try:
    import android
except ImportError:
    android = None

def main():

    class Player:
        def __init__(self):
            self.x = 47
            self.y = 45
            self.image = pygame.image.load('player.png')
            #self.score = 0
        def draw(self):
            screen.blit(self.image,(self.x,self.y))
        def move(self,move):
            if 0 <= self.x + move <= 84:
                player.x += move
            #elif self.

    class Block:
        def __init__(self):
            global current_block
            #self.x = random.choice(range(0,196,4))
            self.y = 0
            current_block = random.choice(block_images)
            self.image = pygame.image.load(current_block)
            self.already_passed_line = False
        def draw(self):
            screen.blit(self.image, (0,self.y))
        def move(self):
            self.y += block_speed
        def off_screen(self):
            return self.y > 64
        def passed_line(self):
            if (not self.already_passed_line) and (self.y >= 32):
                self.already_passed_line = True
                return True

    def player_top_collided():
        for x in range(player.x,player.x+12):
            if screen.get_at((x,player.y)) != (1, 1, 1, 255):
                #print screen.get_at((x,player.y))
                print 'top'
                return True
        '''for y in range(player.y,player.y+8):
            if screen.get_at((player.x,y)) != (1, 1, 1, 255):
                return True
            elif screen.get_at((player.x+11, y)) != (1, 1, 1, 255):
                return True'''
        return False
    def player_left_collided():
        for y in range(player.y+1,player.y+8):
            if screen.get_at((player.x,y)) != (1, 1, 1, 255):
                print 'left'
                return True
        return False
    def player_right_collided():
        for y in range(player.y+1,player.y+8):
            if screen.get_at((player.x+11, y)) != (1, 1, 1, 255):
                print 'right'
                return True
        return False


    pygame.init()
    display = pygame.display.set_mode((384,256))
    screen = pygame.Surface((96,64))
    fps_clock = pygame.time.Clock()

    if android:
        android.init()

    PIXEL_SIZE = 1
    #FPS = 30

    font = pygame.font.Font('LCD_Solid.ttf',24)
    big_font = pygame.font.Font('LCD_Solid.ttf',32)

    map_image = pygame.image.load('map3.png')
    map_prime = pygame.image.load('map2.png')


    while 1:
        move = 0
        #block_images = ['block%i.png'%i for i in range(2,9) if 'block%i.png'%i ] #create a list of all the block image names
        player = Player()
        #blocks = [Block()]
        game_over = False
        restart = False
        player_speed = 2
        block_speed = 1
        k = -3159
        fps = 30
        start_time = time.time()
        level_up = False
        score = 0


        while not restart:
            #block_images = ['block%i.png'%i for i in range(2,9) if 'block%i.png'%i != current_block] #list of available blocks so there's no repetition
            screen.fill(Color(239,254,221)) #light green
            player.draw()
            '''for block in blocks:
                block.draw()'''
            screen.blit(map_image,(0,k))
            if not game_over: k+= 1

            display.blit(font.render('LEVEL: %i'%(block_speed),False,Color('black')),(260,0))
            display.blit(font.render('TIME: %s'%str(score)[:str(score).find('.')+2],False,Color('black')),(0,0))
            if game_over:
                display.blit(big_font.render('GAME OVER!',False,Color('black')),(100,120))

            for event in pygame.event.get(): #event loop
                if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        move = player_speed #player moves 4*player_speed px right
                    elif event.key == K_LEFT:
                        move = -player_speed
                    elif event.key == K_r:
                        restart = True
                if event.type == KEYUP:
                    if event.key == K_RIGHT and move > 0:
                        move = 0
                    if event.key == K_LEFT and move < 0:
                        move = 0
                if event.type == MOUSEBUTTONDOWN:
                    if game_over:
                        restart = True
                    mouse_x, mouse_y = event.pos
                    if mouse_x < 192:
                        move = -player_speed
                    else:
                        move = player_speed
                if event.type == MOUSEBUTTONUP:
                    if mouse_x < 192 and move < 0:
                        move = 0
                    if mouse_x >= 192 and move > 0:
                        move = 0

            if player.y > 55:
                game_over = True

            if not game_over and player_top_collided():
                #pygame.display.update()
                #game_over = True
                player.y += 1



            if move and not game_over:
                player.move(move)

            '''if blocks[0].off_screen():
                blocks = blocks[1:]

            if blocks[0].passed_line():
                blocks.append(Block())'''

            '''if not game_over:
                for block in blocks:
                    block.move()
                player.score += 1'''

            '''if not game_over and int(time.time() - start_time) and int(time.time() - start_time) % 10 == 0 and not level_up:
                block_speed += 1
                fps += 1
                level_up = True'''
            if not game_over and score > 30 and not level_up:
                fps = 40
            if level_up and not int(time.time() - start_time) % 10 == 0:
                level_up = False
            if not game_over:
                score = round(time.time() - start_time,2)
            #print int(time.time() - start_time)

            pygame.display.update()
            fps_clock.tick(fps)
            display.blit(pygame.transform.scale(screen,(384,256)),(0,0))

if __name__ == '__main__':
    main()

