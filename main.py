# Michael Sikora <m.sikora@uky.edu>
# 2020.03.30
# generates an image using a markov state model
# where each pixel transitions through a markov model
# based only on its current state
# it is not intended to be viewed real-time as only
# very small images are not computationally costly.

# update - code has been split into two seperate classes.
# one class for the color scheme markov chain, the second for
# the generative image

# uses opencv-python, csv and numpy
import cv2
from markovColorChain import ColorChain
from markovImage import MarkovImage

# define a color chain
chain_blue = ColorChain('chain1')
chain_bright = ColorChain('chain2')
# chain_purple = ColorChain('chain3')
# chain_red = ColorChain('chain4')
chain_new = ColorChain('.')

# args : color_chain, with_overlay_flag, resolution, pixel_grp_size, maximum_transitions, border_size
# image1 = MarkovImage(chain_new, 0, [1080, 1940], 1, 10000, [0, 0])  # HD Desktop Wallpaper
# image1 = MarkovImage(chain_new, 0, [1080, 1080], 1, 10000, [200, 200])  # HD square
# image1 = MarkovImage(chain_new, 0, [2160, 3840], 1, 10000, [0, 0])  # HD 16:9 Wallpaper
# image1 = MarkovImage(chain_new, 0, [1520, 720], 1, 10000, [50, 50])  # Phone Wallpaper
image1 = MarkovImage(chain_bright, 0, [600, 600], 2, 10000, [0, 0])  # small square

# Generate several epicenters in a grid
# epicenters = []
# stepsize = 50
# N = int(np.floor((1080-400)/stepsize))
# for i in range(N):
#     for j in range(N):
#         epicenters.append([stepsize*(i+1)+200, stepsize*(j+1)+200])

# epicenters = [[0.16, 0.16],
#               [0.8, 0.25],
#               [0.41, 0.8]]
epicenters = [[0.8, 0.1]]
image1.addEpicentersNormal(epicenters)

# #################### SETUP WINDOW ####################
cv2.namedWindow('main')
# cv2.namedWindow('main', flags=cv2.WINDOW_GUI_NORMAL)
# cv2.setWindowProperty('main', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# #################### MAKE IMAGE ####################
# image1.generateSingleChainImageSteps(1)
# image1.generateSingleChainImageFull()
# args : length of snakes, number of transition matrices
image1.generateSingleChainCentersImage(100000, 10)

# #################### SHOW IMAGE ####################
cv2.imshow('main', image1.main_pixel_map)
cv2.waitKey(0)  # stall program

# #################### SAVE IMAGE ####################
# cv2.imwrite('square11.png', image1.main_pixel_map)  # save last image
# cv2.imwrite('phonewallpaper3.png', image1.main_pixel_map)  # save last image

cv2.destroyAllWindows()