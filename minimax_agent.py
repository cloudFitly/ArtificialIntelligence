# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

"""
    Enter your details below:

    Name: Tanmay Negi
    Student ID: u6741351
    Email: u6741351@anu.edu.au
"""

from typing import Tuple
import operator
from agents import Agent
from game_engine.actions import Directions
from search_problems import AdversarialSearchProblem

Position = Tuple[int, int]
Positions = Tuple[Position]
State = Tuple[int, Position, Position, Positions, float, float]

import numpy as np

def manhattan_heuristic(pos1: Position, pos2: Position) -> int:
    """The Manhattan distance heuristic for a PositionSearchProblem."""

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_heuristic(pos1: Position, pos2: Position) -> float:
    """The Euclidean distance heuristic for a PositionSearchProblem"""

    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
        """
        self.max_player = max_player
        self.depth = int(depth)


    def evaluation(self, problem: AdversarialSearchProblem, state: State) -> float:
        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number

            This evaluation function takes three factor in account
            score: the standard problem.utility(state)
            factor1 : the euclidean_distance between red and black agent, higher the distance more the evaluated score
            factor2 : number of surrounding states containing yellow_birds
                      this gives high weightage to states whose successors state contains yellow_bird

            calculated_score := score+yb_score*factor2+factor1

            factor2 is multiplied by yb_score to represent the tradeoff between agent gaining score by yellow bird to it's chance to come close to blackbird 
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state
        if problem.terminal_test(state):
            return problem.utility(state)
        score = problem.utility(state)
        
        
        factor1 = euclidean_heuristic(pos1=red_pos,pos2=black_pos)
        factor2 = 0 
        
        # factor3 = problem.maze_distance(pos1=red_pos,pos2=black_pos) # representing distance b/w red and black
        
        # method2
        """
        flag = 0
        for succ,_,_ in problem.get_successors(state):
            if succ[1] in yellow_birds:
                factor2 = factor2 + 1
            for nsucc,_,_ in problem.get_successors(succ):
                if nsucc[1] == black_pos:
                    flag = 1
                    break
        return score+yb_score*factor2 + flag*factor1   # takes factor1 in account only when black is twp 
        """


        return score+yb_score*factor2+flag*factor1
        # return score + factor2 + yb_score*(factor1+factor3) 

    def maximize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, str]:
        """ This method return a pair (max_utility, max_action).
            It implements alpha-beta pruning to limit expanded nodes
        """


        if problem.terminal_test(state) or current_depth==self.depth:
            # return (problem.utility(state),Directions.STOP)
            return (self.evaluation(problem=problem,state=state),Directions.STOP)
        # move = None
        # print("S")
        maxEval = -np.inf
        move = None
        for succ,action,_ in problem.get_successors(state):
            # print("c")
            evl = self.minimize(problem=problem,state=succ,current_depth=current_depth+1,alpha=alpha,beta=beta)
            #maxEval = max(maxEval,eval)
            if evl>maxEval:
                maxEval=evl
                move = action # taggging move associated with max utility
            alpha = max(alpha,evl)
            if beta <= alpha:
                break
                
        return (maxEval , move)



    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> float:
        """ This function  just return the minimum utility.
            It implements alpha-beta pruning to limit expanded nodes
        """


        if problem.terminal_test(state) or current_depth==self.depth:
            # return problem.utility(state)
            return self.evaluation(problem=problem,state=state)
        
        # without alpha-beta pruning
        # return min([self.maximize(problem=problem,state=succ,current_depth=current_depth+1)[0] for succ,_,_ in problem.get_successors(state)])

        # with alpha-beta pruning
        minEval = np.inf
        for succ,_,_ in problem.get_successors(state):
            evl = self.maximize(problem=problem,state=succ,current_depth=current_depth+1,alpha=alpha,beta=beta)[0]
            minEval = min(minEval,evl)
            beta = min(beta,evl)
            if beta <= alpha:
                break
        return minEval

        

    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:",
              max_action, "Expanded:", problem._expanded)
        return max_action
