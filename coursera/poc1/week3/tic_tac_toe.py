"""
Monte Carlo Tic-Tac-Toe Player
"""
import random
import poc_simpletest
import poc_ttt_gui
import poc_ttt_provided as provided


# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
X = provided.PLAYERX
O = provided.PLAYERO
DRAW = provided.DRAW
EMPTY = provided.EMPTY
    
# ------------------------ FUNCTIONS --------------------------- #
def mc_trial(board, player):
    '''
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player by making random moves,
    alternating between players. The function should return when the game is over.
    '''
    in_progress = lambda: not board.check_win()
    while in_progress():
        row, col = random.choice(board.get_empty_squares())
        board.move(row, col, player)
        provided.switch_player(player)

def mc_update_scores(scores, board, player):
    '''
    Update the game score
    '''
    # Scores probably looks like: [ [0,0,0], [0,0,0], [0,0,0] ]
    
    if board.check_win() == provided.DRAW:
        return
    elif player == board.check_win():
        sign = 1
    elif player != board.check_win():
        sign = -1
    
    print("sign: %s" %sign)
    for row in range(len(scores[0])):
        for col in range(len(scores[0])):
            if board.square(row, col) == player:
                scores[row][col] += sign * SCORE_CURRENT
            elif board.square(row, col) == provided.switch_player(player):
                scores[row][col] -= sign * SCORE_OTHER
    print("SCORE_OTHER: %s" %SCORE_OTHER)
    print("SCORE_CURRENT: %s" %SCORE_CURRENT)
    return scores

def get_best_move(board, scores): 
    '''
    Take board and scores. Return a randomly picked tuple of best moves
    '''
    nrow = ncol = board.get_dim()
    #best_move_tuples = [(row,col) for row in range(nrow)
    #                    for col in range(ncol)
    #                   if board.square(row,col) == board.check_win()]
    max_value = 0
    score_index = {}
    print ('emptys', board.get_empty_squares())
    for row in range(len(scores)):
        for col in range(len(scores[row])):
            print ('index', score_index)
            if (row,col) not in board.get_empty_squares(): # need to define thse
                continue
            print ('scores', scores)
            print (row, col)
            score = scores[row][col]
            if score not in score_index:
                score_index[score] = [(row,col)]
            else:
                score_index[score].append((row,col))
    best_score = max(score_index)
    return random.choice(score_index[best_score])

def mc_move(board, player, trials):
    '''
    This function takes a current board, 
    which player the machine player is, 
    and the number of trials to run. 
    The function should use the Monte Carlo simulation 
    described above to return a move for the 
    machine player in the form of a (row, column) tuple. 
    Be sure to use the other functions you have written!
    '''
    pass


# ------------------------ PLAYGROUND --------------------------- #

print("EMPTY:   %s" %provided.EMPTY)                  
print("PLAYERX: %s" %provided.PLAYERX)
print("PLAYERO: %s" %provided.PLAYERO)
print("DRAW:    %s" %provided.DRAW)

board = provided.TTTBoard(3)
board.move(0, 0, provided.PLAYERX)
board.move(0, 1, provided.PLAYERX)
#board.move(0, 2, provided.PLAYERX)
board.move(2, 0, provided.PLAYERO)
board.move(2, 1, provided.PLAYERO)
board.move(2, 2, provided.PLAYERO)
print(board)
print("check_win: %s" %board.check_win())
print("provided.switch_player(O): %s" %provided.switch_player(O))
print("empty_squares: %s" %str(board.get_empty_squares()))
    
# ------------------------ FUNCTION TESTS --------------------------- #
def test_mc_update_scores():
    suite = poc_simpletest.TestSuite()
    board = provided.TTTBoard(3)
    board.move(0, 0, provided.PLAYERX)
    board.move(0, 1, provided.PLAYERX)
    board.move(0, 2, provided.PLAYERX)
    board.move(2, 0, provided.PLAYERO)
    board.move(2, 1, provided.PLAYERO)
    board.move(2, 2, provided.PLAYERO)
    computed1 = mc_update_scores([[0,0,0], [0,0,0], [0,0,0]], board, X)
    expected1 = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
    board2 = provided.TTTBoard(3)
    board2.move(0, 0, provided.PLAYERX)
    board2.move(1, 0, provided.PLAYERX)
    board2.move(2, 0, provided.PLAYERX)
    board2.move(1, 1, provided.PLAYERO)
    board2.move(2, 1, provided.PLAYERO)
    suite.run_test(computed1, expected1, "mc_test failed")
    computed2 = mc_update_scores([[0,0,0], [0,0,0], [0,0,0]], board2, O)
    expected2 = [[1, 0, 0], [1, -1, 0], [1, -1, 0]]
    suite.run_test(computed2, expected2, "mc_test failed")
    suite.report_results()
    
def test_get_best_move():
    suite = poc_simpletest.TestSuite()
    board = provided.TTTBoard(3)
    board.move(0, 0, provided.PLAYERX)
    board.move(0, 1, provided.PLAYERX)
    board.move(0, 2, provided.PLAYERX)
    board.move(2, 0, provided.PLAYERO)
    board.move(2, 1, provided.PLAYERO)
    board.move(2, 2, provided.PLAYERO)
    computed = get_best_move(board, [[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    expected = computed in [(0,0), (0,1), (0,2)]
    suite.run_test(True, expected, "get_best_move_test failed")
    
                   
# ------------------------ RUN TESTS --------------------------- #
test_mc_update_scores()
test_get_best_move()


# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
