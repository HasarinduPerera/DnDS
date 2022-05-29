import random

class Agent:

    def __init__(self):
        '''
        Place any initialization code for your agent here (if any)
        '''
        pass

    def next_move(self, game_state, player_state):
        '''
        This method is called each time your Agent is required to choose an action
        '''

        ###### CODE HERE ######

        # a list of all the actions your Agent can choose from
        actions = ['','u','d','l','r','p']

        # randomly choosing an action
        action = random.choice(actions)

        ###### END CODE ######

        return action