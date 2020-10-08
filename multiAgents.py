# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newGhost = successorGameState.getGhostPositions()
        foodDist = newFood.asList()
        score = successorGameState.getScore()
        for dist in foodDist:
            newfoodDist = util.manhattanDistance(newPos, dist)
            score += 1/newfoodDist


        #if ghost too near, then don't go in that Direction
        for ghostDist in newGhost:
            newghostDist = util.manhattanDistance(newPos, ghostDist)
            if (newghostDist < 2):
                #rather than assigning just return infinite score
                #score = -float('inf')
                return -float('inf')
        return score

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
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

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
    Your minimax agent (question 2)
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        maximum = float("-inf")
        bestAction = Directions.STOP
        actions = gameState.getLegalActions(0);
        return self.findBestAction(gameState, actions, maximum, bestAction)

    def findBestAction(self, gameState, actions, maximum, bestAction):
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            nextVal = self.findVal(nextState, 0, 1)
            if (maximum < nextVal):
                maximum = nextVal
                bestAction = action
        return bestAction

    def findVal(self, gameState, depth, index):
        if (depth == self.depth):
            return self.evaluationFunction(gameState)
        elif (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(index)
        totalAgents = gameState.getNumAgents()
        maximum = float("-inf")
        minimum = float('inf')
        #max-value
        if (index == 0):
            for action in actions:
                newGameState = gameState.generateSuccessor(index, action)
                newVal = self.findVal(newGameState, depth, 1)
                maximum = max(maximum, newVal)
            return maximum
        #min-value
        else:
            for action in actions:
                newGameState = gameState.generateSuccessor(index, action)
                if ((index == totalAgents - 1)):
                    newVal = self.findVal(newGameState, depth + 1, 0)
                else:
                    newVal = self.findVal(newGameState, depth, index + 1)
                minimum = min(minimum, newVal)
            return minimum



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        maximum = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        bestAction = Directions.STOP
        actions = gameState.getLegalActions(0);
        return self.findBestAction(gameState, actions, maximum, bestAction, alpha, beta)

    def findBestAction(self, gameState, actions, maximum, bestAction, alpha, beta):
        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            nextVal = self.findVal(nextState, 0, 1, alpha, beta)
            if (maximum < nextVal):
                maximum = nextVal
                bestAction = action
            alpha = max(alpha, maximum)
        return bestAction

    def findVal(self, gameState, depth, index, alpha, beta):
        if (depth == self.depth):
            return self.evaluationFunction(gameState)
        elif (gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(index)
        totalAgents = gameState.getNumAgents()
        maximum = float("-inf")
        minimum = float('inf')
        #max-value
        if (index == 0):
            for action in actions:
                newGameState = gameState.generateSuccessor(0, action)
                newVal = self.findVal(newGameState, depth, 1, alpha, beta)
                maximum = max(maximum, newVal)
                if (maximum <= beta):
                    #update alpha: max's best option on path to root
                    alpha = max(alpha, maximum)
                else:
                    return maximum
            return maximum
        #min-value
        else:
            for action in actions:
                newGameState = gameState.generateSuccessor(index, action)
                if ((index == totalAgents - 1)):
                    newVal = self.findVal(newGameState, depth + 1, 0, alpha, beta)
                else:
                    newVal = self.findVal(newGameState, depth, index + 1, alpha, beta)
                minimum = min(minimum, newVal)
                if (minimum >= alpha):
                    #update beta: min's best option on path to root
                    beta = min(beta, minimum)
                else:
                    return minimum
            return minimum


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Initialize default values
        action = Directions.STOP
        maxValue = float('-inf')
        
        # Traverse legal moves
        for currAction in gameState.getLegalActions(0):
            currState = gameState.generateSuccessor(0, currAction)
            currValue = self.computeValue(currState, 1, 0)
            if currValue > maxValue:
                action, maxValue = currAction, currValue
        return action 

    def computeValue(self, gameState, agent, currDepth):
        if currDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        value = float('-inf') if not agent else 0

        for currAction in gameState.getLegalActions(agent):
            if not agent:
                value = max(value, self.computeValue(gameState.generateSuccessor(0, currAction), 1, currDepth))
            elif agent == gameState.getNumAgents() - 1:
                value += self.computeValue(gameState.generateSuccessor(agent, currAction), 0, currDepth + 1)
            else:
                value += self.computeValue(gameState.generateSuccessor(agent, currAction), agent + 1, currDepth)
        return value

    # def getAction(self, gameState):
    #     """
    #       Returns the expectimax action using self.depth and self.evaluationFunction
    #       All ghosts should be modeled as choosing uniformly at random from their
    #       legal moves.
    #     """
    #     maxValue = float("-inf")
    #     maxAction = Directions.STOP
    #     for action in gameState.getLegalActions(0):
    #         nextState = gameState.generateSuccessor(0, action)
    #         nextValue = self.getValue(nextState, 0, 1)
    #         if nextValue > maxValue:
    #             maxValue = nextValue
    #             maxAction = action
    #     return maxAction

    # def getValue(self, gameState, currentDepth, agentIndex):
    #     if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
    #         return self.evaluationFunction(gameState)
    #     elif agentIndex == 0:
    #         return self.maxValue(gameState,currentDepth)
    #     else:
    #         return self.avgValue(gameState,currentDepth,agentIndex)

    # def maxValue(self, gameState, currentDepth):
    #     maxValue = float("-inf")
    #     for action in gameState.getLegalActions(0):
    #         maxValue = max(maxValue, self.getValue(gameState.generateSuccessor(0, action), currentDepth, 1))
    #     return maxValue

    # def avgValue(self, gameState, currentDepth, agentIndex):
    #     avgValue = 0
    #     for action in gameState.getLegalActions(agentIndex):
    #         if agentIndex == gameState.getNumAgents()-1:
    #             avgValue = avgValue + self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0)
    #         else:
    #             avgValue = avgValue + self.getValue(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1)
    #     return avgValue


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
