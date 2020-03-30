
import numpy as np
import random
import csv


class ColorChain:
    def __init__(self, w="chain1"):
        self.chain_string = w
        self.states, self.transition_matrix = self.loadMarkovProperties()

    def getNextState(self, current):
        evt = random.randint(1, 100)
        probabilities = self.transition_matrix[current, :]*100
        next_state = 0
        total = 0
        for p in range(0, len(probabilities)):
            total += probabilities[p]
            if evt <= total:
                next_state = p
                break
        return next_state

    def getNextState(self, current, transitionmatrix):
        evt = random.randint(1, 100)
        probabilities = transitionmatrix[current, :]*100
        next_state = 0
        total = 0
        for p in range(0, len(probabilities)):
            total += probabilities[p]
            if evt <= total:
                next_state = p
                break
        return next_state

    def getCurrState(self, pixel_value):
        curr_state = 0
        for p in range(self.states.shape[0]):
            if sum(self.states[p, :] == pixel_value) == 3:
                curr_state = p
        return curr_state

    def loadMarkovProperties(self):
        # read in state space from csv
        reader = csv.reader(open(self.chain_string + "/states.csv", "r"), delimiter=',')
        x = list(reader)
        states = np.array(x).astype("int")

        # read in transition matrix from csv
        reader = csv.reader(open(self.chain_string + "/transitionMatrix.csv", "r"), delimiter=',')
        x = list(reader)
        transition_matrix = np.array(x).astype("float")
        return states, transition_matrix

