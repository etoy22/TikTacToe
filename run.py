import http.client
from minimax import minimax,secondLastMove
from heursitic import node
import json

'''
    CONSTS
    url - the url to connect to
    headers - the header that is needed to connect to the games contains the api
    TEAM - Our team id
'''
conn = http.client.HTTPSConnection("www.notexponential.com")
TEAM = 1424
headers = {
  'x-api-key': 'f1d4e5463f445fa81aae',
  'userid': '3626',
  'Content-Type': 'application/x-www-form-urlencoded'
}

'''
    Global Varriable

    opponent (int) - The opponents team id
    n (int) - Voard Size of the game
    m (int) - how many you need to get in a row on the board
    gameId (int) - recieved from the api and gives us the id of the game
    first (bool) - says if we are going first or second
'''
opponent = -1
n = 12
gameId = -1





def startGame():
    '''
        Function to start the TicTacToe game
    '''
    global n
    global m
    global gameId
    global headers
    global gameId
    first = False
    create = YesNo()
    if (create):
    # Clarifying questions about the game
        print("Whats the opponent id?")
        opponent = validNumber()
        
        print("Are you going first or second?")
        first = YesNo()
        
        print("Defaults are Board Size of 12 and 6 would you like the defaults")
        default = YesNo()
        if (not(default)):
            print("Whats the board size")
            n = validNumber()
            print("Whats the amount in a row to win")
            m = validNumber()

    # Creation of the game
        if (first):
            payload = f'type=game&teamId1={TEAM}&teamId2={opponent}&gameType=TTT&boardSize={n}&target={m}'
        else:
            payload = f'type=game&teamId1={opponent}&teamId2={TEAM}&gameType=TTT&boardSize={n}&target={m}'
        conn.request("POST", "/aip2pgaming/api/index.php", payload, headers)
        res = conn.getresponse()
        data = res.read()
        board = []
        for i in range(n):
            board.append(["-"] * n)
    else:
        print("Input the Game ID")
        gameId = validNumber()

        payload = ''
        conn.request("GET", f"/aip2pgaming/api/index.php?type=boardString&gameId={gameId}", payload, headers)

        res = conn.getresponse()
        data = res.read()
        input_string = data.decode('utf-8')
        translate = json.loads(input_string)

        # Extract the grid pattern
        grid_pattern = translate["output"]

        m = translate["target"]
        board = [] # Possible new
        for row in grid_pattern.split("\n"):
            board.append(list(row))
        board.pop()
    
    
    
    if (first):
        goingFirst(board)
    else:
        goingSecond(board)
           
def depthPenality():
    '''
    Determines if the depth penaty comes into play which is any game where n is larger than 4
    '''
    global n
    global m
    depth = m * 2
    if (n > 4):
        return depth
    return -1

def goingFirst(board):
    '''
        Calculates the first move of the game

        Input:
            board (list) - current board state
    '''
    global headers
    global m
    gameId = 4786
    depth = depthPenality()
    current = node(board,m,'O')
    _, current = (minimax(current,float('-inf'),float('inf'),True,'O',depth))
    payload = f'type=move&gameId={gameId}&teamId={TEAM}&move={current.move[0]}%2C{current.move[1]}'
    conn.request("POST", "/aip2pgaming/api/index.php", payload, headers)
    res = conn.getresponse()
    unified(board,'O','X',current)

def goingSecond(board):
    '''
        Going second attempts to calculate what the opponent might do and starts calculating in advance

        Input:
            board (list) - current board state
    '''
    global headers
    global m
    conn = http.client.HTTPSConnection("www.notexponential.com")
    depth = depthPenality()
    count = 0
    for row in board:
        count += row.count('-')
    if len(board)*len(board) == count: # This occurs when you are waiting for the next move from the opposition
        current = node(board,m,'O')
        minimax(current,float('-inf'),float('inf'),False,'X')
    else:
        current = node(board,m,'X')
        val, current = (minimax(current,float('-inf'),float('inf'),True,'X',depth))
        payload = f'type=move&gameId={gameId}&teamId={TEAM}&move={current.move[0]}%2C{current.move[1]}'
        board = current.cBoard
        print("Sending next move")
        conn.request("POST", f"/aip2pgaming/api/index.php?type=boardString&gameId={gameId}", payload, headers)
        res = conn.getresponse()
        print(res)
        
    unified(board,'X','O',current)

