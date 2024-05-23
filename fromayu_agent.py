import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .fromayu_neat_game import BirdGame, Bird



def eval_genomes(genomes, config):
    bird_game = BirdGame()
    nets = []
    birds = []
    birds_score = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(game=bird_game))
        birds_score.append(0)
        ge.append(genome)

    while len(birds) > 0:
        bird_game.clock.tick(SPEED)
        bird_game._update_screen()
        bird_game.play_step()
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            pipe_y = bird_game.h//2
            pipe_x = bird_game.w
            if bird_game.pipes:
                pipe_y = bird_game.pipes[0][1] - bird.y
                pipe_x = bird_game.pipes[0][0] - BIRD_X
            output = nets[x].activate((bird.y, pipe_y, pipe_x))
            action = 1 if output[0] > 0.5 else 0
            game_over, score, scored = bird.play_step(action)
            
            if scored:
                ge[x].fitness += 1

            if game_over:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        draw_frame(game=bird_game,birds=birds)
        

def draw_frame(game:BirdGame,birds:[Bird]):
    game._update_screen()
    for bird in birds:
        bird._draw_bird()
    pygame.display.flip()

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
