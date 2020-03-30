import cv2
import numpy as np
import random
from markovColorChain import ColorChain


class MarkovImage:
    def __init__(self, color_chain=ColorChain('chain1'),
                 overlaybool=0,
                 psize=[400, 400],
                 grpsize=5,
                 tmax=10,
                 pbordersize=[20, 20]):
        # image properties
        self.WITH_OVERLAY = overlaybool
        self.x_offset, self.y_offset = pbordersize[0], pbordersize[1]
        self.pixel_group_size = grpsize
        self.OVERLAY_COLOR = (255, 255, 255, 255)
        self.markov_color_chain = color_chain
        self.epicenters = []
        self.tmax = tmax

        if self.WITH_OVERLAY == 1:
            # make outline image
            self.edges_image = cv2.imread('logo.png', -1)
            self.pixel_height = self.edges_image.shape[0] + 2 * self.y_offset
            self.pixel_width = self.edges_image.shape[1] + 2 * self.x_offset
        else:
            self.pixel_height, self.pixel_width = psize[0], psize[1]

        self.main_pixel_map = np.zeros((self.pixel_height, self.pixel_width, 3), np.uint8)  # generated image space
        self.y_range = range(self.y_offset-1, self.pixel_height - self.y_offset, self.pixel_group_size)
        self.x_range = range(self.x_offset-1, self.pixel_width - self.x_offset, self.pixel_group_size)
        self.state_grid_map = np.zeros((len(self.y_range), len(self.x_range)), dtype='int')
        self.transitions_grid_map = np.zeros((len(self.y_range), len(self.x_range)), dtype='int')
        self.paintBorder()

    def load_initial_state(self):
        self.main_pixel_map[:, :] = self.markov_color_chain.states[0, :]  # initial state

    def paintBorder(self):
        # border_color = [20, 20, 20]
        border_color = self.markov_color_chain.states[3]
        self.main_pixel_map[:self.y_offset, :] = border_color
        self.main_pixel_map[self.y_offset:self.pixel_height - self.y_offset, :self.x_offset] = border_color
        self.main_pixel_map[self.y_offset:self.pixel_height - self.y_offset, self.pixel_width - self.x_offset:] \
            = border_color
        self.main_pixel_map[self.pixel_height - self.y_offset:, :] = border_color

    def updateImage(self):
        for ii in range(len(self.y_range)):
            for jj in range(len(self.x_range)):
                current_state = self.state_grid_map[ii, jj]
                self.state_grid_map[ii, jj] = self.markov_color_chain.getNextState(current_state)
                self.main_pixel_map[self.y_range[ii]:self.y_range[ii] + self.pixel_group_size,
                self.x_range[jj]:self.x_range[jj] + self.pixel_group_size] \
                    = self.markov_color_chain.states[self.state_grid_map[ii, jj], :]

    def generateSingleChainImageSteps(self, show=1):
        for x in range(self.tmax):
            print(x)
            self.updateImage()
            if show == 1:
                cv2.imshow('main', self.main_pixel_map)
                cv2.waitKey(1000)
        if self.WITH_OVERLAY == 1:
            self.addOverlay()

    def generateSingleChainImageFull(self):
        originalTM = self.markov_color_chain.transition_matrix
        for x in range(self.tmax):
            self.markov_color_chain.transition_matrix \
                = np.matmul(self.markov_color_chain.transition_matrix, originalTM)
        self.updateImage()
        if self.WITH_OVERLAY == 1:
            self.addOverlay()

    def addOverlay(self):
        self.main_pixel_map = cv2.cvtColor(self.main_pixel_map, cv2.COLOR_BGR2BGRA)
        indices = np.where(self.edges_image == [255])
        self.main_pixel_map[indices[0] + self.y_offset, indices[1] + self.x_offset, :] = self.OVERLAY_COLOR

    def addEpicenters(self, epcts):
        # epicenters = [(np.floor(self.pixel_height / 2), np.floor(self.pixel_width / 2))]
        for point in epcts:
            self.epicenters.append(point)

    def addEpicentersNormal(self, epcts):
        # epicenters = [(np.floor(self.pixel_height / 2), np.floor(self.pixel_width / 2))]
        for i in range(len(epcts)):
            epcts[i][0] = int(np.floor((self.pixel_height - self.y_offset) * epcts[i][0]))
            epcts[i][1] = int(np.floor((self.pixel_width - self.x_offset) * epcts[i][1]))
        for point in epcts:
            self.epicenters.append(point)

    def generateSingleChainCentersImage(self, snake_length, num_transitions):
        # generates all needed transition matrices
        num_states = np.shape(self.markov_color_chain.transition_matrix)[0]
        num_transitions_range = np.linspace(0, self.tmax-1, num_transitions, dtype='int')
        all_transition_matrices = np.zeros((num_transitions, num_states, num_states), dtype='float')
        all_transition_matrices[0] = np.identity(num_states)
        for ii in range(1, num_transitions):
            for jj in range(num_transitions_range[ii-1], num_transitions_range[ii]):
                all_transition_matrices[ii] = \
                    np.matmul(all_transition_matrices[ii-1], self.markov_color_chain.transition_matrix)

        # generates number of transitions at each square
        for loc in self.epicenters:
            grid_y = int(np.floor(loc[0]/self.pixel_group_size))
            grid_x = int(np.floor(loc[1]/self.pixel_group_size))
        # self.transitions_grid_map[grid_y][grid_x] = (self.tmax-1) * (self.transitions_grid_map[grid_y][grid_x] + 1)
            for ii in range(snake_length):
                self.transitions_grid_map[grid_y][grid_x] \
                    = min(num_transitions-1, self.transitions_grid_map[grid_y, grid_x]+1)
                x_choice, y_choice = self.getMove(grid_x, grid_y)
                grid_x = grid_x + x_choice
                grid_y = grid_y + y_choice

        for ii in range(len(self.y_range)):
            for jj in range(len(self.x_range)):
                current_state = self.state_grid_map[ii, jj]
                self.state_grid_map[ii, jj] = \
                    self.markov_color_chain.getNextState(current_state,
                                                         all_transition_matrices[self.transitions_grid_map[ii, jj]])
                self.main_pixel_map[self.y_range[ii]:self.y_range[ii] + self.pixel_group_size,
                                    self.x_range[jj]:self.x_range[jj] + self.pixel_group_size] \
                    = self.markov_color_chain.states[self.state_grid_map[ii, jj], :]

    def getMove(self, grid_x, grid_y):
        x_choice = random.randint(-1, 1)
        y_choice = random.randint(-1, 1)
        # if x_choice == 0 and y_choice == 0:
        #     x_choice, y_choice = self.getMove(grid_x, grid_y)
        if (grid_x + x_choice) >= len(self.x_range) or (grid_x + x_choice) < 0:
            x_choice, y_choice = self.getMove(grid_x, grid_y)
        if (grid_y + y_choice) >= len(self.y_range) or (grid_y + y_choice) < 0:
            x_choice, y_choice = self.getMove(grid_x, grid_y)
        return x_choice, y_choice

