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
import logic
import game

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

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostSearchProblem)
        """
        util.raiseNotDefined()

    def terminalTest(self, state):
        """
          state: Search state
        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionSearchProblem
        """
        util.raiseNotDefined()

    def result(self, state, action):
        """
        Given a state and an action, returns resulting state and step cost, which is
        the incremental cost of moving to that successor.
        Returns (next_state, cost)
        """
        util.raiseNotDefined()

    def actions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

    def getWidth(self):
        """
        Returns the width of the playable grid (does not include the external wall)
        Possible x positions for agents will be in range [1,width]
        """
        util.raiseNotDefined()

    def getHeight(self):
        """
        Returns the height of the playable grid (does not include the external wall)
        Possible y positions for agents will be in range [1,height]
        """
        util.raiseNotDefined()

    def isWall(self, position):
        """
        Return true if position (x,y) is a wall. Returns false otherwise.
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


def atLeastOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at least one of the expressions in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    return logic.Expr("|", *expressions)


def atMostOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that at most one of the expressions in the list is true.
    """

    listOfOrs = []
    firstLiteral = []
    for i in expressions:
        firstLiteral += [i];
        for j in expressions:
            if j not in firstLiteral:
                listOfOrs += [logic.Expr("|", logic.Expr("~", i), logic.Expr("~", j))]
    return logic.Expr("&", *listOfOrs)





def exactlyOne(expressions) :
    """
    Given a list of logic.Expr instances, return a single logic.Expr instance in CNF (conjunctive normal form)
    that represents the logic that exactly one of the expressions in the list is true.
    """
    return atLeastOne(expressions) & atMostOne(expressions)


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    timeSteps = {}
    for elem in model:
        action = elem.parseExpr(elem)[0]
        time = elem.parseExpr(elem)[1]
        if action in actions:
            if model[elem] == True:
                if time in timeSteps.keys():
                    update = timeSteps.get(time)
                    update += [action]
                    timeSteps[time] = update
                else:
                    timeSteps[time] = [action]
    path = []
    for i in range(len(timeSteps)):
        path += timeSteps[str(i)]
    return path



def initialConstraints(problem, start):
        height = problem.getHeight()
        width = problem.getWidth()
        exprList = [logic.PropSymbolExpr('P', start[0], start[1], 0)]
        for h in range(1, height + 1):
            for w in range(1, width + 1):
                if (h != start[1]) | (w != start[0]):
                    exprList += [logic.Expr("~", logic.PropSymbolExpr('P', w, h, 0))]
        return exprList


def dictInsert(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += [value]
    else:
        dictionary[key] = [value]


def getConstraintList(dictionary):
    dictKeys = dictionary.keys()
    const = []
    for elem in dictKeys:
        constList = dictionary[elem]
        laterConst = atLeastOne(constList)
        currConst = logic.to_cnf(logic.expr(elem % laterConst))
        const += [currConst]
    return const



def translateToSat(problem, start, actions, goalState, depth):
    exprList = initialConstraints(problem, start) #starts at initial state and is nowhere else
    height = problem.getHeight()
    width = problem.getWidth()
    for time in range(0, depth):
        actionsAtTime = []
        prog = {}
        for w in range(1, width + 1):
            for h in range(1, height + 1): #go through every position on the board
                currPos = logic.PropSymbolExpr('P', w, h, time) 
                if problem.isWall((w, h)) != True: #if the position is not a wall
                    possibleActions = problem.actions((w, h)) #get the actions from the position
                    for action in possibleActions:
                        if action == game.Directions.NORTH:
                            nextState = problem.result((w, h), action)[0]
                            currAction = logic.PropSymbolExpr('North', time)
                        if action == game.Directions.SOUTH:
                            nextState = problem.result((w, h), action)[0]
                            currAction = logic.PropSymbolExpr('South', time)
                        if action == game.Directions.WEST:
                            nextState = problem.result((w, h), action)[0]
                            currAction = logic.PropSymbolExpr('West', time)
                        if action == game.Directions.EAST:
                            nextState = problem.result((w, h), action)[0]
                            currAction = logic.PropSymbolExpr('East', time)
                        possibleState = logic.PropSymbolExpr('P', nextState[0], nextState[1], time + 1)
                        dictInsert(prog, possibleState, logic.Expr("&", currPos, currAction))
        exprList.extend(getConstraintList(prog))
        actionsAtTime += [logic.PropSymbolExpr('North', time)] #add each possible action at time to list
        actionsAtTime += [logic.PropSymbolExpr('South', time)]
        actionsAtTime += [logic.PropSymbolExpr('East', time)]
        actionsAtTime += [logic.PropSymbolExpr('West', time)]
        exprList += [logic.to_cnf(exactlyOne(actionsAtTime))] #can only take one action at any time
    goalStateAtTime = logic.PropSymbolExpr('P', goalState[0], goalState[1], depth)
    exprList += [goalStateAtTime] #add goal state to constraints
    return exprList


def positionLogicPlan(problem):
    """
    Given an instance of a PositionSearchProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    actions = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    startState = problem.getStartState()
    goalState = problem.getGoalState()
    for depth in range(0, 50):
        sat = translateToSat(problem, startState, actions, goalState, depth)
        if sat:
            world = logic.pycoSAT(sat)
            if world != False:
                path = extractActionSequence(world, ['North', 'South', 'East', 'West'])
                return path


