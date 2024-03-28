class node():
    def __init__(self, cBoard, m):
        self.cBoard = cBoard
        self.n = len(self.cBoard)
        self.m = m     

#assuming that node has cBoard, n, m
def is_winner(node, mark):

  def check_line(line):
    count = 0
    for cell in line:
      if cell == mark:
        count += 1
        if count == node.m:
          return True
      else: count = 0
    return False
  
  def check_row():
    for row in node.cBoard:
      if check_line(row):
        return True
    return False
  
  def check_col():
    transposed_matrix = [list(column) for column in zip(*node.cBoard)]
    for row in transposed_matrix:
      if check_line(row): 
        return True
    return False
  
  def check_diag():
    diag = []
    for i in range(node.n):
      for j in range(node.n):
        if i == j:
          diag.append(node.cBoard[i][j])
    return check_line(diag)
    
  def check_antiDiag():
    diag = []
    for i, j in zip(range(node.n), reversed(range(node.n))):
      diag.append(node.cBoard[i][j])
    return check_line(diag)

  is_row_winner = check_row()
  is_col_winner = check_col()
  is_diag_winner = check_diag()
  is_antiDiag_winner = check_antiDiag()

  if is_row_winner or is_col_winner or is_diag_winner or is_antiDiag_winner:
    return True
  else:
    return False

def is_draw(node):
  if not (is_winner(node, 'X') or is_winner(node, 'O')):
    for row in node.cBoard:
      for cell in row:
        if cell == '_':
          return False
    return True
  return False

def cutoffs(node, opponent_mark):

  def count_in_line(line):
    cutoff_cnt = 0
    count = 0
    for cell in line:
      if cell == opponent_mark:
        count += 1
        if count == node.m - 1:
          cutoff_cnt += 1
      else: count = 0
    return cutoff_cnt
  
  def count_row():
    cnt = 0
    for row in node.cBoard:
      cnt += count_in_line(row)
    return cnt
  
  def count_col():
    cnt = 0
    transposed_matrix = [list(column) for column in zip(*node.cBoard)]
    for row in transposed_matrix:
      cnt += count_in_line(row)
    return cnt
  
  def check_diag():
    diag = []
    for i in range(node.n):
      for j in range(node.n):
        if i == j:
          diag.append(node.cBoard[i][j])
    return count_in_line(diag)
    
  def check_antiDiag():
    diag = []
    for i, j in zip(range(node.n), reversed(range(node.n))):
      diag.append(node.cBoard[i][j])
    return count_in_line(diag)

  return (check_antiDiag() +  check_diag() + count_col() + count_row())

def heuristic(node, depth, agent_mark, opponent_mark):
  h = 0
  cutoffs_cnt = cutoffs(node, opponent_mark)
  if is_winner(node, agent_mark):
    h += (10*node.n - depth - cutoffs_cnt)
  elif is_winner(node, opponent_mark):
    h -= (10*node.n - depth - cutoffs_cnt)
  return h

board = [['X', 'X', 'O'],
         ['O', 'X', 'O'],
         ['_', 'X', '_']]

node1 = node(board, 3)

print(heuristic(node1, 2, 'O', 'X'))