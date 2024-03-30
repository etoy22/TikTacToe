import copy

from heursitic import heuristic,node 


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
def minimax(cNode, alpha, beta, maxBool, player):
    '''
    This part only runs if its the first time the node has been looked at. This is so that we dont
    run the propogating of children more than once for any given node
    '''
    if cNode.new: 
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
            val, _ = minimax(children, alpha, beta, False, player)
            if val > max_val: 
                max_val = val
                chosen_node = children  
            alpha = max(alpha, max_val)
            if beta <= alpha:
                break
        return max_val, chosen_node  
    else: # Checks for minimizing of value
        min_val = float('inf')
        chosen_node = None  
        for children in cNode.child:
            val, _ = minimax(children, alpha, beta, True, player)
            if val < min_val:
                min_val = val
                chosen_node = children  
            beta = min(beta, min_val)
            if beta <= alpha:
                break
        return min_val, chosen_node


# TODO everything below subject to change as a result of the API

board = [['_', '_', '_']
         ['_', '_', '_']
         ['_', '_', '_']]

current = node(board, 3,'O')
first = True
opponent = 'X'

while len(current.child) != 0 or first:
    first = False
    _, current = (minimax(current,0,float('-inf'),float('inf'),True,current.player))
    for i in range(current.n):
        print(current.cBoard[i])

    if len(current.child) == 0:
        break
    
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