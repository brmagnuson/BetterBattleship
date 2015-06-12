# This program lets a user play Battleship against the computer. The computer either plays randomly or intelligently.

from __future__ import print_function
import random
import sys
import play_wav
import os


def getInt(prompt):
    """This function gets an integer from the user."""
    while True:
        try:
            number = int(input(prompt))
            return number
        except ValueError:
            pass


def getPosInt(prompt):
    """This function gets a positive integer from the user."""
    invalid = True
    while invalid:
        number = getInt(prompt)
        if number > 0:
            invalid = False
    return number


def getAI():
    """This function allows the user to choose the AI to play against."""
    promptAI = ('Choose your AI.\n'
                '1. Random\n'
                '2. Smart\n'
                '3. Cheater\n'
                ' Your choice: ')
    invalid = True
    while invalid:
        choice = getInt(promptAI)
        if 1 <= choice <= 3:
            invalid = False
    return choice


def createBoard(shipCoordinates, boardWidth, boardHeight):
    """This functions uses the board dimensions and the user's input to place the ships."""

    board = []

    # Fill board with * symbol.
    curRow = 0
    while curRow < boardHeight:
        currentRowList = []
        curColumn = 0
        while curColumn < boardWidth:
            currentRowList.append('*')
            curColumn += 1
        board.append(currentRowList)
        curRow += 1

    # Replace * with ship symbol when appropriate
    for shipSymbol, coordinates in shipCoordinates.items():
        for pair in coordinates:
            row, column = pair
            board[row][column] = shipSymbol

    return board


def getAIShipDimensions(userShipCoordinates):
    """This function gets the symbols and dimensions for the games' ships"""
    shipDimensions = {}
    for symbol, coordinates in userShipCoordinates.items():
        shipDimensions[symbol] = len(coordinates)
    return shipDimensions


def getAIShipCoordinates(aiShips, maximumColumnIndex, maximumRowIndex):
    """This creates the AI board based on the given ships' dimensions"""

    boardWidth = maximumColumnIndex + 1
    boardHeight = maximumRowIndex + 1

    # Get sorted order of ships
    shipSymbolList = list(aiShips.keys())
    shipSymbolList.sort()

    aiShipCoordsList = []
    aiShipDict = {}
    for aiShipSymbol in shipSymbolList:

        length = aiShips[aiShipSymbol]

        # Create horizontal ship, incrementing the column index, or vertical ship, incrementing the row
        invalid = True
        while invalid:

            direction = random.choice(['vert', 'horz'])

            if direction == 'horz':
                lastPossStartRow = maximumRowIndex
                lastPossStartColumn = boardWidth - length
            else:
                lastPossStartRow = boardHeight - length
                lastPossStartColumn = maximumColumnIndex

            tryNewCoordinates = False
            currentAIShipCords = []
            row = random.randint(0, lastPossStartRow)
            column = random.randint(0, lastPossStartColumn)

            for segment in range(length):

                # If coordinate overlaps with another ship, restart while loop
                coordinate = (row, column)
                if coordinate in aiShipCoordsList:
                    tryNewCoordinates = True
                    break
                else:
                    currentAIShipCords.append(coordinate)

                # Increment column
                if direction == 'horz':
                    column += 1
                else:
                    row += 1

            # If either of the above conditions are invalidated, restart the loop. Otherwise, the whole ship is valid
            if tryNewCoordinates:
                continue
            else:
                invalid = False

        # Add valid ship to coordinates list and ship dictionary and announce placement
        aiShipCoordsList += currentAIShipCords
        aiShipDict[aiShipSymbol] = currentAIShipCords

    print('AI ships placed.')

    return aiShipDict


def displayUserBoard(board):
    """This displays the current state of the user's board"""
    print('My Board')
    numRows = len(board)
    numColumns = len(board[0])

    # Columns
    print('  ', end='')
    for columnIndex in range(numColumns):
        print(str(columnIndex) + ' ', end='')
    print()

    # Rows
    for rowIndex, rowValues in enumerate(board):
        print(rowIndex, end=' ')
        for cell in rowValues:
            print(cell + ' ', end='')
        print()

    # Finish with a space
    print()


def displayAIBoard(board):
    """This displays the current known state of the AI board"""
    print('Scanning Board')
    numRows = len(board)
    numColumns = len(board[0])

    # Columns
    print('  ', end='')
    for columnIndex in range(numColumns):
        print(str(columnIndex) + ' ', end='')
    print()

    # Rows
    for rowIndex, rowValues in enumerate(board):
        print(rowIndex, end=' ')
        for cell in rowValues:
            if cell in 'xXoO*':
                print(cell + ' ', end='')
            else:
                print('* ', end='')
        print()

    # Finish with a space
    print()


