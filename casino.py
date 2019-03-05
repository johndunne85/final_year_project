import random
from poker_rules import POKER_BOX, Hand, Card, card_table
import numpy as np
import pandas as pd
import itertools
import copy
from collections import Counter
import collections
import torch

from neural_network_flop import Net, test_cards
from neural_network_turn import Net, test_cards_turn
from neural_network_river import Net, test_cards_river

# x = torch.FloatTensor([[32,14,3,10,31,11,23]])
#
# ans = test_cards_river(x)
# print(ans)

def determine_value(x):
    try:
        return int(x)
    except ValueError:
        return {
            'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }.get(x)

pre_flop_odds = {'AA':'r','AK':'r','AQ':'r','AJ':'r','KK':'r','KQ':'r','KJ':'r','QK':'r','JK':'r','QJ':'r'\
                ,'KA':'r','QA':'r','JA':'r','11':'r','99':'r','88':'r','77':'r','66':'r','JJ':'r','JQ':'r'}

pre_flop_fold = {'69':'f','96':'f','16':'f','61':'f','17':'f','71':'f'}

RANKS = [str(i) for i in range(6, 10)] + ['T','J', 'Q', 'K', 'A']
SUITS = ['C', 'D', 'H', 'S']
POKER_BOX = [r+s for r,s in itertools.product(RANKS, SUITS)]
random.seed()
random.shuffle(POKER_BOX)

ACTIONS = ['r', 'c', 'f']  # RAISE or CALL/CHECK or FOLD
turn_card = [0]
river_card = [0]
button = 0
#          0    1
stacks = [100, 100]
button_names = ['player_1','player_2']
pot = 0
small_blind = 1
big_blind = 2
player_1_raise = False
player_2_raise = False
player_1_bet_history = []
player_2_bet_history = []


#while(stacks[0] > 0 and stacks[1] > 0):



def decision_at_flop_player_1(p2_raise):

    if not p2_raise:
        return 'r'
    else:
        return 'f'

def decision_of_opponent_at_flop(p1_bet_history,p2_cards):

    score = best_hand(p2_cards)[0][0]
    if score > 0:
        player_2_bet_history.append('r')
        return 'r'
    else:
        player_2_bet_history.append('c')
        return 'c'

def decision_at_turn_player_1(p2_raise):
    if not p2_raise:
        return 'r'
    else:
        return 'c'

def decision_of_opponent_at_turn(p1_bet_history,p2_cards):

    score = best_hand(p2_cards)[0][0]
    if score > 0:
        player_2_bet_history.append('r')
        return 'r'
    else:
        player_2_bet_history.append('c')
        return 'c'

def decision_at_river_player_1(p2_raise):
    if not p2_raise:
        return 'r'
    else:
        return 'c'

def decision_of_opponent_at_river(p1_bet_history,p2_cards):

    score = best_hand(p2_cards)[0][0]
    if score > 0:
        player_2_bet_history.append('r')
        return 'r'
    else:
        player_2_bet_history.append('c')
        return 'c'

def best_hand(cards):
            all_hands = list(itertools.permutations(cards , 5))
            scores = [Hand(hand).get_score() for hand in all_hands]
            return max(scores),Hand(all_hands[scores.index(max(scores))])

def find_winner(p1_cards_FW, hand_type, p2_cards_FW):
    print('hand type {}'.format(hand_type[0]))
    p1_best, p1_hand = best_hand(p1_cards_FW)
    p2_best, p2_hand = best_hand(p2_cards_FW)
    p1_cards = p1_hand.values
    p2_cards = p2_hand.values
    print(p1_cards)
    print(p2_cards)

    if hand_type[0] == 1:
        print('yes one pair')
        p1 = [item for item, count in collections.Counter(p1_cards).items() if count > 1][0]
        p2 = [item for item, count in collections.Counter(p2_cards).items() if count > 1][0]
        if p1 > p2:
            return 0
        elif p2 > p1:
            return 1


    if hand_type[0] == 2:
        print('yes two pair')
        p1 = [item for item, count in collections.Counter(p1_cards).items() if count > 1]
        p2 = [item for item, count in collections.Counter(p2_cards).items() if count > 1]
        p1.sort()
        p1.reverse()
        p2.sort()
        p2.reverse()
        if p1[0] > p2[0]:
            return 0
        elif p2[0] > p1[0]:
            return 1
        elif p1[1] > p2[1]:
            return 0
        elif p2[1] > p1[1]:
            return 1


    if hand_type[0] == 3 or hand_type[0] == 7:
        print('yes three of a kind')
        p1 = [item for item, count in collections.Counter(p1_cards).items() if count > 1][0]
        p2 = [item for item, count in collections.Counter(p2_cards).items() if count > 1][0]
        if p1 > p2:
            return 0
        elif p2 > p1:
            return 1


    if hand_type[0] == 4 or hand_type[0] == 6 or hand_type[0] == 8:
        p1_cards.sort()
        p2_cards.sort()
        p1_cards.reverse()
        p2_cards.reverse()
        if p1_cards[0] > p2_cards[0]:
            return 0
        elif p2_cards[0] > p1_cards[0]:
            return 1


    if hand_type[0] == 5:
        p1 = [item for item, count in collections.Counter(p1_cards).items() if count > 1]
        p2 = [item for item, count in collections.Counter(p2_cards).items() if count > 1]
        p1.sort()
        p1.reverse()
        p2.sort()
        p2.reverse()
        if p1[0] > p2[0]:
            return 0
        elif p2[0] > p1[0]:
            return 1
        elif p1[1] > p2[1]:
            return 0
        elif p2[1] > p1[1]:
            return 1


    else:
        p1_cards.sort()
        p2_cards.sort()
        p1_cards.reverse()
        p2_cards.reverse()
        for i in range(len(p1_cards)):
            if p1_cards[i] > p2_cards[i]:
                return 0
            elif p1_cards[i] < p2_cards[i]:
                return 1

        else:
            return -1

bomb = True
while bomb:

    player_1_pre_flop_raise = False
    player_2_pre_flop_raise = False
    probability_num = random.randint(1,8)
    stacks[button] -= 2
    stacks[(button+1)%2] -= 4
    pot += 6

    # deal first 2 cards to players ***
    player_1 = POKER_BOX[:2]
    player_2 = POKER_BOX[2:4]
    # player_1 = ['1S','AD']
    # player_2 = ['AS','7D']

    player_1_two_card = player_1[0][0] + player_1[1][0]
    player_2_two_card = player_2[0][0] + player_2[1][0]

    p1_card_val_1 = player_1[0][0]
    p1_card_val_2 = player_1[1][0]


    print('player 1 two cards {}'.format(player_1))
    print('player 2 two cards {}'.format(player_2))


    if button_names[button] == 'player_1':
        pot += 2 # small blind
        stacks[0] -= 2
        pot += 4 # big blind
        stacks[1] -= 4
        if player_1_two_card in pre_flop_odds:
            print('player_1 raise')
            pot += 4
            stacks[0] -= 4
            player_1_pre_flop_raise = True
            player_1_bet_history.append('r')
        elif player_1[0][-1] != player_1[1][-1] and player_1_two_card in pre_flop_fold and probability_num != 8:
            print('player_1 folds pre flop')
            break
        else:
            pot += 2
            stacks[0] -= 2
            print('player 1 checks')
            player_1_bet_history.append('c')

        if player_2_two_card in pre_flop_odds:
            print('player_2 raise')
            if player_1_pre_flop_raise:
                pot += 4
                stacks[1] -= 4
            else:
                pot += 2
                stacks[1] -= 2
            player_2_pre_flop_raise = True
            player_2_bet_history.append('r')
        elif player_2[0][-1] != player_2[1][-1] and player_2_two_card in pre_flop_fold and probability_num != 8:
            print('player_2 folds pre flop')
            break
        else:
            if player_1_pre_flop_raise:
                pot += 2
                stacks[1] -= 2
            print('player 2 checks')
            player_2_bet_history.append('c')

    if button_names[button] == 'player_2':
        pot += 2 # small blind
        stacks[1] -= 2
        pot += 4 # big blind
        stacks[0] -= 4
        if player_2_two_card in pre_flop_odds:
            print('player_2 raise')
            pot += 4
            stacks[1] -= 4
            player_2_pre_flop_raise = True
            player_2_bet_history.append('r')
        elif player_2[0][-1] != player_2[1][-1] and player_2_two_card in pre_flop_fold and probability_num != 8:
            print('player_2 folds pre flop')
            break
        else:
            pot += 2
            stacks[1] -= 2
            print('player 2 checks')
            player_2_bet_history.append('c')

        if player_1_two_card in pre_flop_odds:
            print('player_1 raise')
            if player_2_pre_flop_raise:
                pot += 4
                stacks[0] -= 4
            else:
                pot += 2
                stacks[0] -= 2
            player_1_pre_flop_raise = True
            player_1_bet_history.append('r')
        elif player_1[0][-1] != player_1[1][-1] and player_1_two_card in pre_flop_fold and probability_num != 8:
            print('player_1 folds pre flop')
            break
        else:
            if player_2_pre_flop_raise:
                pot += 2
                stacks[0] -= 2
            print('player 1 checks')
            player_1_bet_history.append('c')

      # ******  end of pre flop betting ******


    flop_cards = POKER_BOX[4:7]
    # flop cards on table ***
    player_1_with_flop = player_1 + flop_cards
    player_2_with_flop = player_2 + flop_cards

    print(player_1_with_flop)
    # print(player_2_with_flop)
    p3 = player_1_with_flop

    x = torch.FloatTensor([[card_table[p3[0]],card_table[p3[1]],card_table[p3[2]],card_table[p3[3]],card_table[p3[4]]]])
    ans = test_cards(x)
    print(ans)



    cards =  player_1_with_flop
    # print(u"\u2665")
    # print(u"\u2663")

    # num = Hand(cards).get_score()
    # print('player 1 : score is {}'.format(num))
    #
    # num2 = Hand(player_2_with_flop).get_score()
    # opponent_hand_rank = num2[0]
    # print('player 2 : score is {}'.format(num2))
    # print(opponent_hand_rank)
#   ******************** here *********************

    if button_names[button] == 'player_1':
        if decision_at_flop_player_1(player_2_raise) == 'r':
            print('player_1 raise at flop')
            pot += 4
            stacks[0] -= 4
            player_1_raise = True
        elif decision_at_flop_player_1(player_2_raise) == 'c':
            print('player_1 calls')
            player_1_raise = False

        if decision_of_opponent_at_flop(player_1_bet_history,player_2_with_flop) == 'c':
            print('player_2 calls')
            if player_1_raise:
                pot += 4
                stacks[1] -= 4

        elif decision_of_opponent_at_flop(player_1_bet_history,player_2_with_flop) == 'r':
            print('player_2 raise at flop')
            if player_1_raise:
                pot += 8
                stacks[1] -= 8
            else:
                pot += 4
                stacks[1] -= 4
                player_2_raise = True

        if player_2_raise:
            if decision_at_flop_player_1(player_2_raise) == 'c':
                pot += 4
                stacks[0] -= 4

            elif decision_at_flop_player_1(player_2_raise) == 'f':
                print('player_1 folds')
                stacks[1] += pot
                print('player_2 wins ${}'.format(pot))
                break

    else:
        if decision_of_opponent_at_flop(player_1_bet_history,player_2_with_flop) == 'r':
            print('player_2 raise at flop')
            pot += 4
            stacks[1] -= 4
            player_2_raise = True
        elif decision_of_opponent_at_flop(player_1_bet_history,player_2_with_flop) == 'c':
            print('player_2 calls')
            player_2_raise = False

        if decision_at_flop_player_1(player_2_raise) == 'c':
            print('player_1 calls')
            if player_2_raise:
                pot += 4
                stacks[0] -= 4
        elif decision_at_flop_player_1(player_2_raise) == 'r':
            print('player_1 raise at flop')
            if player_2_raise:
                pot += 8
                stacks[0] -= 8
            else:
                pot += 4
                stacks[0] -= 4
            player_1_raise = True

        if player_1_raise:
            if decision_of_opponent_at_flop(player_1_bet_history,player_2_with_flop) == 'c':
                pot += 4
                stacks[1] -= 4
            elif decision_of_opponent_at_flop(player_1_bet_history,player_2_with_flop) == 'f':
                print('player_2 folds')
                stacks[0] += pot
                print('player_1 wins ${}'.format(pot))
                break

    # # Turn cards on table ***
    # player_1_raise = False
    # player_2_raise = False
    # turn_cards = POKER_BOX[7:8]
    # # print(flop_cards)
    # # print(turn_cards)
    #
    # player_1_cards_at_turn = player_1_with_flop + turn_cards
    # player_2_cards_at_turn = player_2_with_flop + turn_cards
    #
    # # print('player 1\'s cards at turn {}'.format(player_1_cards_at_turn))
    # # print('player 2\'s cards at turn {}'.format(player_2_cards_at_turn))
    #
    # # num = best_hand(player_1_cards_at_river)
    # # print('player_1 has {}'.format(num[0][1]))
    # # num2 = best_hand(player_2_cards_at_river)
    # # print('player_2 has {}'.format(num2[0][1]))
    #
    #         # betting at the river ***
    #
    # if button_names[button] == 'player_1':
    #     if decision_at_turn_player_1(player_2_raise) == 'r':
    #         print('player_1 raise at turn')
    #         pot += 4
    #         stacks[0] -= 4
    #         player_1_raise = True
    #     elif decision_at_turn_player_1(player_2_raise) == 'c':
    #         print('player_1 calls at turn')
    #         player_1_raise = False
    #
    #     if decision_of_opponent_at_turn(player_1_bet_history,player_2_cards_at_turn) == 'c':
    #         print('player_2 calls at turn')
    #         if player_1_raise:
    #             pot += 4
    #             stacks[1] -= 4
    #     elif decision_of_opponent_at_turn(player_1_bet_history,player_2_cards_at_turn) == 'r':
    #         print('player_2 raise at turn')
    #         if player_1_raise:
    #             pot += 8
    #             stacks[1] -= 8
    #         else:
    #             pot += 4
    #             stacks[1] -= 4
    #         player_2_raise = True
    #
    #     if player_2_raise:
    #         if decision_at_turn_player_1(player_2_raise) == 'c':
    #             pot += 4
    #             stacks[0] -= 4
    #         elif decision_at_turn_player_1(player_2_raise) == 'f':
    #             print('player_1 folds')
    #             stacks[1] += pot
    #             print('player_2 wins ${}'.format(pot))
    #             break
    #
    # else:
    #     if decision_of_opponent_at_turn(player_1_bet_history,player_2_cards_at_turn) == 'r':
    #         print('player_2 raise at turn')
    #         pot += 4
    #         stacks[1] -= 4
    #         player_2_raise = True
    #     elif decision_of_opponent_at_turn(player_1_bet_history,player_2_cards_at_turn) == 'c':
    #         print('player_2 calls at turn')
    #         player_2_raise = False
    #
    #     if decision_at_turn_player_1(player_2_raise) == 'c':
    #         print('player_1 calls at turn')
    #         if player_2_raise:
    #             pot += 4
    #             stacks[0] -= 4
    #     elif decision_at_turn_player_1(player_2_raise) == 'r':
    #         print('player_1 raise at turn')
    #         if player_2_raise:
    #             pot += 8
    #             stacks[0] -= 8
    #         player_1_raise = True
    #
    #     if player_1_raise:
    #         if decision_of_opponent_at_turn(player_1_bet_history,player_2_cards_at_turn) == 'c':
    #             pot += 4
    #             stacks[1] -= 4
    #         elif decision_of_opponent_at_turn(player_1_bet_history,player_2_cards_at_turn) == 'f':
    #             print('player_2 folds')
    #             stacks[0] += pot
    #             print('player_1 wins ${}'.format(pot))
    #             break
    #
    # player_1_raise = False
    # player_2_raise = False
    #
    # river_cards = POKER_BOX[8:9]
    # print(flop_cards)
    # print(turn_cards)
    # print(river_cards)
    #
    # player_1_cards_at_river = player_1_cards_at_turn + river_cards
    # player_2_cards_at_river = player_2_cards_at_turn + river_cards
    # print(player_1_cards_at_river)
    # print(player_2_cards_at_river)
    #
    #             # betting at the river ***
    #
    # if button_names[button] == 'player_1':
    #     if decision_at_river_player_1(player_2_raise) == 'r':
    #         print('player_1 raise at river')
    #         pot += 4
    #         stacks[0] -= 4
    #         player_1_raise = True
    #     elif decision_at_river_player_1(player_2_raise) == 'c':
    #         print('player_1 calls at river')
    #         player_1_raise = False
    #
    #     if decision_of_opponent_at_river(player_1_bet_history,player_2_cards_at_river) == 'c':
    #         print('player_2 calls at river')
    #         if player_1_raise:
    #             pot += 4
    #             stacks[1] -= 4
    #     elif decision_of_opponent_at_river(player_1_bet_history,player_2_cards_at_river) == 'r':
    #         print('player_2 raise at river')
    #         if player_1_raise:
    #             pot += 8
    #             stacks[1] -= 8
    #         else:
    #             pot += 4
    #             stacks[1] -= 4
    #         player_2_raise = True
    #
    #     if player_2_raise:
    #         if decision_at_river_player_1(player_2_raise) == 'c':
    #             pot += 4
    #             stacks[0] -= 4
    #         elif decision_at_river_player_1(player_2_raise) == 'f':
    #             print('player_1 folds')
    #             stacks[1] += pot
    #             print('player_2 wins ${}'.format(pot))
    #             break
    #
    # else:
    #     if decision_of_opponent_at_river(player_1_bet_history,player_2_cards_at_river) == 'r':
    #         print('player_2 raise at river')
    #         pot += 4
    #         stacks[1] -= 4
    #         player_2_raise = True
    #     elif decision_of_opponent_at_river(player_1_bet_history,player_2_cards_at_river) == 'c':
    #         print('player_2 calls at river')
    #         player_2_raise = False
    #
    #     if decision_at_river_player_1(player_2_raise) == 'c':
    #         print('player_1 calls at river')
    #         if player_2_raise:
    #             pot += 4
    #             stacks[0] -= 4
    #
    #     elif decision_at_river_player_1(player_2_raise) == 'r':
    #         print('player_1 raise at river')
    #         if player_2_raise:
    #             pot += 8
    #             stacks[0] -= 8
    #         else:
    #             pot += 4
    #             stacks[0] -= 4
    #         player_1_raise = True
    #
    #     if player_1_raise:
    #         if decision_of_opponent_at_river(player_1_bet_history,player_2_cards_at_river) == 'c':
    #             pot += 4
    #             stacks[1] -= 4
    #         elif decision_of_opponent_at_river(player_1_bet_history,player_2_cards_at_river) == 'f':
    #             print('player_2 folds')
    #             stacks[0] += pot
    #             print('player_1 wins ${}'.format(pot))
    #             break
    #
    # p1_cards_for_game = best_hand(player_1_cards_at_river)[0]
    # p2_cards_for_game = best_hand(player_2_cards_at_river)[0]
    # print('player 1 history {}'.format(p1_cards_for_game))
    # print('player 2 history {}'.format(p2_cards_for_game))
    # if p1_cards_for_game[0] > p2_cards_for_game[0]:
    #     print('player 1 wins ${}'.format(pot))
    # elif p1_cards_for_game[0] == p2_cards_for_game[0]:
    #     discision = find_winner(player_1_cards_at_river,p1_cards_for_game,player_2_cards_at_river)
    #     if discision == 0:
    #         print('player 1 wins')
    #     elif discision == 1:
    #         print('player 2 wins')
    #     else:
    #         print('it was a draw')
    # else:
    #     print('player 2 wins ${}'.format(pot))
    #
    bomb = False
