"""
    Enter your details below:

    Name: Tanmay Negi
    Student ID: u6741351
    Email: u6741351@anu.edu.au
"""

from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem

from game_engine.actions import Actions, Directions
from frontiers import Queue , Stack


from search_strategies import SearchNode 

class Node(SearchNode):
    def __init__(self,state,action=None,path_cost=0,parent=None,depth=0,visited=False):
        super().__init__(state,action,path_cost,parent,depth)
        self.visited = visited

def map_network(problem: SearchProblem):
    """
    problem: SearchProblem -> tuple(dict{(int,int):Node()} , (int,int))

    Returns a Tuple(dictionary{state: Node(state.information)} , goal_state)

    The frontier used is Queue with FIFO policy
            

    """

    start = problem.get_initial_state()
    queue = Queue()
    network = {}
    goal = None
    network[start] = Node(start,visited=True)
    queue.push(start)
    
    flag = True
    while not queue.is_empty() and flag:
        p = queue.pop()
        for succ,action,cost in problem.get_successors(p):
            
            # walls check and loop check
            if problem.get_walls()[succ[0]][succ[1]] or succ in network.keys():
                continue
            cost = network[p].path_cost + 1
            network[succ] = Node(state=succ,action=action,path_cost=cost,parent=p,visited=True)


            queue.push(succ)

            if problem.goal_test(succ):
                goal = succ
                flag = False
    return network,goal


def solve(problem: SearchProblem) -> List[str]:
    """
    
    problem -> list[action]
    returns a list of actions from start to goal_state
    """
    network = None
    goal = None
    try:
        network, goal = map_network(problem)
        if not network or not goal:
            raise ValueError("network mapping error!!!")
    except ValueError as e:
        print(e)
        return None

    actions = []
    flag = True
    start = problem.get_initial_state()
    while flag:

        actions.append(network[goal].action)
        goal = network[goal].parent
        if goal == start:
            flag = False

    return actions[::-1]