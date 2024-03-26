from heursitic import heuristic

class node():
    def __init__(self, value=None):
        self.n = len(self.cBoard)
        self.child = []
        self.value = None
    
    def findVal(self):
        self.value = heuristic()

def minimax(node,depth,alpha,beta,max):
    if (len(node.child) == 0):
        return node.value

    if(max):
        max_val = float('-inf')
        for children in node.child:
            val = minimax(children,depth+1,alpha,beta,False)
            max_val = max(max_val,val)
            alpha = max(alpha,max_val)
            if beta <= alpha:
                break
        return max_val
    else:
        min_val = float('inf')
        for children in node.child:
            val = minimax(children,depth+1,alpha,beta,False)
            min_val = max(min_val,val)
            beta = min(beta,min_val)
            if beta <= alpha:
                break
        return min_val
