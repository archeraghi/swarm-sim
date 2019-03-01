"""
The sim module provides the datas that are needed for simulating.

"""


import importlib, os

import random


class Sim:
    def __init__(self, seed=1, max_round=10, solution="None"):
        """

        :param seed: seed number for new random numbers
        :param max_round: the max round number for terminating the simulator
        :param solution: The name of the solution that is going to be used
        """
        random.seed(seed)
        self.__max_round = max_round
        self.__round_counter = 1
        self.__seed=seed
        self.__solution = solution
        self.solution_mod = importlib.import_module('solution.' + solution)
        self.__end = False
        #csv attributes


    def get_max_round(self):
        """
        Return the initialized endding round number

        :return: The maximum round number
        """
        return self.__max_round

    def get_actual_round(self):
        """
        The actual round number

        :return: actual round number
        """
        return self.__round_counter

    def set_end(self):
        """
        Allows to terminate before the max round is reached
        """
        self.__end=True

    def get_end(self):
        """
            Returns the end parameter values either True or False
        """
        return self.__end


    def inc_round_cnter(self):
        """
        Increases the the round counter by

        :return:
        """

        self.__round_counter +=  1

    def get_solution(self):
        """
        actual solution name

        :return: actual solution name
        """
        return self.__solution


    def run(self, world):
        """
        :param world: The world object
        :param solution: The name of the solution file
        :return:
        """

        while self.get_actual_round() <= self.get_max_round() and self.__end == False:
            self.solution_mod.solution(self, world)
            world.csv_round_writer.next_line(self.get_actual_round())
            self.__round_counter = self.__round_counter + 1

        #creating gnu plots
        return

