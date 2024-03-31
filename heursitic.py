import copy

class node():
    '''
        Initalizes node
        
        Input:
        cBoard (list) - current board state
        m (int) - how many you need to get in a row to win
        player (string) - If that player would place down a "X" or an "O
        depth (int) - Depth of the node (Defaults to 0)
        move ((int,int)) - The (row,column) of the move made 
        
        Setup:
        n (int) - width/height of the board
        value (int) - the heuristic value of the board 
        child (list[Node]) - a list of all possible moves that can be done
        new (bool) - Determines if we need to attempt to populate the child list
    '''
    def __init__(self, cBoard, m,player,depth = 0, move = None):
        self.cBoard = cBoard 
        self.m = m
        self.player = player
        self.depth = depth
        self.n = len(self.cBoard)
        self.value = None
        self.child = []
        self.new = True
        self.move = move
    
    def populate(self):
        '''
            Populates the child nodes of the board should only run once per node
            Input:
                parent(Node) - the current node that you want the children of
            
            Returns:
                possibleMoves (Node) - List of all possible moves that can be made
        '''
        possibleMoves = []
        for i in range (self.n):
            for j in range (self.n):
                if self.cBoard[i][j] == '_' or self.cBoard[i][j] == '-':
                    childBoard = copy.deepcopy(self.cBoard)
                    childBoard[i][j] = self.player
                    if(self.player == 'X'):
                        child = node(childBoard,3,'O',self.depth +1,(i,j))
                    else:
                        child = node(childBoard,3,'X',self.depth+1,(i,j))
                    possibleMoves.append(child)
        self.child = possibleMoves
        
#assuming that cNode has cBoard, n, m


def is_winner(cNode, mark):
    '''
        Checks to see if there is a winner
        
        Input:
            cNode (node) - the current node
            mark (string) - either X or O

        Returns:
            bool - Either True if there is a winner or False if there isn't one
    '''
    def check_line(line):
        '''
            Helper function to check if there is a win of size m (borrowing from node)
            
            Input:
                line (list) - the line to check if there is a win
            
            Returns:
                bool - Either True (Yes) False (No)
        '''
        count = 0
        for cell in line:
            if cell == mark:
                count += 1
                if count == cNode.m:
                    return True
            else: count = 0
        return False
    
    def check_row():
        '''
        Check in a row if there is a win
        
        Returns:
            bool - Either True (Yes) False (No)
        '''
        for row in cNode.cBoard:
            if check_line(row):
                return True
        return False
    
    def check_col():
        '''
        Check in a column if there is a win
        
        Returns:
            bool - Either True (Yes) False (No)
        '''
        transposed_matrix = [list(column) for column in zip(*cNode.cBoard)]
        for row in transposed_matrix:
            if check_line(row): 
                return True
        return False
    
    def check_diag():
        '''
        Check in a diagonal if there is a win
        
        Returns:
            bool - Either True (Yes) False (No)
        '''
        diag = []
        for i in range(cNode.n):
            for j in range(cNode.n):
                if i == j:
                    diag.append(cNode.cBoard[i][j])
        return check_line(diag)
        
    def check_antiDiag():
        '''
        Check in other diagonals if there is a win
        
        Returns:
            bool - Either True (Yes) False (No)
        '''
        diag = []
        for i, j in zip(range(cNode.n), reversed(range(cNode.n))):
            diag.append(cNode.cBoard[i][j])
        return check_line(diag)

    is_row_winner = check_row()
    is_col_winner = check_col()
    is_diag_winner = check_diag()
    is_antiDiag_winner = check_antiDiag()

    if is_row_winner or is_col_winner or is_diag_winner or is_antiDiag_winner:
        return True
    else:
        return False




def cutoffs(cNode, opponent_mark):
    def count_in_line(line):
        cutoff_cnt = 0
        count = 0
        for cell in line:
            if cell == opponent_mark:
                count += 1
                if count == cNode.m - 1:
                    cutoff_cnt += 1
            else: count = 0
        return cutoff_cnt
    
    def count_row():
        cnt = 0
        for row in cNode.cBoard:
            cnt += count_in_line(row)
        return cnt
    
    def count_col():
        cnt = 0
        transposed_matrix = [list(column) for column in zip(*cNode.cBoard)]
        for row in transposed_matrix:
            cnt += count_in_line(row)
        return cnt
    
    def check_diag():
        diag = []
        for i in range(cNode.n):
            for j in range(cNode.n):
                if i == j:
                    diag.append(cNode.cBoard[i][j])
        return count_in_line(diag)
        
    def check_antiDiag():
        diag = []
        for i, j in zip(range(cNode.n), reversed(range(cNode.n))):
            diag.append(cNode.cBoard[i][j])
        return count_in_line(diag)

    return (check_antiDiag() +    check_diag() + count_col() + count_row())



def heuristic(cNode, agent_mark):
    '''
    Calculates the heurisitic value of a node

    Input:
        cNode (node) - current node that we are calculating
        agent_mark (string) - if node is drawing a O or a X
    '''
    if agent_mark == "O": # Determines that if agent is drawing one the opponent should draw the other
        opponent_mark = "X"
    else:
        opponent_mark = "O"
    
    h = 0
    cutoffs_cnt = cutoffs(cNode, opponent_mark)
    if is_winner(cNode, agent_mark):
        h += (10*cNode.n - cNode.depth - cutoffs_cnt)
    elif is_winner(cNode, opponent_mark):
        h -= (10*cNode.n - cNode.depth - cutoffs_cnt)
    return h

# board = [['X', 'X', 'O'],
#         ['O', 'X', 'O'],
#         ['_', 'X', '_']]

# node1 = node(board, 3)

# print(heuristic(node1, 2, 'O'))