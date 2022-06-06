from .helpers import *

class Agent:

    def __init__(self):
        '''
        Place any initialization code for your agent here (if any)
        '''
        self.pending_actions = []

    def next_move(self, game_state, player_state):

        print(f"tick: {game_state.tick_number}")

        # treasure spawns randomly
        treasure = get_treasure(game_state)

        if len(self.pending_actions) > 0:
            action = self.pending_actions.pop()
        elif treasure:
            path = astar(game_state, player_state.location, treasure)

            if path:
                actions = get_path_actions(path)
                print(f"--ACTIONS: {actions}")

                for action in actions:
                    self.pending_actions.append(action)

                action = self.pending_actions.pop()
            else:
                action = ''
        else:
            action = ''

        return action

