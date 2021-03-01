from tkinter import Frame, Label, CENTER
# from puzzle import GameGrid
import numpy as np
import gym
from enum import Enum
import logic
import constants as c

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class GameEnv(gym.Env):
    NB_ACTIONS = 4

    action_space = gym.spaces.Discrete(NB_ACTIONS)
    observation_space = gym.spaces.Box(low=0., high = (2 ** 16), shape = (c.GRID_LEN, c.GRID_LEN))



    _ACTION_MAP = {Action.UP : logic.up,
                 Action.DOWN : logic.down,
                 Action.LEFT : logic.left,
                 Action.RIGHT : logic.right}

    _matrix = None

    _inactive_penalty = 0
    _inactive_penalty_function = None
    

    def __init__(self, inactive_penalty=2):
        """ 
        Args:
            inactive_penalty : 0 -> no inactive penalty
            1 -> constant (-1) inactive penalty
            2 -> -1, then -2, then -3
        """
        self._inactive_penalty_function = {
            0 : (lambda _ : 0),
            1 : (lambda _ : -1),
            2 : self._linear_penalty
        }[inactive_penalty]

    def reset(self):
        self._matrix = logic.new_game(c.GRID_LEN)
        return self._matrix

    def step(self, action: Action):
        new_matrix, action_done, score = self._ACTION_MAP[action](self._matrix)
        new_matrix = logic.add_two(new_matrix)

        prev_matrix = self._matrix
        self._matrix = new_matrix

        state = logic.game_state(new_matrix)
        done = state == logic.State.LOSE

        info = {"observation_prev": prev_matrix}

        if not action_done:
            return  new_matrix, score + self._inactive_penalty_function(), done, info
        self._reset_inactive_penalty()
        
        return new_matrix, score, done, info


    def _reset_inactive_penalty(self):
        self.inactive_penalty = 0

    def _linear_penalty(self):
        self._inactive_penalty -= 1
        return self._inactive_penalty

            






# class GameEnv(GameGrid, gym.Env):
#     def __init__(self):
#         Frame.__init__(self)
#
#         self.grid()
#         self.master.title('2048')
#         self.master.bind("<Key>", self.key_down)
#         self._commands = {Action.UP : logic.up,
#                          Action.DOWN : logic.down,
#                          Action.LEFT : logic.left,
#                          Action.RIGHT : logic.right}
#
#         self.grid_cells = []
#         self.init_grid()
#         self.matrix = logic.new_game(c.GRID_LEN)
#         self.history_matrixs = []
#         self.update_grid_cells()
#
#         # self.mainloop() # NO MAINLOOP
#         self.update()
#
#
#     def key_down(self, event): # remove bindings from GameGrid
#         pass
#
#     def score(self):
#         return 0
#
#     def reset(self):
#         self.matrix = logic.new_game(c.GRID_LEN)
#         self.update()
#
#     def step(self, action):
#         self.matrix, done = self.commands[action](self.matrix)
#         self.update()
#         return done




# env = GameEnv

