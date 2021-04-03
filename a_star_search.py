"""
    Enter your details below:

    Name: tanmay negi
    Student ID: u6741351
    Email: u6741351@anu.edu.au
"""

from typing import Callable, List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem
from search_strategies import SearchNode
from frontiers import PriorityQueue
import numpy as np


# def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
#     """See 2_implementation_notes.md for more details.

#     Your search algorithms needs to return a list of actions that reaches the
#     goal from the start state in the given problem. The elements of this list
#     need to be one or more references to the attributes NORTH, SOUTH, EAST and
#     WEST of the class Directions.
#     """

#     raise_not_defined()  # Remove this line when your solution is implemented
#     # *** YOUR CODE HERE ***


def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """
    implements astar search algorithm
    """
    problem_type = type(problem).__name__
    if problem_type == "PositionSearchProblem":
        return PositionSearchProblem(problem=problem,heuristic=heuristic).A_Star()
    elif problem_type =="MultiplePositionSearchProblem":
        print("not completed")
        raise_not_defined()
    

# supporting classes

# class MultiplePositionSearchProblem():
#     """
#     creates a model for MultiplePositionSearchProblem
#     """
#     def __init__(self,problem,heuristic):
#         self.problem   = problem
#         self.heuristic = heuristic
#         self.cameFrom  = {}
#         self.openSet   = PriorityQueue()
#         self.gScore    = {}
#         self.nirds     = self.problem.get_initial_state()[1]
#         self.actions   = []

#     def reconstruct_path():
#         return None

#     def A_Star(self):
#         """
#         state = ((in,int) , ((int,int)), str, int)

#         """
#         start = self.problem.get_initial_state

#         start_node = Node(state=self.problem.get_initial_state()[0],
#                  fScore=self.heuristic(pos=self.problem.get_initial_state()[0],problem=self.problem),
#                  gScore=0)
#         self.openSet.push(item=state,priority=start.fScore)
#         self.gScore = {self.problem.get_initial_state()[0]:0}
        
#         while not self.openSet.is_empty():
#             current = self.openSet.pop()
            
#             if current.state in self.birds:
#                 add_to_actions(reconstruct_path(start=start,current=current_state.state))
#                 self.birds.remove(current.state)
#             for succ,rem,action,cost in self.problem.get_successors(current.state):
#                 if self.problem.get_walls()[succ[0]][succ[1]]:
#                     continue
#                 if succ not in self.gScore.keys():
#                     self.gScore[succ] = np.inf

#                 t_gScore = current.gScore + cost

#                 if t_gScore < self.gScore[succ]:
#                     self.cameFrom[succ] = (current.state,action)
#                     self.gScore[succ] = t_gScore
#                     succ_node = Node(state=succ,action=action,parent=current.state,
#                         fScore = t_gScore+self.heuristic(pos=))



#         start = Node(state=self.problem.get_initial_state()[0],
#                  fScore=self.heuristic(pos=self.problem.get_initial_state()[0],problem=self.problem),
#                  gScore=0)
#         self.openSet.push(item=start,priority=start.fScore)
#         self.gScore = {self.problem.get_initial_state():0}

#         while not self.openSet.is_empty():
#             # openSet is a priority queue
#             current = self.openSet.pop() # returns the node associated with lowest fScore
#             if self.problem.goal_test(current.state):
#                 return self.reconstruct_path(current.state)

#             for succ,action,cost in self.problem.get_successors(current.state):
#                 if self.problem.get_walls()[succ[0]][succ[1]]:
#                     continue
#                 if succ not in self.gScore.keys():
#                     self.gScore[succ] = np.inf

#                 t_gScore = current.gScore + cost # d(current,neighbour) ; Wiki

#                 if t_gScore < self.gScore[succ]:
#                     self.cameFrom[succ] = (current.state,action) # a tuple of parent and action
#                     self.gScore[succ] = t_gScore
#                     succ_node = Node(state=succ,action=action,gScore=self.gScore[succ],parent=current.state,
#                             fScore=t_gScore+self.heuristic(pos=succ,problem=self.problem))
                    
#                     if not self.openSet.find(lambda node: node.state == succ):
#                         self.openSet.push(item=succ_node,priority=succ_node.fScore)
#         print("failure")
#         return None



class Node(SearchNode):
    def __init__(self,state,action=None,parent=None,gScore=np.inf,fScore=np.inf):
        super().__init__(state=state,action=action,parent=parent)
        self.fScore = fScore
        self.gScore = gScore

class PositionSearchProblem():
    """
    creates the model for PositionalSearch Problem
    """
    
    def __init__(self,problem,heuristic):
        self.problem   = problem
        self.heuristic = heuristic
        self.cameFrom  = {}
        self.openSet   = PriorityQueue()
        self.gScore    = {}
        # fScore will be attached to each node(state) hence not needed as extra variable
        

    def reconstruct_path(self,current_state):
        actions = []
        while current_state is not self.problem.get_initial_state():
            actions.append(self.cameFrom[current_state][1]) # cameFrom[state] = (state.parent,action[parent->state])
            current_state = self.cameFrom[current_state][0]
        return actions[::-1]

    def A_Star(self):
        """
        This implements Astar search algorithm on PositionSearchProblem
        Here I implemented the pseudo-code given on wikipedia <https://en.wikipedia.org/wiki/A*_search_algorithm>

        Most of the variable/functions names are kept same for proper follow up (please refer to the link for in-depth detail)
        """
        start = Node(state=self.problem.get_initial_state(),
                 fScore=self.heuristic(pos=self.problem.get_initial_state(),problem=self.problem),
                 gScore=0)
        self.openSet.push(item=start,priority=start.fScore)
        self.gScore = {self.problem.get_initial_state():0}

        while not self.openSet.is_empty():
            # openSet is a priority queue
            current = self.openSet.pop() # returns the node associated with lowest fScore
            if self.problem.goal_test(current.state):
                return self.reconstruct_path(current.state)

            for succ,action,cost in self.problem.get_successors(current.state):
                if self.problem.get_walls()[succ[0]][succ[1]]:
                    continue
                if succ not in self.gScore.keys():
                    self.gScore[succ] = np.inf

                t_gScore = current.gScore + cost # d(current,neighbour) ; Wiki

                if t_gScore < self.gScore[succ]:
                    self.cameFrom[succ] = (current.state,action) # a tuple of parent and action
                    self.gScore[succ] = t_gScore
                    succ_node = Node(state=succ,action=action,gScore=self.gScore[succ],parent=current.state,
                            fScore=t_gScore+self.heuristic(pos=succ,problem=self.problem))
                    
                    if not self.openSet.find(lambda node: node.state == succ):
                        self.openSet.push(item=succ_node,priority=succ_node.fScore)
        print("failure")
        return None

