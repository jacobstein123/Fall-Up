import pygame
import sys
import random
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
            if screen.get_at((x,180)) not in ((52, 52, 52, 255),(49, 52, 49, 255)):
                return True
        for y in range(180,212):
            if screen.get_at((player.x,y)) not in ((52, 52, 52, 255),(49, 52, 49, 255)):
                return True
            elif screen.get_at((player.x+47, y)) not in ((52, 52, 52, 255),(49, 52, 49, 255)):
                return True
        return False


    pygame.init()
    screen = pygame.display.set_mode((384,256))
    fps_clock = pygame.time.Clock()

    if android:
        android.init()

    PIXEL_SIZE = 4
    FPS = 30

    font = pygame.font.Font('LCD_Solid.ttf',24)
    big_font = pygame.font.Font('LCD_Solid.ttf',32)


    map_image = pygame.image.load('map3.png')
    while 1:
        move = 0
        block_images = ['block%i.png'%i for i in range(2,9) if 'block%i.png'%i ] #create a list of all the block image names
        player = Player()
        blocks = [Block()]
        game_over = False
        restart = False
        player_speed = 2
        block_speed = 3
        k = 4800

        while not restart:
            block_images = ['block%i.png'%i for i in range(2,9) if 'block%i.png'%i != current_block] #list of available blocks so there's no repetition
            screen.fill(Color(239,254,221)) #light green
            player.draw()
            #for block in blocks:
                #block.draw()
            screen.blit(map_image,(0,k))
            if not game_over: k+= 1

            screen.blit(font.render('LEVEL: %i'%(block_speed-2),False,Color('black')),(260,0))
            screen.blit(font.render('SCORE: %i'%player.score,False,Color('black')),(0,0))
            if game_over:
                screen.blit(big_font.render('GAME OVER!',False,Color('black')),(100,120))

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

            if player_collided():
                pygame.display.update()
                game_over = True

            if move and not game_over:
                player.move(move)

            if blocks[0].off_screen():
                blocks = blocks[1:]

            if blocks[0].passed_line():
                blocks.append(Block())

            if not game_over:
                for block in blocks:
                    block.move()
                player.score += 1

            if player.score % 500 == 0 and block_speed < 7:
                block_speed += 1

            pygame.display.update()
            fps_clock.tick(FPS)

if __name__ == '__main__':
    main()