def getWinner(usersBoard, aisBoard):
    """This function tests for a winner. If neither board has been fully guessed, this function returns None."""

    winner = None

    notUserVictory = False
    for row in usersBoard:
        for cell in row:

            # If the user's board contains an unsunken ship cell, break out of both loops
            if not(cell in 'xXoO*'):
                notUserVictory = True
                break

        if notUserVictory:
            break
    else:
        winner = 'AI'

    notAIVictory = False
    for row in aisBoard:
        for cell in row:

            # If the user's board contains an unsunken ship cell, break out of both loops
            if not(cell in 'xXoO*'):
                notAIVictory = True
                break

        if notAIVictory:
            break
    else:
        winner = 'user'

    return winner


def getUserMove(previousUserMoves, maximumColumnIndex, maximumRowIndex):
    """This function gets a valid coordinate for a user move."""

    invalid = True
    while invalid:

        userInput = raw_input('Enter row and column to fire on separated by a space: ').strip()

        userInput = userInput.split()
        if len(userInput) != 2:
            continue

        row, column = userInput
        if not row.isdigit():
            continue
        else:
            row = int(row)
        if not column.isdigit():
            continue
        else:
            column = int(column)

        if row > maximumRowIndex:
            continue
        if column > maximumColumnIndex:
            continue

        coordinate = (row, column)
        if coordinate in previousUserMoves:
            continue
        else:
            invalid = False

    return coordinate


def playMove(board, coordinate, turn):

    row, column = coordinate

    if board[row][column] in 'xXoO*':

        outcome = 'miss'
        print('Miss!')
        play_wav.Sound().playFile('miss.wav')
        if turn == 0:
            os.system('say You missed.')
        else:
            os.system('say I missed.')
        board[row][column] = 'O'

    else:

        outcome = 'hit'
        cellValue = board[row][column]
        board[row][column] = 'X'
        liveShip = False
        inRow = False

        for r in board:
            for c in r:
                if c == cellValue:
                    liveShip = True
                    inRow = True
                    break
            if inRow:
                break

        if liveShip:
            print('Hit!')
            play_wav.Sound().playFile('hit.wav')
            if turn == 0:
                os.system('say You hit me.')
            else:
                os.system('say I hit you.')
        else:
            if turn == 0:
                print('You sunk my %s ship.' % cellValue)
            else:
                print('I sunk your %s ship.' % cellValue)
            play_wav.Sound().playFile('sunk.wav')
            if turn == 0:
                os.system('say -v "Bubbles" "You sunk my %s ship."' % cellValue)
            else:
                os.system('say I sunk your %s ship.' % cellValue)

    return outcome

def generateAllPossibleMoves(boardHeight, boardWidth):
    wholeBoard = []
    for row in range(boardHeight):
        for column in range(boardWidth):
            coordinate = (row, column)
            wholeBoard.append(coordinate)
    return wholeBoard


def getRandomMove(previousAIMoves, openMoves):
    move = random.choice(openMoves)
    return move


def getCheaterMove(cheaterMoveList):
    move = cheaterMoveList[0]
    return move


def getDestroyMoves(lastMove, openMoves, currentDestroyMoveList):
    # If last move was a hit, get moves around previous aiMove.
    row, column = lastMove
    above = (row - 1, column)
    below = (row + 1, column)
    left = (row, column - 1)
    right = (row, column + 1)
    potentialDestroyMoves = [above, below, left, right]

    validDestroyMoves = []
    for move in potentialDestroyMoves:
        # Skip potential moves not in bounds or that have already been guessed.
        if not (move in openMoves):
            continue
        # Skip moves that are already in the destroy move list.
        if move in currentDestroyMoveList:
            continue
        validDestroyMoves.append(move)

    return validDestroyMoves


############
# SETUP INFO
############

# Board dimensions
width = getPosInt('Enter the width of the board: ')
maxColIndex = width - 1
height = getPosInt('Enter the height of the board: ')
maxRowIndex = height - 1

# Import user ship placements
filepath = raw_input('Enter the name of the file containing your ship placements: ').strip()
userShipPlacements = []
with open(filepath) as userShipFile:
    for ship in userShipFile:
        (symbol, row1, column1, row2, column2) = ship.split()
        placement = {'Symbol': symbol, 'R1': int(row1), 'C1': int(column1), 'R2': int(row2), 'C2': int(column2)}
        userShipPlacements.append(placement)

# Choose AI
aiMode = getAI()

