# Tic-Tac-Toe: Adversarial search with Minimax


## Introduction

This report describes the development and analysis of an agent designed to play generalized Tic-Tac-Toe, a variant of the traditional game, on an n*n board. The objective of this version is for a player to place m consecutive symbols in a row, column, or diagonal to win. This project aims to construct a utility function, apply minimax—an adversarial search algorithm—and implement optimizations to enhance the algorithm's performance. The agent will compete against another agent through an API, automatically recording outcomes.

## Heuristics

One of the key points in applying the adversarial search is to determine the utility function for evaluating the state of the game. The following is the approach taken in designing the heuristic function:

- The function evaluates game states based on three possible outcomes: a win by the agent, a win by the opponent, or a draw. 
- The function attributes positive values to states leading to the agent's victory, negative values to those resulting in the opponent's win, and neutral values to draw states.
- The function considers the depth at which a state occurs in the game tree. The inclusion of depth results in outcomes where the agent wins in fewer moves, promoting efficiency.
- The function also takes into account the number of near-win situations for the opponent, which are referred to as 'cutoffs'. Evaluating cutoffs aims to lower the score of game states where the opponent is nearly winning, emphasizing the need for careful play.

The utility function is thus defined as follows:

- for a win by the agent: `h(n) = + (10*n - depth - cutoffs)`
- for a win by the opponent: `h(n) = - (10*n - depth - cutoffs)`
- for a draw: `h(n) = 0`

## Minimax 

The minimax algorithm is used for optimal decision-making in zero-sum games like Tic-Tac-Toe. It is an inherently recursive function where each call potentially leads to further calls evaluating all possible future game states aiming to maximize the utility for the player making the current move while minimizing the utility for the opponent. The search goes on until the terminal state is reached (i.e., current node has no possible moves left).

### The working principle of Minimax:

The recursive minimax has 2 base cases:
- Depth limit reached - in case of the current node reaching the specified depth limit, the heuristic value of that node is calculated and returned.
- Terminal state reached - if the current node has no available moves left, the recursion stops and the value and the current state are returned.

For nodes not previously explored, the heuristic function calculates their value based on the current game state. If it's not a winning position, child nodes representing possible moves are generated.

Depending on whether the state must be maximized or minimized, the function iterates through each node and applies minimax recursively.
- **Maximizing step**: The function chooses the child node with the maximum value from the children of the current node. After saving the chosen node, it then recursively calls itself with `maxBool` set to `False` as the next move must be minimized.
- **Minimizing step**: The function chooses the child node with the minimum value from the children of the current node. After saving the chosen node, it then recursively calls itself with `maxBool` set to `True` as the next move must be maximized.

During both maximizing and minimizing steps, alpha and beta values are updated and used to prune the search tree. In case of beta <= alpha meaning the current branch cannot be improved, further exploration is not allowed.

The exploration is done when all paths have been explored to the specified depth limit, or terminal states are reached. Each recursive call returns the optimal value achievable from the current node and the node that leads to this outcome. This makes sure that the initial call to the function eventually receives the best possible move from the game's current state, taking into account the opponent's best responses.

## Optimizations in the Minimax Algorithm

- **Alpha-Beta Pruning**: Increases efficiency by eliminating branches of the search tree that won't affect the outcome, reducing the number of nodes evaluated.
- **Depth limit**: Introduces an optional limit on search depth. When this limit is reached, the algorithm stops further exploration and returns the current node's score, preventing excessively deep searches.
- **Custom sorting of child nodes**: Child nodes of the current state are sorted by their scores – descending order for maximizing and ascending for minimizing. This is done to improve future pruning and search processes.

