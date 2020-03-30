# Michael Sikora <m.sikora@uky.edu>
# 2018.07.07
# generates an image using a markov state model
# where each pixel transitions through a markov model
# based only on its current state
# it is not intended to be viewed real-time as only
# very small images are not computationally costly.

# uses opencv-python, csv and numpy
import cv2
import numpy as np
import random
import csv


def get_next_state(current):
    evt = random.randint(1, 100)
    probs = transitionMatrix[current, :]*100
    nextstate = 0
    sum = 0
    for p in range(0, len(probs)):
        sum += probs[p]
        if evt <= sum:
            nextstate = p
            break
    return nextstate


def get_curr_state(pixel_value):
    currstate = 0
    for p in range(0, states.shape[0]):
        if sum(states[p, :] == pixel_value) == 3:
            currstate = p
    return currstate


def update_image():
    for ii in range(0, height, pixel_group_size):
        for jj in range(0, width, pixel_group_size):
            curr = get_curr_state(markov[ii, jj])
            next = get_next_state(curr)
            markov[ii:ii+pixel_group_size, jj:jj+pixel_group_size] = states[next, :]


# read in state space from csv
reader = csv.reader(open("states.csv", "r"), delimiter=',')
x = list(reader)
states = np.array(x).astype("int")

# read in transition matrix from csv
reader = csv.reader(open("transitionMatrix.csv", "r"), delimiter=',')
x = list(reader)
transitionMatrix = np.array(x).astype("float")


# make outline image
edgesim = cv2.imread('logo.png', -1)

# image dimensions
x_offset = 0
y_offset = 0
height = edgesim.shape[0] + 2*y_offset
width = edgesim.shape[1] + 2*x_offset
pixel_group_size = 2

tmax = 50  # number of transitions
markov = np.zeros((height, width, 3), np.uint8)  # generated image space
markov[:, :] = states[0, :]  # initial state


# RUN TRANSITIONS
cv2.namedWindow('main')
if ((height+width)/pixel_group_size*tmax) < 2500:  # if small enough run as a sequence
    for x in range(0, tmax):
        update_image()
        cv2.imshow('main', markov)
        cv2.waitKey(1000)
else:  # determine matrix result after run and generate last image
    originalTM = transitionMatrix
    for x in range(0, tmax):
        transitionMatrix = np.matmul(transitionMatrix, originalTM)
    print(transitionMatrix)
    update_image()

# cv2.imshow('main', markov)  # show last image
# cv2.imwrite('test2.png', markov)  # save last image

y1, y2 = y_offset, y_offset + edgesim.shape[0]
x1, x2 = x_offset, x_offset + edgesim.shape[1]
print(x1,x2,y1,y2)
print(edgesim.shape)

markov_bgra = cv2.cvtColor(markov, cv2.COLOR_BGR2BGRA)
print(markov_bgra.shape)
indices = np.where(edgesim == [255])
markov_bgra[indices[0]+y_offset, indices[1]+x_offset, :] = (255, 255, 255, 255)

cv2.imshow('main', markov_bgra)
cv2.imwrite('test2woverlay.png', markov_bgra)  # save last image

cv2.waitKey(0)  # stall program
cv2.destroyAllWindows()