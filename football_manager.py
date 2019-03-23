from fuzzywuzzy import fuzz
import random
from functions import *
from nn import *

"""=================================================================================================================="""
def decision(our_team, their_team, ball, your_side, half, time_left, our_score, their_score):
    manager_decision = [dict(), dict(), dict()]

    # X = [our_team, their_team, ball, your_side, half, time_left, our_score, their_score]
    # print(our_team[0]['alpha'])
    # X = our_team[0]['alpha']
    X = random.randint(0, 100)
    # print("X = ", X)
    y = random.randint(0, 100)
    # y = NN(X, y)
    # print("Y = ", y)
    for i in range(3):
        player = our_team[i]
        manager_decision[i]['alpha'] = player['alpha']
        manager_decision[i]['force'] = 0
        manager_decision[i]['shot_request'] = True
        manager_decision[i]['shot_power'] = 100000
    # print(our_score, their_score, end=' -- ')
    return manager_decision