def foodSat(problem, start, actions, goalState, depth, foods):
    exprList = initialConstraints(problem, start) #starts at initial state and is nowhere else
    height = problem.getHeight()
    width = problem.getWidth()
    for time in range(0, depth):
        actionsAtTime = []
        prog = {}
        for h in range(1, height + 1): #go through every position on the board
            for w in range(1, width + 1):
                currPos = logic.PropSymbolExpr('P', w, h, time) 
                if problem.isWall((w, h)) != True: 
                    fakeState = ((w, h), foods)
                    possibleActions = problem.actions(fakeState) #get the actions from the position
                    for action in possibleActions:
                        if action == game.Directions.NORTH:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('North', time)
                        if action == game.Directions.SOUTH:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('South', time)
                        if action == game.Directions.WEST:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('West', time)
                        if action == game.Directions.EAST:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('East', time)
                        possibleState = logic.PropSymbolExpr('P', nextState[0], nextState[1], time + 1)
                        dictInsert(prog, possibleState, logic.Expr("&", currPos, currAction))
        exprList.extend(getConstraintList(prog))
        actionsAtTime += [logic.PropSymbolExpr('North', time)] #add each possible action at time to list
        actionsAtTime += [logic.PropSymbolExpr('South', time)]
        actionsAtTime += [logic.PropSymbolExpr('East', time)]
        actionsAtTime += [logic.PropSymbolExpr('West', time)]
        exprList += [logic.to_cnf(exactlyOne(actionsAtTime))] #can only take one action at any time
        
    for food in goalState:
        foodList = []
        for t in range(0, depth + 1):
            currFd = logic.PropSymbolExpr('P', food[0], food[1], t)
            foodList += [currFd]
        exprList += [logic.to_cnf(atLeastOne(foodList))]

    return exprList



def foodLogicPlan(problem):
    """
    Given an instance of a FoodSearchProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    actions = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    startState = problem.getStartState()
    foods = problem.getStartState()[1]
    omnom = foods.asList()
    for depth in range(0, 50):
        sat = foodSat(problem, startState[0], actions, omnom, depth, foods)
        if sat:
            world = logic.pycoSAT(sat)
            if world != False:
                path = extractActionSequence(world, ['North', 'South', 'East', 'West'])
                return path


def foodGhostSat(problem, start, actions, goalState, depth, foods, ghosties):
    exprList = initialConstraints(problem, start) #starts at initial state and is nowhere else
    height = problem.getHeight()
    width = problem.getWidth()
    for ghost in ghosties:
        dir = 'East'
        curr = ghost.getPosition()
        for d in range(0, depth):
            currPos = logic.PropSymbolExpr('P', curr[0], curr[1], d + 1) 
            exprList += [logic.Expr("~", currPos)]
            if dir == 'East':
                if problem.isWall((curr[0] + 1, curr[1])):
                    dir = 'West'
            else:
                if problem.isWall((curr[0] - 1, curr[1])):
                    dir = 'East'
            if dir == 'East':
                curr = (curr[0] + 1, curr[1])
            else:
                curr = (curr[0] - 1, curr[1])
            nextPos = logic.PropSymbolExpr('P', curr[0], curr[1], d + 1)
            exprList += [logic.Expr("~", nextPos)]
    for time in range(0, depth):
        actionsAtTime = []
        prog = {}
        for h in range(1, height + 1): #go through every position on the board
            for w in range(1, width + 1):
                currPos = logic.PropSymbolExpr('P', w, h, time) 
                if problem.isWall((w, h)) != True: #if the position is not a wall
                    fakeState = ((w, h), foods)
                    possibleActions = problem.actions(fakeState) #get the actions from the position
                    for action in possibleActions:
                        if action == game.Directions.NORTH:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('North', time)
                        if action == game.Directions.SOUTH:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('South', time)
                        if action == game.Directions.WEST:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('West', time)
                        if action == game.Directions.EAST:
                            nextState = problem.result(fakeState, action)[0][0]
                            currAction = logic.PropSymbolExpr('East', time)
                        possibleState = logic.PropSymbolExpr('P', nextState[0], nextState[1], time + 1)
                        dictInsert(prog, possibleState, logic.Expr("&", currPos, currAction))
        exprList.extend(getConstraintList(prog))
        actionsAtTime += [logic.PropSymbolExpr('North', time)] #add each possible action at time to list
        actionsAtTime += [logic.PropSymbolExpr('South', time)]
        actionsAtTime += [logic.PropSymbolExpr('East', time)]
        actionsAtTime += [logic.PropSymbolExpr('West', time)]
        exprList += [logic.to_cnf(exactlyOne(actionsAtTime))] #can only take one action at any time

    for food in goalState:
        foodList = []
        for t in range(0, depth + 1):
            currFd = logic.PropSymbolExpr('P', food[0], food[1], t)
            foodList += [currFd]
        exprList += [logic.to_cnf(atLeastOne(foodList))]

    return exprList


def foodGhostLogicPlan(problem):
    """
    Given an instance of a FoodGhostSearchProblem, return a list of actions that help Pacman
    eat all of the food and avoid patrolling ghosts.
    Ghosts only move east and west. They always start by moving East, unless they start next to
    and eastern wall. 
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    "*** YOUR CODE HERE ***"
    actions = [game.Directions.NORTH, game.Directions.SOUTH, game.Directions.EAST, game.Directions.WEST]
    startState = problem.getStartState()
    foods = problem.getStartState()[1]
    omnom = foods.asList()
    ghosties = problem.getGhostStartStates()
    for depth in range(0, 50):
        sat = foodGhostSat(problem, startState[0], actions, omnom, depth, foods, ghosties)
        if sat:
            world = logic.pycoSAT(sat)
            if world != False:
                path = extractActionSequence(world, ['North', 'South', 'East', 'West'])
                return path


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan
fglp = foodGhostLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)