import pygame

pygame.init()

SPEED = 20

class BirdGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.gravity = 9.8
        
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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                
        self._update_screen()
        self.clock.tick(SPEED)
            
        return game_over, self.score
    
    def _update_screen(self):
        pass
        
if __name__ == '__main__':
    game = BirdGame()
    
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break
    
    print(score)
    pygame.quit()
    