def unified(oldBoard,player,oString,current):
    '''
        After either going first or second it doesn't really matter as much as long as some information is know

        Input:
            oldboard (list[["-"]*n]*n) - n by n size board that has been affected by goingFirst() or goingSecond()
            player (string) - Whether the program is X or O
            oString (string) - Whether the opponent is X or O 
            current (Node) - current node thats being looked at
    '''
    global m
    global n
    headers = {
        'x-api-key': 'f1d4e5463f445fa81aae',
        'userid': '3626',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    board = oldBoard
    depth = depthPenality()
    firstMax = False
    counter = 0
    while len(current.child) != 0:
        depth += 1
        # Waits for the other players move
        while(True): # Waiting on a reply from the other user
            payload = ''
            conn = http.client.HTTPSConnection("www.notexponential.com")
            conn.request("GET", f"/aip2pgaming/api/index.php?type=boardString&gameId={gameId}", payload, headers)

            res = conn.getresponse()
            data = res.read()
            input_string = data.decode('utf-8')
            translate = json.loads(input_string)

            # Extract the grid pattern
            grid_pattern = translate["output"]

            newBoard = [] # Possible new
            for row in grid_pattern.split("\n"):
                newBoard.append(list(row))
            newBoard.pop()
            
            if (listSame(newBoard,board)): # Checks if the player has made a new move
                found = False 
                for child in current.child:
                    if child.cBoard == newBoard:
                        found = True
                        break
                if (found):
                    current = child
                else:
                    current = node(newBoard,m,oString) #Exists if somehow the program didn't see the move should never appear
                break # Break out of the while (true) loop
        # TODO: Not sure if we want this remove??? 
        '''
            elif depth+counter == n*n:
                if (firstMax):
                    firstMax = False
                    print("All nodes have been calculated")
                pass
            else: # Calculates next depth while waiting 
                counter += 1
                (minimax(current,float('-inf'),float('inf'),False,'X',depth+counter))

        counter = 0
        firstMax = True
        '''
        # Responding to move from opponent
        _, current = (minimax(current,float('-inf'),float('inf'),True,player,depth))
        payload = f'type=move&gameId={gameId}&teamId={TEAM}&move={current.move[0]}%2C{current.move[1]}'

        print("Sending next move")
        conn = http.client.HTTPSConnection("www.notexponential.com")
        conn.request("POST", "/aip2pgaming/api/index.php", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        if(secondLastMove(current.cBoard)): #Checks if its the last move made by this program
            break
    print("GAME OVER")

def listSame(first, second):
    '''
        Says if the lists are the same

        Input:
        first (list) - the first list
        second (list) - second list

        Return:
            bool - True if they are the same False if not
    '''
    if len(first) != len(second):
        return False
    
    for i in range(len(first)):
        if len(first[i]) != len(second[i]):
            return False
        
        for j in range(len(first[i])):
            if first[i][j] != second[i][j]:
                return False
    
    return True

def YesNo():
    '''
        A function that forces yes or no response

        Returns:
            bool - True (Yes), False(No)
    '''
    while True:
        default = input("Please enter a yes or no: ").strip().lower()
        if default in ['yes', 'y']:
            return True
        elif default in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            

def validNumber():
    '''
        A function that forces yes or no response

        Returns:
            int - a valid integer
    '''      
    while True:
        try:
            number = int(input("Please enter a valid number: "))
            return number
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            
if __name__ == "__main__":
    startGame()