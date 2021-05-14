import turtle
import random
import time
s = turtle.Screen()
s.bgcolor('green')
s.setup(800,800)
s.tracer(0,0)
t = turtle.Turtle()

import copy



size = (800-180)/8


def go_to(x,y):
    t.penup()
    t.goto(x,y)
    t.pendown()

def clear():
    turtle.resetscreen()

def switchPlayer(player):
    return 1 if player ==2 else 2

def drawBoard(n):
    upperCorner = (-400+90,400-90)
    for row in range(8):
        go_to(upperCorner[0],upperCorner[1]-(size*row))
        for col in range(8):
            for sq in range(4):
                t.forward(size)
                t.right(90)
            t.forward(size)
    s.update()




def whichRow(y):
    val = -((y-310)/size)
    if val >=8 or val<0:
        return None
    return int(val) #move 310 down over so that 0th column starts at 0 but goes down negatively

def whichColumn(x):
    val = (x+310)/size
    if val >=8 or val<0:
        return None
    return int(val) #move 350 over so that 0th column starts at 0

def yFromRow(row):
    return -(size*row)+400-90

def xFromColumn(row):
    return (size*row)-400+90

def stampPlayer(row,column, player):
    go_to(xFromColumn(column)+size/2,yFromRow(row)-size/2)
    color = 'white' if player==1 else 'black'
    t.shape('circle')
    t.color(color)
    t.shapesize(2.5,2.5,2.5)
    t.stamp()
    s.update()


def calculateScore(board,player):
    return sum([len([loc for loc in row if loc==player]) for row in board])

def stampMoves(board):
    [stampPlayer(row,col,board[row][col]) for col in range(8) for row in range(8) if board[row][col] != 0]

def updateScore():
    t.color('black')
    go_to(-250,400-45)
    t.write("Player %s Turn" % playerTurn, font=("Arial", 15, "normal"))
    go_to(200,400-45)
    t.write("Player 1: %s, Player 2: %s" % (calculateScore(gameBoard,1),calculateScore(gameBoard,2)), font=("Arial", 15, "normal"))

def updateBoard():
    clear()
    t.hideturtle()
    drawBoard(8)
    stampMoves(gameBoard)
    updateScore()
    drawPossibleMoves(gameBoard,playerTurn)
    s.update()

def initialize():
    global gameBoard
    global playerTurn
    gameBoard = [[0 for y in range(8)] for x in range(8)]
    gameBoard[3][3] = 1
    gameBoard[3][4] = 2
    gameBoard[4][3] = 2
    gameBoard[4][4] = 1
    updateBoard()



def checkListForMove(values,player):
    oppPlayer = switchPlayer(player)
    if player not in values: return False
    values = values[:values.index(player)]
    if len([val for val in values if val != oppPlayer]) > 0 or len(values)==0: return False
    return True

