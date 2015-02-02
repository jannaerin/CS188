# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    goalFound = 0
    explored = []
    actions = []
    frontier = util.Queue()
    frontier.push([problem.getStartState(), actions]) # item = [state, action list]
    while frontier.isEmpty() != True:
        next = frontier.pop() #[state, action list]
        if next[0] not in explored:
            if problem.isGoalState(next[0]):
                goalFound = 1
                actions = next[1]
                #print("in goal", actions)
                return actions
            else:
                successors = problem.getSuccessors(next[0])
                updateExploredSet(next[0], explored)
                for elem in successors:
                    if elem[0] not in explored:
                        frontier.push([elem[0], next[1] + [elem[1]]])
    if goalFound == 0:
        return []

    """state = problem.getStartState()
    print("start state is", state)
    if problem.isGoalState(state):
        print("found",[state])
        return [state]
    frontier = util.Queue()
    explored = []
    frontierList = []
    frontier.push([state, []])
    frontierList += [state]
    while frontier.isEmpty() != True:
        next = frontier.pop()
        actions = next[1]
        print("just popped ", next)
        if next[0] not in explored:
            explored += [next[0]]
            successors = problem.getSuccessors(state)
            for elem in successors:
                if elem[0] not in frontierList:
                    if problem.isGoalState(elem[0]):
                        print("found goal returning", actions + [elem[1]])
                        return actions + [elem[1]]
                    frontier.push([elem[0], actions + [elem[1]]])
                    print("just pushed ", [elem[0], actions + [elem[1]]])
                    frontierList += [elem[0]]
    print("didn't find goal")
    return []"""


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

explored = [] # make explored set global variable 
goalFound = 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth.

    Begin with a depth of 1 and increment depth by 1 at every step.
    """
    global goalFound
    global explored
    depth = 0
    actions = []
    while goalFound == 0:
        actions = []
        explored = []
        actions = depthLimitedDFS(problem, problem.getStartState(), depth, actions)
        if len(actions) != 0:
            goalFound = 0
            return actions
        else:
            depth += 1
    goalFound = 0
    return actions

def depthLimitedDFS(problem, state, depth, actions):
    global goalFound
    global explored
    frontier = util.Stack()
    if problem.isGoalState(state):
        goalFound = 1
        return actions
    elif depth == 0:
        return actions # cutoff value
    else:
        successors = problem.getSuccessors(state)
        for elem in successors:
            if elem[0] not in explored:
                frontier.push(elem)
                updateExploredSet(elem[0], explored)
        while frontier.isEmpty() != True:
            next = frontier.pop()
            actions += [next[1]]
            nextAc = depthLimitedDFS(problem, next[0], depth - 1, actions)
            if goalFound == 0:
                del actions[-1]
            else:
                return actions
    return actions # failure value


def updateExploredSet(vertex, currExplored):
    currExplored.append(vertex)
    return currExplored


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    goalFound = 0
    explored = []
    actions = []
    frontier = util.PriorityQueue()
    frontier.push([problem.getStartState(), actions, 0], heuristic(problem.getStartState(), problem)) # item = [state, action list, total path cost]
    while frontier.isEmpty() != True:
        next = frontier.pop() #[state, action list]
        if next[0] not in explored:
            if problem.isGoalState(next[0]):
                goalFound = 1
                actions = next[1]
                return actions
            else:
                successors = problem.getSuccessors(next[0])
                updateExploredSet(next[0], explored)
                for elem in successors:
                    if elem[0] not in explored:
                        frontier.push([elem[0], next[1] + [elem[1]], next[2] + elem[2]], next[2] + elem[2] + heuristic(elem[0], problem))
    if goalFound == 0:
        return []


def findMyPath(node, actions):
    if node.actionToGetToMe == None: #root node
        return actions[::-1] #return actions list reversed
    else:
        actions += [node.actionToGetToMe]
        findMyPath(node.parent, actions)


class childNode:

    def __init__(self, parent, action):
        self.mama = parent
        self.actionToGetToMe = action


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
