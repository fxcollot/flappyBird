import pygame
import random
import time
from main import runGraphics
from neuralNetwork import last_network, forward_propagation, network_initialization, mutation
from pygame.locals import *

HEIGHT = 336
WIDTH = 496
ACC = 0.5
FRIC = -0.12
FPS = 60

class GenAI():
    def __init__(self, params):
        self.params = params
        self.x = [ HEIGHT/2 - 15, HEIGHT/2 + 15 ]
        self.y = [ WIDTH/6 - 15, WIDTH/6 + 15 ]
        self.speed = 0
        self.X = [0, 0, self.speed, 0, 0]

    def flapChoice(self):
        output = forward_propagation(self.X, self.params)
        return output > 0.5

    def update(self):
        if all_pipes != []:
            self.X = [(self.x[0]+self.x[1]) / 2, (self.y[0]+self.y[1])/2, self.speed, (all_pipes[0].x[0]+all_pipes[0].x[1])/2, (all_pipes[0].y[1]+all_pipes[0].y[2])/2]
        if self.flapChoice():
            self.speed -= 4
        self.speed += 0.5
        self.y = [self.y[0] - self.speed, self.y[1] - self.speed]

    def destroy(self):
        del self

class Pipe():
    def __init__(self):
        super().__init__()
        height = random.randint(10, 50)
        space = 80
        self.x = [ 450, 500 ]
        self.y = [ 60-height, 60+90-height,200-height+space, 200+90-height+space ]

    def update(self, player):
        self.x = [self.x[0] - 2, self.x[1] - 2]
        if self.x[1] < player.x[0]:
            all_pipes.remove(self)


def runWithoutGraphics(player, frame_counter, all_pipes, score):
    running = True
    lost = False

    while running:
        frame_counter += 1
        score += 1

        player.update()

        if frame_counter == 60:
            frame_counter = 0
            all_pipes.append(Pipe())

        for pipe in all_pipes:

            #print(" Pipe ", all_pipes.index(pipe), " : ", pipe.x, pipe.y)

            if (player.x[1] > pipe.x[0]) & (player.x[0] < pipe.x[1]):
                if ( ( player.y[0] < pipe.y[1] ) ):
                    lost = True
                elif ( (player.y[1] > pipe.y[2] ) ):
                    lost = True

            if player.y[1] > HEIGHT:
                lost = True
            elif player.y[0] < 0:
                lost = True

            if lost:
                running = False

            pipe.update(player)
    
    return score

generation = [GenAI(network_initialization()) for _ in range(100)]

for _ in range(50):
    generation_result = []
    i = 0
    for player in generation:
        i += 1
        frame_counter = 59
        all_pipes = []
        score = 0
        finalScore = runWithoutGraphics(player, frame_counter, all_pipes, score)
        generation_result.append((player, finalScore))
        generation_result.sort(key=lambda tup: tup[1], reverse=True)  # sorts in place
    generation = mutation(generation_result, 0.1, 0.5, 30, 40)



    print(generation_result[0:10])

print(generation_result[0][0].params)
#runGraphics(generation_result[0][0])