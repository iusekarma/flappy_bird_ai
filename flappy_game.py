import pygame
import random
import neat
import os

pygame.init()

SPEED = 30
JUMP_ACCELERATION = 14
PIPE_SPEED = 7
BIRD_X = 100

BIRD_SIZE = 40
PIPE_GAP_Y = 160
PIPE_GAP_X = 60


class Bird:
    
    def __init__(self, game):
        self.y = 240
        self.game_over = False
        self.score = 0
        self.y_velocity = 0
        self.y = 240
        self.game = game
        self.bird_index = 1
        self.flap_count = 0
        
    def play_step(self,action):
        scored = False
        game_over = False
        self.y_velocity = min(self.y_velocity + self.game.gravity, 10)
        self.y += self.y_velocity
        
        if self.game.pipes:
            if self.game.pipes[0][0] < BIRD_X - (BIRD_SIZE//2):
                self.score += 1
                scored = True
        if action == 1:
            self.y_velocity = -JUMP_ACCELERATION
            self.flap_count = 15
           
        if self._is_collision() or self._is_out_of_bounds():
            game_over = True
        
        return game_over, self.score, scored
        
    def _is_collision(self):        
        for pipe in self.game.pipes:
            if (((BIRD_X - (BIRD_SIZE // 2)) > (pipe[0] - (PIPE_GAP_X // 2))) and ((BIRD_X - (BIRD_SIZE // 2)) < (pipe[0] + (PIPE_GAP_X // 2)))) or \
                (((BIRD_X + (BIRD_SIZE // 2)) > (pipe[0] - (PIPE_GAP_X // 2))) and ((BIRD_X + (BIRD_SIZE // 2)) < (pipe[0] + (PIPE_GAP_X // 2)))):
                    
                if (((self.y - (BIRD_SIZE // 2)) > (pipe[1] - (PIPE_GAP_Y // 2))) and ((self.y - (BIRD_SIZE // 2)) < (pipe[1] + (PIPE_GAP_Y // 2)))) and \
                    (((self.y + (BIRD_SIZE // 2)) > (pipe[1] - (PIPE_GAP_Y // 2))) and ((self.y + (BIRD_SIZE // 2)) < (pipe[1] + (PIPE_GAP_Y // 2)))):
                    return False
                else:
                    return True
            
    def _is_out_of_bounds(self):
        if self.y < 0 or self.y > self.game.h:
            return True
        return False
    
    def _draw_bird(self):
        if self.flap_count > 0:
            self.flap_count -= 1
            if self.flap_count == 0:
                self.bird_index = (self.game.bird_index + 1) % len(self.game.bird_images)

        bird_image = self.game.bird_images[self.bird_index]
        self.game.display.blit(bird_image, (BIRD_X - (BIRD_SIZE // 2), self.y - (BIRD_SIZE // 2)))

class BirdGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.gravity = 1.3
        
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('BirdGame')
        
        self.clock = pygame.time.Clock()
        self.pipes = []
        self.reset()

        self.bird_images = [
            pygame.image.load('assets/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('assets/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
        ]
        self.bird_index = 1
        self.flap_count = 0

        self.background_image = pygame.image.load('assets/background-day.png').convert()
        self.background_rect = self.background_image.get_rect()
        self.background_x = 0

        self.pipe_top_image = pygame.image.load('assets/pipe-top.png').convert_alpha()
        self.pipe_bottom_image = pygame.image.load('assets/pipe-bottom.png').convert_alpha()
        
        
        self._spawn_pipe()
     
    def reset(self):
        self.score = 0
        self.y_velocity = 0
        self.y = 240
        self.frame_iteration = 0
        self.pipes = []

    def play_step(self):
        self.frame_iteration += 1

        if self.frame_iteration % 60 == 0:
            self.frame_iteration = 0
            self._spawn_pipe()

        for index in range(len(self.pipes)):
            self.pipes[index][0] -= PIPE_SPEED

    def _update_screen(self):
        self.display.blit(self.background_image, (self.background_x, 0))
        self.display.blit(self.background_image, (self.background_x + self.w, 0))

        self.background_x -= PIPE_SPEED*0.75
        if self.background_x <= -self.w:
            self.background_x = 0

        for pipe in self.pipes:
            self._draw_pipe(pipe)
        
        if self.pipes:
            if self.pipes[0][0] < 0:
                self.pipes.pop(0)

    def _spawn_pipe(self):
        self.pipes.append([self.w, random.randint(60, self.h - 60)])

    # def _draw_pipe(self, pipe):
    #     pygame.draw.rect(self.display, (0, 255, 0), (pipe[0] - (PIPE_GAP_X // 2), pipe[1] - (PIPE_GAP_Y // 2), PIPE_GAP_X, PIPE_GAP_Y))

    def _draw_pipe(self, pipe):
        pipe_x = pipe[0]
        pipe_y = pipe[1]
        
        top_pipe_rect = self.pipe_top_image.get_rect(midbottom=(pipe_x, pipe_y - PIPE_GAP_Y // 2))
        bottom_pipe_rect = self.pipe_bottom_image.get_rect(midtop=(pipe_x, pipe_y + PIPE_GAP_Y // 2))
        
        self.display.blit(self.pipe_top_image, top_pipe_rect)
        self.display.blit(self.pipe_bottom_image, bottom_pipe_rect)

# if __name__ == '__main__':
#     game = BirdGame()
    
#     while True:
#         game_over, score = game.play_step()
#         if game_over:
#             print(score)
#             break
    
#     # print(game.frame_iteration)
#     pygame.quit()

if __name__ == '__main__':
    bird_game = BirdGame()
    bird = Bird(game = bird_game)

    running = True
    while running:
        bird_game.clock.tick(SPEED)
        bird_game._update_screen()
        bird_game.play_step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.play_step(action=1)

        game_over, score, scored = bird.play_step(action=0)
        bird._draw_bird()
        pygame.display.flip()

        if game_over:
            print("Score: ", score)
            break

    pygame.quit()