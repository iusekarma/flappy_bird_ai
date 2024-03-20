import pygame

pygame.init()

SPEED = 60
JUMP_ACCELERATION = 20

class BirdGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.gravity = 2
        
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('BirdGame')
        
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.score = 0
        self.y_velocity = 0
        self.y = 240
        self.frame_iteration = 0
        
    def play_step(self):
        game_over = False
        self.score += 1
        
        self.y_velocity = min(self.y_velocity+self.gravity,10)
        self.y += self.y_velocity
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.y_velocity = -JUMP_ACCELERATION
                    
        self.y = max(0,self.y)
        self.y = min(self.y,self.h)
                
        self._update_screen()
        self.clock.tick(SPEED)
            
        return game_over, self.score
    
    def _update_screen(self):
        self.display.fill((0,0,0))
        
        pygame.draw.circle(self.display,(255,255,255),(100,self.y),20)
        
        pygame.display.flip()
        
if __name__ == '__main__':
    game = BirdGame()
    
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break
    
    print(score)
    pygame.quit()
    