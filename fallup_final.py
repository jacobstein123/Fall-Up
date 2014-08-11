import pygame
import sys
import random
import time
from pygame.locals import *

try:
    import android
except ImportError:
    android = None

def main():

    class Player:
        def __init__(self):
            self.x = 188
            self.y = 180
            self.image = pygame.image.load('player.png')
            self.score = 0
        def draw(self):
            screen.blit(self.image,(self.x,self.y))
        def move(self,move):
            if 0 <= self.x + move <= 336:
                self.x += move
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
            return self.y > 256
        def passed_line(self):
            if (not self.already_passed_line) and (self.y >= 128):
                self.already_passed_line = True
                return True

    def player_collided():
        for x in range(player.x,player.x+48):
            if sum(screen.get_at((x,180))[:-1]) > 10:
                return True
        for y in range(180,212):
            if sum(screen.get_at((player.x,y))[:-1]) >10:
                return True
            elif sum(screen.get_at((player.x+47, y))[:-1]) >10:
                return True
        return False

    def intro():
        while 1:
            screen.fill(Color(239,254,221))
            screen.blit(huge_font.render('FALL UP!',False,pygame.Color('black')),(88,60))
            screen.blit(big_font.render('STAGE 1 | STAGE 2',False,pygame.Color('black')),(24,160))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.pos[0] < 192:
                        return 1
                    else:
                        return 2
            pygame.display.update()

    pygame.init()
    screen = pygame.display.set_mode((384,256))
    fps_clock = pygame.time.Clock()

    if android:
        android.init()
        android.map_key(android.KEYCODE_MENU, pygame.K_p)

    PIXEL_SIZE = 4

    font = pygame.font.Font('LCD_Solid.ttf',24)
    big_font = pygame.font.Font('LCD_Solid.ttf',32)
    huge_font = pygame.font.Font('LCD_Solid.ttf',44)


    map_image = pygame.image.load('map4.png')
    map_prime = map_image

    stage = intro()
    mouse_x = mouse_y = 0
    while 1:
        move = 0
        block_images = ['block%i.png'%i for i in range(2,9) if 'block%i.png'%i ] #create a list of all the block image names
        player = Player()
        blocks = [Block()]
        game_over = False
        restart = False
        level_up = False
        pause = False
        player_speed = 2
        block_speed = 2
        k = -12630
        start_time = time.time()
        score = 0
        fps = 30
        game_over_msg = 'GAME OVER!'
        pause_time = 0

        while not restart:
            block_images = ['block%i.png'%i for i in range(2,9) if 'block%i.png'%i != current_block] #list of available blocks so there's no repetition
            screen.fill(Color(239,254,221)) #light green
            player.draw()

            if stage == 1:
                for block in blocks:
                    block.draw()
            else:
                screen.blit(map_image,(0,k))
                if not game_over and not pause: k+= block_speed

            screen.blit(font.render('LEVEL: %i'%(int(score)/10),False,Color('black')),(244,0))
            screen.blit(font.render('TIME: %s'%str(score)[:str(score).find('.')+2],False,Color('black')),(0,0))
            if game_over:
                screen.blit(big_font.render(game_over_msg,False,Color('black')),(100,120))

            for event in pygame.event.get(): #event loop
                if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        move = PIXEL_SIZE * player_speed #player moves 4*player_speed px right
                    elif event.key == K_LEFT:
                        move = -PIXEL_SIZE * player_speed
                    elif event.key == K_r:
                        restart = True
                    elif event.key == K_p:
                        pause = not pause
                        if pause:
                            pause_start = time.time()
                        else:
                            pause_time = round(time.time() - pause_start,2)
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
                        move = -PIXEL_SIZE * player_speed
                    else:
                        move = PIXEL_SIZE * player_speed
                if event.type == MOUSEBUTTONUP:
                    if mouse_x < 192 and move < 0:
                        move = 0
                    if mouse_x >= 192 and move > 0:
                        move = 0

            if not pause:
                if player_collided():
                    pygame.display.update()
                    game_over = True

                if move and not game_over:
                    player.move(move)

                if blocks[0].off_screen():
                    blocks = blocks[1:]

                if blocks[0].passed_line():
                    blocks.append(Block())

                if stage == 1 and not game_over:
                    for block in blocks:
                        block.move()
                if stage == 2 and not game_over:
                    if score > 125:
                        game_over = True
                        game_over_msg = 'YOU WON!'

                if not game_over and int(score) and int(score) % 10==0 and not level_up:
                    fps += 4
                    level_up = True
                if level_up and not int(time.time() - start_time - pause_time) % 10 == 0:
                    level_up = False
                if not game_over:
                    score = round(time.time() - start_time - pause_time,2)
            else:
                screen.blit(huge_font.render('PAUSED',False,Color('black')),(112,120))

            pygame.display.update()
            fps_clock.tick(fps)

if __name__ == '__main__':
    main()

