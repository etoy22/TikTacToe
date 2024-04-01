import copy

from heursitic import heuristic,node 

def custom_sort(x):
    '''
    Custom sort so that we look at lost states last and win states first
    '''
    if x is None:
        return 0
    else:
        return -x

def minimax(cNode, alpha, beta, maxBool, player,depth=-1):
    '''
        Gets the minimax of the current branch
        Input:
            cNode (node) - current node that is being looked at
            alpha (int) - the alpha value for alpha beta prunning
            beta (int) - the beta value for alpha beta prunning
            maxBool (bool) - just says True if maximizing or False if minimizing
            player (string) - says if the player is X or O
        Returns:
            value (int) - This is the max or min value depending on what was being optimized
            chosen_node (node) - This returns the node that was chosen in the path used too say the next move
    '''
    if depth != -1: # Introduced node depth because we may want to have that exist especially as we get to the huge boards
        if cNode.depth >= depth:
            cNode.value = heuristic(cNode, player)
            return cNode.value, cNode
    
    if cNode.new: # This part only runs if its the first time the node has been looked at
        cNode.new = False
        cNode.value = heuristic(cNode, player) # Determines if its a win state 
        if cNode.value == 0: # Because its not a win state we populate the child nodes 
            cNode.populate()

    if len(cNode.child) == 0: # This catches any win states or tie states
        return cNode.value, cNode  


    if maxBool: # Checks for maximizing for value
        max_val = float('-inf')
        chosen_node = None
        for children in cNode.child:
            val, _ = minimax(children, alpha, beta, False, player,depth)
            if val > max_val: 
                max_val = val
                chosen_node = children  
            alpha = max(alpha, max_val)
            if beta <= alpha:
                break
        sorted_children = sorted(cNode.child, key=lambda x: custom_sort(x.value), reverse=True) # Sort in descending order for maximizing minimax on subsequent views 
        return max_val, chosen_node  
    else: # Checks for minimizing of value
        min_val = float('inf')
        chosen_node = None  
        for children in cNode.child:
            val, _ = minimax(children, alpha, beta, True, player,depth)
            if val < min_val:
                min_val = val
                chosen_node = children  
            beta = min(beta, min_val)
            if beta <= alpha:
                break
        sorted_children = sorted(cNode.child, key=lambda x: custom_sort(x.value))# Sort in ascending order for minimax on subsequent views
        return min_val, chosen_node

def secondLastMove(board):
    '''
        Checks if its the last move on the board

        Input:
            board (list) - the current board state

        Return:
            bool - True (if one more move on the board) False (if there exists more than one move on the board remaining)
    '''
    count = 0
    for row in board:
        count += row.count('-')
    
    return count == 1


if __name__ == "__main__":
    '''
        Testing if only if this program is run
    '''
    board = [['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']]

    current = node(board, 3,'X')
    first = True
    opponent = 'X'

    minimax(current,float('-inf'),float('inf'),False,'O')
    while len(current.child) != 0 or first:
        first = False
        row = int(input("row? "))
        column = int (input("column? "))
        newBoard = copy.deepcopy(current.cBoard)
        newBoard[row][column] = opponent

        for child in current.child:
            if child.cBoard == newBoard:
                break

        current = child
        
        for i in range(current.n):
            print(current.cBoard[i])
        
        _, current = (minimax(current,float('-inf'),float('inf'),True,'O'))
        for i in range(current.n):
            print(current.cBoard[i])
        
        if len(current.child) == 0:
            break
        print(current.move)
        