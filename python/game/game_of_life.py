import numpy as np
from scipy.signal import convolve2d
from game_of_life_globals import *

# Kernel to calculate next step based on a 2D convolution.
# TODO : Refactor as a static function instead of a global variable
kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

class game_of_life:
    # Game logic for Conway's Game of Life.
    
    # def evolve_cell(alive, neighbours):
    #     return neighbours == 3 or (alive and neighbours == 2)
    
    @staticmethod
    def count_neighbours(life):
        # A shorthand for finding the number of neighbours for each cell.
        neighs = convolve2d(life, kernel, boundary='wrap', mode='same')
        return neighs
    
    @staticmethod
    def step(life):
        life = np.array(life).astype(int)
        neighs = game_of_life.count_neighbours(life)
        
        first = np.equal(neighs,3)
        second = np.bitwise_and(life, np.equal(neighs,2))

        return (np.bitwise_or(first, second)).tolist()
    
    @staticmethod
    def new_life(size_x = DEFAULT_SIZE_X, size_y = DEFAULT_SIZE_Y, probability=INITIAL_PROBABILITY):
        return (np.random.random(size=(size_x, size_y),) < probability).astype(int).tolist()

