#Winning positions
WINS = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def newGame(): #Creates a new game
    output = {}
    output["x"] = None
    output["o"] = None
    output["users"] = set()
    output["board"] = "         "
    output["end"] = False
    return output

def addUser(game, user): #Adds user to a game
    game["users"].add(user)
    if game["x"] == None:
        game["x"] = user
    elif game["o"] == None:
        game["o"] = user

def removeUser(game, user): #Removes user from a game, returns a winner if the leaver was a participant
    game["users"].remove(user)
    if game["o"] == user:
        game["o"] = None
        return 'x'
    elif game["x"] == user:
        game["x"] = None
        return 'o'
    return None

def makeMove(game, pos, mover): #Makes a move and updates the game
    if game['board'][pos] != ' ':
        return
    else:
        game['board'] = game['board'][0:pos] + mover + game['board'][pos + 1:]

def checkStatus(game): #Returns the winner, draw, or None if the game is ongoing
    layout = game['board']
    for awin in WINS:
        if layout[awin[0]] != ' ' and layout[awin[0]] == layout[awin[1]] == layout[awin[2]]:
                return 'x' if layout[awin[0]] == 'x' else 'o'
        elif layout.count(' ') == 0:
            return 'Draw'
    return None
