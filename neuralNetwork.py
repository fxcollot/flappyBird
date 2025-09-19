import numpy as np
import random 
#import mainTraining
import mainTraining

def network_initialization(input_size=5, hidden_size=5, output_size=1):

    W1 = np.random.randn(input_size, hidden_size) * 0.1

    b1 = np.zeros((1, hidden_size))

    W2 = np.random.randn(hidden_size, output_size) * 0.1

    b2 = np.zeros((1, output_size))

    return [W1, b1, W2, b2]#{"W1": W1, "b1": b1, "W2": W2, "b2": b2}

def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x))

def forward_propagation(X, params):

    W1, b1, W2, b2 = params[0], params[1], params[2], params[3]

    Z1 = np.dot(X, W1) + b1
    A1 = relu(Z1)

    Z2 = np.dot(A1, W2)+ b2
    A2 = sigmoid(Z2)

    return A2

def mutation( generation_result, variation, prob,  keeping_threshold, new_randoms ):
    new_generation = []

    # WINNERS & MUTATIONS
    ranking = 0
    for player, _ in generation_result:
        ranking += 1
        if ranking <= keeping_threshold:
            new_generation.append(player)
            new_player = []
            for i in player.params:
                add = 0
                mult = 1
                if random.randint(1,10) > prob:
                    add = i * variation
                    if random.randint(1,10) > prob:
                        mult = (-1)
                new_player.append(i + add * mult)
            new_generation.append(mainTraining.GenAI(new_player))
        else:
            player.destroy()

    # NEW PLAYERS
    for _ in range(new_randoms):
        new_generation.append(mainTraining.GenAI(network_initialization()))

    return new_generation


def last_network(W1, b1, W2, b2, store):
    if store:
        with open("store.txt", "w") as f:
            f.write(W1 + "\n" + b1 + "\n" + W2 + "\n" + b2)
            return [W1, b1, W2, b2]
    else:
        with open("store.txt", "r"):
            lastW1 = f.readline()
            lastb1 = f.readline()
            lastW2 = f.readline()
            lastb2 = f.readline()
        return [lastW1, lastb1, lastW2, lastb2]

    

