import requests
from minimax import minimax,secondLastMove
from heursitic import node

'''
    CONSTS
    URL - the url to connect to
    HEADERS - the header that is needed to connect to the games contains the api
    TEAM - Our team id
'''
URL = "https://www.notexponential.com/aip2pgaming/api/index.php"
HEADERS = {
  'x-api-key': ' f1d4e5463f445fa81aae ',
  'userid': '3626',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Cookie': 'qa_key=02ujxhw4l9kefv9gxzdbd0m889fv2rxk'
}
TEAM = 1424


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
m = 6
gameId = -1
first = True

def startGame():
    '''
        Function to start the TicTacToe game
    '''
    
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
    
    response = requests.request("POST", URL, headers=HEADERS, data=payload) 
    if response.code == "OK": #Double checks that it went through correctly
        gameId = response.gameId
    
    board = []
    for i in range(n):
        board.append(["-"] * n)
    
    if (first):
        goingFirst(board)
    else:
        goingSecond(board)
           
    
def goingFirst(board):
    '''
        Calculates the first move of the game
    '''
    current = node(board,m,'X')
    _, current = (minimax(current,float('-inf'),float('inf'),False,'X'))
    board =  current.cBoard
    makeMove = f'type=move&gameId={gameId}&teamId={TEAM}&move={current.move[0]}%2C{current.move[1]}'
    response = requests.request("POST", URL, headers=HEADERS, data=makeMove)
    if response.code != "OK":
        raise ValueError("ERROR on first submit move")
    unified(board,'X','O')
    
def goingSecond(board):
    '''
        Going second attempts to calculate what the opponent might do and starts calculating in advance
    '''
    current = node(board,m,'X')
    minimax(current,float('-inf'),float('inf'),False,'O')
    unified(board,'O', 'X')


def unified(oldBoard,player,oString):
    '''
        After either going first or second it doesn't really matter as much as long as some information is know

        Input:
            oldboard (list[["-"]*n]*n) - n by n size board that has been affected by goingFirst() or goingSecond()
            player (string) - Whether the program is X or O
            oString (string) - Whether the opponent is X or O 
    '''
    board = oldBoard
    while len(current.child) != 0:
        
        # Waits for the other players move
        while(True): # Waiting on a reply from the other user
            getBoard = f'type=boardString&gameId={gameId}' # Payload to get board
            response = requests.request("GET", URL, headers=HEADERS, data=getBoard) # Gets current board
            newboard = [] # Possible new
            for row in response.output.split('\n'):
                newboard.append(list(row))
            
            if (newboard != board): # Checks if the player has made a new move
                found = False 
                for child in current.child:
                    if child.cBoard == newboard:
                        found = True
                        break
                if (found):
                    current = child
                else:
                    current = node(newboard,m,oString) #Exists if somehow the program didn't see the move should never appear
                break # Break out of the while (true) loop 
    
        # Responding to move from opponent
        _, current = (minimax(current,float('-inf'),float('inf'),True,player))
        makeMove = f'type=move&gameId={gameId}&teamId={TEAM}&move={current.move[0]}%2C{current.move[1]}'
        response = requests.request("POST", URL, headers=HEADERS, data=makeMove)
        if(secondLastMove(current.cBoard)): #Checks if its the last move made by this program
            break
    print("GAME OVER")



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
            opponent_id = int(input("Please enter a valid number: "))
            return opponent_id
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            
if __name__ == "__main__":
    startGame()