def ValidMove(board,player, row,column):
    directions = [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
    if board[row][column] != 0: return False
    locs = [loc for loc in [board[row+direction[0]][column+direction[1]] for direction in directions if (row+direction[0])in range(8) and (column+direction[1])in range(8)] if loc!=0]
    if len(locs) == 0: return False # check if surrounded by zeros
    options = [ [ board[row+x*direction[0]][column+x*direction[1]] for x in range(1,8) if (row+x*direction[0])in range(8) and (column+x*direction[1])in range(8)] for direction in directions]
    options = [option for option in options if checkListForMove(option,player)]
    if len(options)>0: return True
    else: return False

def findTurnoverPieces(values,valuesLocation, player):
    oppPlayer = switchPlayer(player)
    if player not in values: return []
    end = values.index(player)
    valuesLocation = valuesLocation[:end]
    values = values[:end]
    if len([val for val in values if val != oppPlayer]) > 0 or len(values)==0: return []
    return valuesLocation


def nextBoard(board,player, move):
    board = copy.deepcopy(board)
    row,column = move
    directions = [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
    optionsLocation = [ [ [row+x*direction[0],column+x*direction[1]] for x in range(1,8) if (row+x*direction[0]) in range(8) and (column+x*direction[1]) in range(8)] for direction in directions]
    options = [ [ board[row+x*direction[0]][column+x*direction[1]] for x in range(1,8) if (row+x*direction[0]) in range(8) and (column+x*direction[1]) in range(8)] for direction in directions]
    for x in range(len(directions)):
        for nrow,ncol in findTurnoverPieces(options[x],optionsLocation[x],player): board[nrow][ncol]=player
    board[row][column] = player
    return board


def allMoves(board,player):
    return [[row,col]for row in range(8) for col in range(8) if ValidMove(board,player,row,col) and board[row][col]==0]

def drawCircle(row,column,player):
    go_to(xFromColumn(column)+size/2,yFromRow(row)-size/2-25)
    t.circle(25)


def drawPossibleMoves(board,player):
    moves = allMoves(board,player)
    t.color('black')
    [drawCircle(row,column,player) for row,column in moves]
    s.update()
def gameOver(board,player):
    if len(allMoves(board,player))==0:
        oppPlayer = switchPlayer(player)
        if len(allMoves(board,oppPlayer))==0:
            s.clear()
            t.color('black')
            go_to(-200,100)
            t.write("Game Over", font=("Arial", 100, "normal"))
            go_to(-200,-10)
            t.write("Player 1: %s, Player 2: %s" % (calculateScore(gameBoard,1),calculateScore(gameBoard,2)), font=("Arial", 15, "normal"))

        return "switch"


def makeMove(x, y):
    global gameBoard
    global playerTurn
    col = whichColumn(x)
    row = whichRow(y)
    if row == None or col== None: return
    if ValidMove(gameBoard,playerTurn,row,col):
        gameBoard = nextBoard(gameBoard,playerTurn,[row,col])
        playerTurn = switchPlayer(playerTurn)
        updateBoard()
        if gameOver(gameBoard,playerTurn) == "switch":
            playerTurn = switchPlayer(playerTurn)
            updateBoard()
            return
        if playingAutomated and playerTurn==2:
            playMoveAutomated()
        print(gameBoard)

def playMoveAutomated():
    global gameBoard
    global playerTurn
    gameBoard = findAutomatedMove(gameBoard,playerTurn)
    playerTurn = switchPlayer(playerTurn)
    updateBoard()
    if gameOver(gameBoard, playerTurn) == "switch":
        playerTurn = switchPlayer(playerTurn)
        playAutomated()

def findAutomatedMove(board, player):
    alpha = -1000
    beta = 1000
    moves = allMoves(board,player)
    vals = [miniMax(3,switchPlayer(player),nextBoard(board,player,move),alpha,beta) for move in moves]
    #3 is 2-1-2-1-2
    move = moves[vals.index(min(vals))]
    return nextBoard(board,player,move)

def evaluateBoardMobility(board):
    maxPlayerMoves = len(allMoves(board,1))
    minPlayerMoves = len(allMoves(board,2))
    if ( maxPlayerMoves + minPlayerMoves != 0):
        return 100* (maxPlayerMoves - minPlayerMoves)/(maxPlayerMoves + minPlayerMoves)
    else:
    	return 0
def isCorner(row,colum):
    return (row==0 or row==7) and (column==0 or column==7)

def cornerPieces(board,player):
    corners = [[0,0],[0,7],[7,0],[7,7]]
    return len([True for row, col in corners if board[row][col]==player])
def wallPieces(board, player):
    sides1 = sum([len([True for row in range(1,7) if board[row][col]==player]) for col in [0,7]])
    sides2 = sum([len([True for col in range(1,7) if board[row][col]==player]) for row in [0,7]])
    return sides1 + sides2
def evaluateBoard2(board):
    player1 = 10*wallPieces(board,1)+50*cornerPieces(board,1)+calculateScore(board,1)
    player2 = 10*wallPieces(board,2)+50*cornerPieces(board,2)+calculateScore(board,2)
    return player1-player2 #+ evaluateBoardMobility(board)

def evaluateBoard(board):
    return calculateScore(board,1) - calculateScore(board,2)

def miniMax(depth, player,board, alpha, beta):
    if depth == 0:
        return evaluateBoard2(board)
    if player == 1: # maximize
        maxScore = -1000
        moves = allMoves(board,player)
        if len(moves) == 0: return miniMax(depth-1,switchPlayer(player),board,alpha,beta)
        for move in moves:
            score = miniMax(depth-1,switchPlayer(player),nextBoard(board, player,move), alpha, beta)
            maxScore = max(score, maxScore)
            alpha = max(score, alpha)
            if beta <= alpha:
                break
        return maxScore
    if player == 2: # minimize
        minScore = 1000
        moves = allMoves(board,player)
        if len(moves) == 0: return miniMax(depth-1,switchPlayer(player),board,alpha,beta)
        for move in moves:
            score = miniMax(depth-1,switchPlayer(player),nextBoard(board, player,move),alpha,beta)
            minScore = min(score, minScore)
            beta = min(score, beta)
            if beta <= alpha:
                break
        return minScore




playerTurn = 1
playingAutomated = True
initialize()

#gameBoard = [[2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 0, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 0], [2, 1, 2, 2, 2, 2, 2, 2], [2, 2, 1, 2, 2, 2, 2, 2], [0, 2, 2, 1, 1, 1, 2, 2], [2, 2, 2, 2, 2, 2, 0, 2]]

#updateBoard()
turtle.onscreenclick(makeMove)

input("end? ")
