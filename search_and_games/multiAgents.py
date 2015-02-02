# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
                # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        newPos = successorGameState.getPacmanPosition()

        newFood = successorGameState.getFood()

        newGhostStates = successorGameState.getGhostStates()
 
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        currScore = successorGameState.getScore()
        numAgents = successorGameState.getNumAgents()
        currentFood = currentGameState.getFood()
        currentCapsules = currentGameState.getCapsules()

        currentFoodAsList = currentFood.asList()

        foodPathCost = float("inf")
        if len(currentFoodAsList) == 0:
            return 0
        for food in currentFoodAsList:
            distance = ((newPos[0] - food[0]) ** 2 + (newPos[1] - food[1]) ** 2) ** 0.5
            if distance < foodPathCost:
                foodPathCost = distance
        foodCost = foodPathCost + 1

        
        ghostPathCost = float("inf")
        if numAgents == 1:
            return 0
        ghostIndex = 1
        while ghostIndex < numAgents:
            ghost = successorGameState.getGhostPosition(ghostIndex)
            distance = ((newPos[0] - ghost[0]) ** 2 + (newPos[1] - ghost[1]) ** 2) ** 0.5
            if distance < ghostPathCost:
                ghostPathCost = distance
            ghostIndex += 1
        ghostCost = ghostPathCost + 1

        totalScore = currScore + (5/foodCost)  - (3/ghostCost)

        return totalScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        bestVal = float("-inf") #best current move for pacman
        bestMove = None
        totalGhosts = gameState.getNumAgents() - 1
        legal = gameState.getLegalActions(0)
        for action in legal:
          newState = gameState.generateSuccessor(0, action)
          newVal = bestVal
          bestVal = max(bestVal, self.minValue(newState, 1, totalGhosts, self.depth))
          if bestVal > newVal:
            bestMove = action
        return bestMove

    def maxValue(who, gameState, totalGhosts, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return who.evaluationFunction(gameState)
        bestVal = float("-inf")
        legal = gameState.getLegalActions(0)
        for action in legal:
          newState = gameState.generateSuccessor(0, action) 
          bestVal = max(bestVal, who.minValue(newState, 1, totalGhosts, depth))
        return bestVal

    def minValue(who, gameState, ghost, totalGhosts, depth):
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return who.evaluationFunction(gameState)
      bestVal = float("inf")
      if ghost < totalGhosts:
        legal = gameState.getLegalActions(ghost)
        for action in legal:
          newState = gameState.generateSuccessor(ghost, action) 
          bestVal = min(bestVal, who.minValue(newState, ghost + 1, totalGhosts, depth))
      elif ghost == totalGhosts:
        legal = gameState.getLegalActions(ghost)
        for action in legal:
          newState = gameState.generateSuccessor(ghost, action)   
          bestVal = min(bestVal, who.maxValue(newState, totalGhosts, depth - 1))
      return bestVal

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        bestVal = float("-inf") #best current move for pacman
        bestMove = None
        totalGhosts = gameState.getNumAgents() - 1
        legal = gameState.getLegalActions(0)
        for action in legal:
          newState = gameState.generateSuccessor(0, action)
          newVal = bestVal
          bestVal = max(bestVal, self.expectedValue(newState, 1, totalGhosts, self.depth))
          #print("bestval is", bestVal)
          if bestVal > newVal:
            bestMove = action
        #print bestMove
        return bestMove

    def maxValue(who, gameState, totalGhosts, depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return who.evaluationFunction(gameState)
        bestVal = float("-inf")
        legal = gameState.getLegalActions(0)
        for action in legal:
          newState = gameState.generateSuccessor(0, action) 
          bestVal = max(bestVal, who.expectedValue(newState, 1, totalGhosts, depth))
        #  print("best Val in max in loop is", bestVal)
       # print("best val max returning", bestVal)
        return bestVal

    def expectedValue(who, gameState, ghost, totalGhosts, depth):
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return who.evaluationFunction(gameState)
      bestVal = 0
      if ghost < totalGhosts:
        legal = gameState.getLegalActions(ghost)
        numLegal = len(legal)
        probability = float(1.0 / numLegal)
        #print ("probability is ", probability)
        for action in legal:
          newState = gameState.generateSuccessor(ghost, action) 
          bestVal =  bestVal + (probability * who.expectedValue(newState, ghost + 1, totalGhosts, depth))
          #print("best Val in expected in loop is", bestVal)
      elif ghost == totalGhosts:
        legal = gameState.getLegalActions(ghost)
        numLegal = len(legal)
        probability = float(1.0 / numLegal)
        #print ("probability is ", probability)
        for action in legal:
          newState = gameState.generateSuccessor(ghost, action)   
          bestVal = bestVal + (probability * who.maxValue(newState, totalGhosts, depth - 1))
          #print("best Val in expected in loop is", bestVal)
     # print("best val expected returning", bestVal)
      return bestVal

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 9).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    print "starting the eval"
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    currScore = currentGameState.getScore()
    numAgents = currentGameState.getNumAgents()
    currentFood = currentGameState.getFood()
    currentCapsules = currentGameState.getCapsules()
    currentFoodAsList = currentFood.asList()

    foodPathCost = float("inf")
    for food in currentFoodAsList:
        distance = abs(newPos[0] - food[0])+ abs(newPos[1] - food[1])
        if distance < foodPathCost:
            foodPathCost = distance
    foodCost = foodPathCost   # closest food is this far away WANTS TO MINIMIZE
        
    ghostPathCost = float("inf")
    ghostIndex = 1
    while ghostIndex < numAgents:
        ghost = currentGameState.getGhostPosition(ghostIndex)
        distance = abs(newPos[0] - ghost[0]) + abs (newPos[1] - ghost[1]) 
        if distance < ghostPathCost:
            ghostPathCost = distance
        ghostIndex += 1
    ghostCost = ghostPathCost + 1 #closest ghost is this far away WANT TO MAXIMIZE

    capsulePathCost = float("inf")
    for cap in currentCapsules:
        distance = abs(newPos[0] - cap[0]) + abs (newPos[1] - cap[1])
        if distance < capsulePathCost:
            capsulePathCost = distance
    capsuleCost = capsulePathCost      

        #totalScore = currScore + 5/foodCost + 10/capsuleCost - 3/ghostCost
    
    numFoodLeft = len(currentFoodAsList)

    foodFloat = float(1.0 / foodCost)
    ghostFloat = float(1.0 / ghostCost)


    if numFoodLeft == 0:
      #print "NO FOOD"
      totalScore = 1000000000
    elif newScaredTimes[0] > 0:
        #print "ghost is SCARED"
        totalScore = currScore + 4*foodFloat + 10*ghostFloat #- numFoodLeft
    elif ghostCost > 4: 
        totalScore = currScore + 5*foodFloat #- numFoodLeft
    else:
        totalScore = currScore + foodFloat - 10*ghostFloat #- numFoodLeft

    return totalScore



# Abbreviation
better = betterEvaluationFunction

# Abbreviation
better = betterEvaluationFunction

