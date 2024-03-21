import pygame
import random

pygame.init()

SPEED = 40
JUMP_ACCELERATION = 15
PIPE_SPEED = 7
BIRD_X = 100

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
        
    def reset(self):
        self.score = 0
        self.y_velocity = 0
        self.y = 240
        self.frame_iteration = 0
        
    def play_step(self):
        game_over = False
        self.frame_iteration += 1
        
        # If frame_number = 60, reset count and spawn a pipe.
        if self.frame_iteration % 60 == 0:
            self.frame_iteration = 0
            self._spawn_pipe()
        
        # move bird
        self.y_velocity = min(self.y_velocity+self.gravity,10)
        self.y += self.y_velocity
        
        # move pipe
        for index in range(len(self.pipes)):
            self.pipes[index][0] -= PIPE_SPEED
        
        # if pipe0 is out of screen pop it from list
        if self.pipes:
            if self.pipes[0][0] < 0:
                self.score += 1
                self.pipes.pop(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.y_velocity = -JUMP_ACCELERATION
                elif event.key == pygame.K_a:
                    self._spawn_pipe()
                    
        self.y = max(0,self.y)
        self.y = min(self.y,self.h)
        
        if self._is_collision() :
            game_over = True
        
        self._update_screen()
        self.clock.tick(SPEED)

        return game_over, self.score
    
    def _update_screen(self):
        self.display.fill((0,0,0))
        
        self._draw_bird()
        
        for pipe in self.pipes:
            self._draw_pipe(pipe)
            
        pygame.display.flip()
    
    def _is_collision(self):
        for pipe in self.pipes:
            if (((BIRD_X - 20) > (pipe[0]-30)) and ((BIRD_X - 20) < (pipe[0]+30))) or (((BIRD_X + 20) > (pipe[0]-30)) and ((BIRD_X + 20) < (pipe[0]+30))):
                if (((self.y - 20) > (pipe[1]-60)) and ((self.y - 20) < (pipe[1]+60))) and (((self.y + 20) > (pipe[1]-60)) and ((self.y + 20) < (pipe[1]+60))):
                    return False
                else:
                    return True

    # def _is_in_gap(self):
    #     for pipe in self.pipes:
    #         if (((BIRD_X - 20) > (pipe[0]-40)) and ((BIRD_X - 20) < (pipe[0]+40))) and (((BIRD_X + 20) > (pipe[0]-40)) and ((BIRD_X + 20) < (pipe[0]+40))):
    #             if (((self.y - 20) > (pipe[1]-60)) and ((self.y - 20) < (pipe[1]+60))) and (((self.y + 20) > (pipe[1]-60)) and ((self.y + 20) < (pipe[1]+60))):
    #                 return True
    #             else:
    #                 return False
    
    def _spawn_pipe(self):
        self.pipes.append([self.w,random.randint(60,self.h-60)])
        
    def _draw_bird(self):
        pygame.draw.rect(self.display,(255,255,255),(BIRD_X-20,self.y-20,40,40))
        
    def _draw_pipe(self,pipe):
        pygame.draw.rect(self.display,(0,255,0),(pipe[0]-30,pipe[1]-60,60,120))
        
if __name__ == '__main__':
    game = BirdGame()
    
    while True:
        game_over, score = game.play_step()
        if game_over:
            print(score)
            break
    
    # print(game.frame_iteration)
    pygame.quit()
    