# given our current location, return only surrounding tiles that are free
def get_free_neighbors(game_state, location):

    x, y = location
    neighbors = [{(x-1, y): 'l'}, {(x+1, y): 'r'}, {(x, y-1): 'd'}, {(x, y+1): 'u'}]
    free_neighbors = []

    for neighbor in neighbors:
        for tile, direction in neighbor.items():
            if game_state.is_in_bounds(tile):
                if game_state.is_occupied(tile):
                    # check if this tile contains treasure or ammo
                    if game_state.entity_at(tile) == 't' or game_state.entity_at(tile) == 'a':
                        free_neighbors.append({tile:direction})
                else:
                    free_neighbors.append({tile:direction})

    return free_neighbors


# finds treasure, if any
def get_treasure(game_state):

    treasure = game_state.treasure

    if treasure:
        return treasure[0] # return first treasure on the list


def manhattan_distance(start, end):

    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])

    return distance


class Node:

    def __init__(self, parent=None, location=None, action=None):
        self.parent = parent
        self.location = location
        self.action = action

        self.h = 0
        self.g = 0
        self.f = 0


def get_path(node):
    path = []

    while node.parent:
        path.append(node)
        node = node.parent

    return path


def get_path_actions(path):

    actions = []

    for node in path:
        actions.append(node.action)

    return actions


def astar(game_state, start, target):

    print("----A* STAR----")
    path = []

    # add starting node to open list
    open_list = [Node(None, start, None)]
    closed_list = []

    # exit the loop early if no path can be found
    # (the target is likely blocked off)
    max_loops = 1000
    counter = 0

    # while lowest rank in OPEN is not the GOAL:
    while len(open_list) > 0 and counter <= max_loops:

        # find the node with the lowest rank
        curr_node = open_list[0]
        curr_index = 0

        for index, node in enumerate(open_list):
            if node.f < curr_node.f:
                curr_node = node
                curr_index = index

        # check if this node is the goal
        if curr_node.location == target:
            print(f"~~~~~~~FOUND TARGET~~~~~~~")
            path = get_path(curr_node)
            return path

        # current = remove lowest rank item from OPEN
        # add current to CLOSED
        del open_list[curr_index]
        closed_list.append(curr_node)

        # get neighbors of current
        neighbors = get_free_neighbors(game_state, curr_node.location)
        neighbor_nodes = []
        for neighbor in neighbors:
            for location, action in neighbor.items():
                neighbor_nodes.append(Node(None, location, action))

        #   for neighbors of current:
        for neighbor in neighbor_nodes:

            # used for loop behavior
            in_closed = False
            in_open = False

            # cost = g(current) + movementcost(current, neighbor)
            cost = curr_node.g + 1

            # if neighbor in OPEN and cost less than g(neighbor):
            #   remove neighbor from OPEN, because new path is better
            for index, node in enumerate(open_list):
                if neighbor.location == node.location and cost < neighbor.g:
                    del open_list[index]
                    in_open = True

            # if neighbor in CLOSED and cost less than g(neighbor): ⁽²⁾
            #   remove neighbor from CLOSED
            for index, node in enumerate(closed_list):
                if neighbor.location == node.location and cost < neighbor.g: 
                    del closed_list[index]
                    in_closed = True

            # if neighbor not in OPEN and neighbor not in CLOSED:
            #   set g(neighbor) to cost
            #   add neighbor to OPEN
            #   set priority queue rank to g(neighbor) + h(neighbor)
            #   set neighbor's parent to current
            if not in_open and not in_closed:
                neighbor.g = cost
                open_list.append(neighbor)
                neighbor.h = manhattan_distance(neighbor.location, target)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = curr_node

        counter += 1

    print(f"---NO PATH FOUND---")
