# Flappy AI Project

This project aims to develop an AI agent capable of autonomously playing the game Flappy Bird using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The agent learns optimal strategies for navigating the game environment and achieving high scores through reinforcement learning.

## Project Structure

- `flappy_bird_manual.py`: A file in the root directory that contains the standard Flappy Bird game, playable by a human using the spacebar key.
- `neat_game.py`: A file in the root directory that implements the game and the NEAT algorithm. Running this file starts the training of the Neural Network.
- `config_feedforward.txt`: A file in the root directory that houses all configurations for the NEAT algorithm, such as population size and fitness threshold.
- `visualize.py`: A file in the root directory that shows a line graph after training the NEAT for specific generations, displaying the best fitness, average, and standard deviation.

## How to Execute

1. **Manual Gameplay**:
   - To play the game manually, use the following command:
     ```
     python flappy_bird_manual.py
     ```
   - Use the spacebar key to control the bird's flap and navigate through the pipes.

2. **Training the NEAT Model**:
   - To train the NEAT model, use the following command:
     ```
     python neat_game.py
     ```
   - This will start the training process, where the AI agent learns to play Flappy Bird autonomously.

3. **Visualization**:
   - After training, you can visualize the results after TOTAL_GEN have completed
     A line graph will show the best fitness, average fitness, and standard deviation over generations.

## Requirements
- Python 3.x
- NEAT Python library
- Pygame library

## Future Scope
- Implementing more advanced neural network architectures, such as CNNs or RNNs, could enhance the AI's ability to learn and improve its gameplay.
- Developing more sophisticated fitness functions that consider factors like obstacle spacing, speed, and patterns could lead to more strategic gameplay.
- Expanding the game to include multiplayer or competitive modes, where AIs compete against each other or against human players, could add an exciting dimension to the game.
- Applying the skills and strategies learned by the AI in playing Flappy Bird to real-world problems, such as autonomous navigation or optimization tasks.

## Contributors
- [Shankjbs571](https://github.com/Shankjbs571)
- [iusekarma](https://github.com/iusekarma)

## License
This project is licensed under the [MIT License](LICENSE).