# Make sure ship placements are valid. If invalid, terminate the program.
symbolList = []
allUserCoordsList = []
userShipCoordsDict = {}
for ship in userShipPlacements:

    # Can't use x, X, o, O, or * as ship symbols
    if ship['Symbol'] in 'xXoO*':
        print('Error: invalid symbol')
        sys.exit(0)

    # Can't use the same symbols for different ships
    if ship['Symbol'] in symbolList:
        print('Error symbol %s is already in use. Terminating game' % ship['Symbol'])
        sys.exit(0)
    else:
        symbolList.append(ship['Symbol'])

    # All of ships must be on board (rows between 0 and height, columns between 0 and width)
    if not ((0 <= ship['R1'] <= maxRowIndex) and (0 <= ship['R2'] <= maxRowIndex)):
        print('Error %s is placed outside of the board. Terminating game.' % ship['Symbol'])
        sys.exit(0)
    if not ((0 <= ship['C1'] <= maxColIndex) and (0 <= ship['C2'] <= maxColIndex)):
        print('Error %s is placed outside of the board. Terminating game.' % ship['Symbol'])
        sys.exit(0)

    # The ships can't be diagonal: either the two row numbers or the two column numbers must be equal.
    if not ((ship['R1'] == ship['R2']) or (ship['C1'] == ship['C2'])):
        print('Ships cannot be placed diagonally. Terminating game.')
        sys.exit(0)

    # The ships can't be placed on top of each other
    maxRow = max(ship['R1'], ship['R2'])
    minRow = min(ship['R1'], ship['R2'])
    maxColumn = max(ship['C1'], ship['C2'])
    minColumn = min(ship['C1'], ship['C2'])

    currentShipCoordinatesList = []
    currentRow = minRow
    while currentRow <= maxRow:
        currentColumn = minColumn
        while currentColumn <= maxColumn:

            coordinatePair = (currentRow, currentColumn)
            if coordinatePair in allUserCoordsList:
                print('There is already a ship at location %d, %d. Terminating game.' % (currentRow, currentColumn))
                sys.exit(0)
            else:
                allUserCoordsList.append(coordinatePair)
                currentShipCoordinatesList.append(coordinatePair)

            currentColumn += 1
        currentRow += 1

    userShipCoordsDict[ship['Symbol']] = currentShipCoordinatesList

#############
# SET UP GAME
#############

# Construct user board
userBoard = createBoard(userShipCoordsDict, width, height)

# Construct AI board
aiShipDimensions = getAIShipDimensions(userShipCoordsDict)
aiShipCoordsDict = getAIShipCoordinates(aiShipDimensions, maxColIndex, maxRowIndex)
aiBoard = createBoard(aiShipCoordsDict, width, height)

# Get turn
turn = random.randint(0, 1)

###########
# PLAY GAME
###########

userMoves = []
aiMoves = []
openAIMoves = generateAllPossibleMoves(height, width)

destroyMoves = []

orderedCheaterMoves = []
for coordPair in openAIMoves:
    if coordPair in allUserCoordsList:
        orderedCheaterMoves.append(coordPair)

winner = None
huntMode = True
lastAIMove = 'miss'

while winner is None:

    # Gameplay. User's turn is 0, AI's turn is 1.
    if turn == 0:

        # Display current board state
        displayAIBoard(aiBoard)
        displayUserBoard(userBoard)

        # Get valid move for the user
        userMove = getUserMove(userMoves, maxColIndex, maxRowIndex)

        # Play the move & update AI's board, announcing success/failure and a sinking if this occurs
        userOutcome = playMove(aiBoard, userMove, turn)

        # Update move list
        userMoves.append(userMove)

    else:

        # Random mode
        if aiMode == 1:
            aiMove = getRandomMove(aiMoves, openAIMoves)

        # Smarter mode
        elif aiMode == 2:
            if huntMode:
                aiMove = getRandomMove(aiMoves, openAIMoves)
            else:

                if aiOutcome == 'hit':

                    # Get moves around previous aiMove that are inside the bounds, that haven't
                    # already been guessed, and that aren't already in the destroy move list.
                    newDestroyMoves = getDestroyMoves(aiMove, openAIMoves, destroyMoves)

                    # Add to hunter moves
                    destroyMoves += newDestroyMoves

                # Get first move from hunter moves list, as long as there are available moves. Otherwise, random move.
                if len(destroyMoves) > 0:
                    aiMove = destroyMoves.pop(0)
                else:
                    aiMove = getRandomMove(aiMoves, openAIMoves)

        # Cheater mode
        else:
            aiMove = getCheaterMove(orderedCheaterMoves)
            orderedCheaterMoves.pop(0)

        # Play the move & update AI's board, announcing success/failure and a sinking if this occurs
        aiRow, aiColumn = aiMove
        print('The AI fires at location (%d, %d)' % (aiRow, aiColumn))
        aiOutcome = playMove(userBoard, aiMove, turn)

        if aiOutcome == 'hit' or len(destroyMoves) > 0:
            huntMode = False
        else:
            huntMode = True

        # Update move lists
        aiMoves.append(aiMove)
        openAIMoves.remove(aiMove)

    # Change turns
    turn = (turn + 1) % 2
    winner = getWinner(userBoard, aiBoard)

# Print final board status
displayAIBoard(aiBoard)
displayUserBoard(userBoard)

# Declare winner
if winner == 'user':
    print('You win!')
    play_wav.Sound().playFile('victory.wav')
    os.system('say Victory is yours. I surrender my sword')
else:
    print('The AI wins.')
    play_wav.Sound().playFile('loss.wav')
    os.system('say I win')