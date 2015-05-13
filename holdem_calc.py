# Original program holdem_calc
# Created by Kevin Tseng
# From Github page: https://github.com/ktseng/holdem_calc
# Modified by pwwp

import time
import holdem_functions
import holdem_argparser


# Driver function which parses the command line arguments into hole cards,
# instantiates data structures to hold the intermediate results of the
# simulations, performs the simulations, and prints the results
def main():
    # Parse command line arguments into hole cards and create deck
    (hole_cards, num_iterations,
                    exact, given_board, deck, num_players) = holdem_argparser.parse_args()
    assigned_num_players, unassigned_num_players = len(hole_cards), num_players - len(hole_cards)
    if(num_players == 0):
        num_players = len(hole_cards)
    # Create results data structures which tracks results of comparisons
    # 1) result_histograms: a list for each player that shows the number of
    #    times each type of poker hand (e.g. flush, straight) was gotten
    # 2) winner_list: number of times each player wins the given round
    # 3) result_list: list of the best possible poker hand for each pair of
    #    hole cards for a given board
    result_list, winner_list = [None] * num_players, [0] * (num_players + 1)
    result_histograms = []
    for player in xrange(num_players):
        result_histograms.append([0] * 10)
    # Choose whether we're running a Monte Carlo or exhaustive simulation
    board_length = 0 if given_board == None else len(given_board)
    # When a board is given, exact calculation is much faster than Monte Carlo
    # simulation, so default to exact if a board is given
    generate_boards = holdem_functions.generate_random_boards

    # Run simulations
    for generated_cards in generate_boards(deck, num_iterations, board_length, unassigned_num_players):
        # Assign cards to unassigned players
        for i in range(unassigned_num_players):
            hole_cards.append((generated_cards[0], generated_cards[1]))
            del generated_cards[0:2]

        hole_card = tuple(hole_cards)
        remaining_board = generated_cards
        # Generate a new board
        if given_board:
            board = given_board[:]
            board.extend(remaining_board)
        else:
            board = remaining_board
        # Find the best possible poker hand given the created board and the
        # hole cards and save them in the results data structures
        (suit_histogram,histogram, max_suit) = holdem_functions.preprocess_board(board)
        for index, hole_card in enumerate(hole_cards):
            result_list[index] = holdem_functions.detect_hand(hole_card, board,suit_histogram, histogram, max_suit)
        # Find the winner of the hand and tabulate results
        winner_index = holdem_functions.compare_hands(result_list)
        winner_list[winner_index] += 1
        if winner_index != 0:
            print "Winner:" + str(winner_index) + " With cards " + str(hole_cards[winner_index - 1][0]) + " | "+ str(hole_cards[winner_index - 1][1])
        # Increment what hand each player made
        for index, result in enumerate(result_list):
            result_histograms[index][result[0]] += 1

        # Dump appended random hole_cards
        hole_cards = list(hole_cards)
        for i in range(unassigned_num_players):
            del hole_cards[assigned_num_players]
    holdem_functions.print_results(hole_cards, winner_list, result_histograms)

if __name__ == '__main__':
    start = time.time()
    main()
    print "\nTime elapsed(seconds): ", time.time() - start
