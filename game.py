import pygame
import random

pygame.init()

SPEED = 30
JUMP_ACCELERATION = 14
PIPE_SPEED = 7
BIRD_X = 100

BIRD_SIZE = 40
PIPE_GAP_Y = 160
PIPE_GAP_X = 60

class BirdGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.gravity = 1.3
        
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('BirdGame')
        # self.bird_image = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
        
        self.clock = pygame.time.Clock()
        self.pipes = []
        self.reset()

        # Load bird images
        self.bird_images = [
            pygame.image.load('assets/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('assets/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
        ]
        self.bird_index = 1  # Start with the midflap image
        self.flap_count = 0  # Counter to control the flapping speed

        # Load background image
        self.background_image = pygame.image.load('assets/background-day.png').convert()
        self.background_rect = self.background_image.get_rect()
        self.background_x = 0

        # Load pipe images
        # self.pipe_top_image = pygame.image.load('pipe_up.png').convert_alpha()
        # self.pipe_bottom_image = pygame.image.load('pipe_bottom.png').convert_alpha()
        
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
                    self.flap_count = 15
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
        # Draw background
        self.display.blit(self.background_image, (self.background_x, 0))
        self.display.blit(self.background_image, (self.background_x + self.w, 0))

        # Move background
        self.background_x -= PIPE_SPEED
        if self.background_x <= -self.w:
            self.background_x = 0


        # self.display.fill((0,0,0))
        
        self._draw_bird()
        
        for pipe in self.pipes:
            self._draw_pipe(pipe)
            
        pygame.display.flip()
    
    def _is_collision(self):
        for pipe in self.pipes:
            if (((BIRD_X - (BIRD_SIZE//2)) > (pipe[0]-(PIPE_GAP_X//2))) and ((BIRD_X - (BIRD_SIZE//2)) < (pipe[0]+(PIPE_GAP_X//2)))) or\
                (((BIRD_X + (BIRD_SIZE//2)) > (pipe[0]-(PIPE_GAP_X//2))) and ((BIRD_X + (BIRD_SIZE//2)) < (pipe[0]+(PIPE_GAP_X//2)))):
                    
                if (((self.y - (BIRD_SIZE//2)) > (pipe[1]-(PIPE_GAP_Y//2))) and ((self.y - (BIRD_SIZE//2)) < (pipe[1]+(PIPE_GAP_Y//2)))) and\
                    (((self.y + (BIRD_SIZE//2)) > (pipe[1]-(PIPE_GAP_Y//2))) and ((self.y + (BIRD_SIZE//2)) < (pipe[1]+(PIPE_GAP_Y//2)))):
                    return False
                else:
                    return True
    
    def _spawn_pipe(self):
        self.pipes.append([self.w,random.randint(60,self.h-60)])
        
    def _draw_bird(self):
        # Flap effect logic
        if self.flap_count > 0:
            self.flap_count -= 1
            if self.flap_count == 0:
                self.bird_index = (self.bird_index + 1) % len(self.bird_images)

        bird_image = self.bird_images[self.bird_index]
        self.display.blit(bird_image, (BIRD_X - (BIRD_SIZE//2), self.y - (BIRD_SIZE//2)))
        # pygame.draw.rect(self.display,(255,255,255),(BIRD_X-20,self.y-20,40,40))
        
    def _draw_pipe(self,pipe):
        pygame.draw.rect(self.display,(0,255,0),(pipe[0]-(PIPE_GAP_X//2),pipe[1]-(PIPE_GAP_Y//2),PIPE_GAP_X,PIPE_GAP_Y))
        
if __name__ == '__main__':
    game = BirdGame()
    
    while True:
        game_over, score = game.play_step()
        if game_over:
            print(score)
            break
    
    # print(game.frame_iteration)
    pygame.quit()
    