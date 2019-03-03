import random
from poker_rules import POKER_BOX, Hand, Card
import numpy as np
import pandas as pd
import itertools
import copy
from collections import Counter
import collections
import torch

from neural_network_flop import Net, test_cards

# x = torch.FloatTensor([[12,32,30,28,18]])
#
# ans = test_cards(x)
# print(ans)

def determine_value(x):
    try:
        return int(x)
    except ValueError:
        return {
            'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }.get(x)

pre_flop_odds = {'AA':'r','AK':'r','AQ':'r','AJ':'r','KK':'r','KQ':'r','KJ':'r','QK':'r','JK':'r','QJ':'r'\
                ,'KA':'r','QA':'r','JA':'r','11':'r','99':'r','88':'r','77':'r','66':'r','JJ':'r','JQ':'r'}

pre_flop_fold = {'69':'f','96':'f','16':'f','61':'f','17':'f','71':'f'}

RANKS = [str(i) for i in range(6, 11)] + ['J', 'Q', 'K', 'A']
SUITS = ['C', 'D', 'H', 'S']
POKER_BOX = [r+s for r,s in itertools.product(RANKS, SUITS)]
random.seed()
random.shuffle(POKER_BOX)

ACTIONS = ['r', 'c', 'f']  # RAISE or CALL/CHECK or FOLD
turn_card = [0]
river_card = [0]
button = 1
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
        player_1_bet_history.append('r')
        return 'r'
    else:
        player_1_bet_history.append('c')
        return 'f'

def decision_of_opponent_at_flop(hand_score):

    if hand_score > 0:
        player_2_bet_history.append('r')
        return 'r'
    else:
        player_2_bet_history.append('c')
        return 'c'

def decision_at_turn_player_1(p2_raise):
    if not p2_raise:
        player_1_bet_history.append('r')
        return 'r'
    else:
        player_1_bet_history.append('c')
        return 'c'

def decision_of_opponent_at_turn(hand_score):

    if hand_score > 0:
        player_2_bet_history.append('r')
        return 'r'
    else:
        player_2_bet_history.append('c')
        return 'c'

def decision_at_river_player_1(p2_raise):
    if not p2_raise:
        player_1_bet_history.append('r')
        return 'r'
    else:
        player_1_bet_history.append('c')
        return 'c'

def decision_of_opponent_at_river(hand_score):


    if hand_score > 0:
        player_2_bet_history.append('r')
        return 'r'
    else:
        player_2_bet_history.append('c')
        return 'c'

def best_hand(cards):
            all_hands = list(itertools.permutations(cards , 5))
            scores = [Hand(hand).get_score() for hand in all_hands]
            return max(scores),Hand(all_hands[scores.index(max(scores))])

def find_winner(my_cards):
    values = []
    suits = []

    for c in my_cards:
        values.append(c[0])

    for v in my_cards:
        suits.append(v[1])

    suits_count = Counter(suits)
    values_count = Counter(values)
    # print(suits_count)
    # print(values_count)
    jset = set(values)


    if suits_count.most_common(1)[0][1] > 4: #rules out a royal flush, straight flush
        if 'A' in jset and 'K' in jset and 'Q' in jset and 'J' in jset and 'T' in jset:
            return (9, 'royal_flush')
        elif '6' in jset and '7' in jset and '8' in jset and '9' in jset and 'T' in jset:
            return (8, ['straight_flush',10])
        elif '7' in jset and '8' in jset and '9' in jset and 'T' in jset and 'J' in jset:
            return (8,  ['straight_flush',11])
        elif '8' in jset and '9' in jset and 'T' in jset and 'J' in jset and 'Q' in jset:
            return (8,  ['straight_flush',12])
        elif '9' in jset and 'T' in jset and 'J' in jset and 'Q' in jset and 'K' in jset:
            return (8,  ['straight_flush',13])
        else:
            maxValue = 0
            for c in values:
                if not c == 'J' and not c == 'Q' and not c == 'K' and not c == 'A' and not c == 'T':
                    maxValue = max(int(c), maxValue)
                else:
                    maxValue = max(maxValue, determine_value(c))
            return (6, ['flush',maxValue])
    elif values_count.most_common(1)[0][1] > 3: #four of a kind
        return (7, ['four_of_a_kind',values_count.most_common(1)[0][0]])
    elif values_count.most_common(1)[0][1] > 2 and values_count.most_common(2)[1][1] > 1: # full house
        return (5, ['full_house',values_count.most_common(1)[0][0]])
    elif 'A' in jset and 'K' in jset and 'Q' in jset and 'J' in jset and 'T' in jset:
        return (3, ['straight',14])
    elif '6' in jset and '7' in jset and '8' in jset and '9' in jset and 'T' in jset:
        return (3, ['straight',10])
    elif '7' in jset and '8' in jset and '9' in jset and 'T' in jset and 'J' in jset:
        return (3, ['straight',11])
    elif '8' in jset and '9' in jset and 'T' in jset and 'J' in jset and 'Q' in jset:
        return (3, ['straight',12])
    elif '9' in jset and 'T' in jset and 'J' in jset and 'Q' in jset and 'K' in jset:
        return (3, ['straight',13])
    elif values_count.most_common(1)[0][1] > 2: # three of a kind
        return (4, ['three_of_a_kind',values_count.most_common(1)[0][0]])
    elif values_count.most_common(1)[0][1] > 1 and values_count.most_common(2)[1][1] > 1:
        return (2, ['two_pair',values_count.most_common(1)[0][0]])
    elif values_count.most_common(1)[0][1] > 1:
        return (1, ['pair',values_count.most_common(1)[0][0]])

    else:
        maxValue = 0
        for c in values:
            if not c == 'J' and not c == 'Q' and not c == 'K' and not c == 'A' and not c == 'T':
                maxValue = max(int(c), maxValue)
            else:
                maxValue = max(maxValue, determine_value(c))
        return (0, ['high_card',maxValue])

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

    cards =  player_1_with_flop
    # print(u"\u2665")
    # print(u"\u2663")

    num = Hand(cards).get_score()
    print('player 1 : score is {}'.format(num))

    num2 = Hand(player_2_with_flop).get_score()
    opponent_hand_rank = num2[0]
    print('player 2 : score is {}'.format(num2))
    print(opponent_hand_rank)
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

        if decision_of_opponent_at_flop(opponent_hand_rank) == 'c':
            print('player_2 calls')
            if player_1_raise:
                pot += 4
                stacks[1] -= 4

        elif decision_of_opponent_at_flop(opponent_hand_rank) == 'r':
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
        if decision_of_opponent_at_flop(opponent_hand_rank) == 'r':
            print('player_2 raise at flop')
            pot += 4
            stacks[1] -= 4
            player_2_raise = True
        elif decision_of_opponent_at_flop(opponent_hand_rank) == 'c':
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
            if decision_of_opponent_at_flop(opponent_hand_rank) == 'c':
                pot += 4
                stacks[1] -= 4
            elif decision_of_opponent_at_flop(opponent_hand_rank) == 'f':
                print('player_2 folds')
                stacks[0] += pot
                print('player_1 wins ${}'.format(pot))
                break

     # Turn cards on table ***
    player_1_raise = False
    player_2_raise = False
    turn_cards = POKER_BOX[7:8]
    # print(flop_cards)
    # print(turn_cards)

    player_1_cards_at_turn = player_1_with_flop + turn_cards
    player_2_cards_at_turn = player_2_with_flop + turn_cards

    # print('player 1\'s cards at turn {}'.format(player_1_cards_at_turn))
    # print('player 2\'s cards at turn {}'.format(player_2_cards_at_turn))

    # num = best_hand(player_1_cards_at_river)
    # print('player_1 has {}'.format(num[0][1]))
    # num2 = best_hand(player_2_cards_at_river)
    # print('player_2 has {}'.format(num2[0][1]))

            # betting at the turn ***

    num3 = Hand(player_2_cards_at_turn).get_score()
    opponent_hand_rank = num3[0]
    print('player 2 : score is {}'.format(num3))
    print(opponent_hand_rank)

    if button_names[button] == 'player_1':
        if decision_at_turn_player_1(player_2_raise) == 'r':
            print('player_1 raise at turn')
            pot += 4
            stacks[0] -= 4
            player_1_raise = True
        elif decision_at_turn_player_1(player_2_raise) == 'c':
            print('player_1 calls at turn')
            player_1_raise = False

        if decision_of_opponent_at_turn(opponent_hand_rank) == 'c':
            print('player_2 calls at turn')
            if player_1_raise:
                pot += 4
                stacks[1] -= 4
        elif decision_of_opponent_at_turn(opponent_hand_rank) == 'r':
            print('player_2 raise at turn')
            if player_1_raise:
                pot += 8
                stacks[1] -= 8
            else:
                pot += 4
                stacks[1] -= 4
            player_2_raise = True

        if player_2_raise:
            if decision_at_turn_player_1(player_2_raise) == 'c':
                pot += 4
                stacks[0] -= 4
            elif decision_at_turn_player_1(player_2_raise) == 'f':
                print('player_1 folds')
                stacks[1] += pot
                print('player_2 wins ${}'.format(pot))
                break

    else:
        if decision_of_opponent_at_turn(opponent_hand_rank) == 'r':
            print('player_2 raise at turn')
            pot += 4
            stacks[1] -= 4
            player_2_raise = True
        elif decision_of_opponent_at_turn(opponent_hand_rank) == 'c':
            print('player_2 calls at turn')
            player_2_raise = False

        if decision_at_turn_player_1(player_2_raise) == 'c':
            print('player_1 calls at turn')
            if player_2_raise:
                pot += 4
                stacks[0] -= 4
        elif decision_at_turn_player_1(player_2_raise) == 'r':
            print('player_1 raise at turn')
            if player_2_raise:
                pot += 8
                stacks[0] -= 8
            player_1_raise = True

        if player_1_raise:
            if decision_of_opponent_at_turn(opponent_hand_rank) == 'c':
                pot += 4
                stacks[1] -= 4
            elif decision_of_opponent_at_turn(opponent_hand_rank) == 'f':
                print('player_2 folds')
                stacks[0] += pot
                print('player_1 wins ${}'.format(pot))
                break

    player_1_raise = False
    player_2_raise = False

    river_cards = POKER_BOX[8:9]

    player_1_cards_at_river = player_1_cards_at_turn + river_cards
    player_2_cards_at_river = player_2_cards_at_turn + river_cards


                # betting at the river ***

    num4 = Hand(player_2_cards_at_river).get_score()
    opponent_hand_rank = num4[0]
    print('player 2 at river: score is {}'.format(num4))
    print(opponent_hand_rank)

    if button_names[button] == 'player_1':
        if decision_at_river_player_1(player_2_raise) == 'r':
            print('player_1 raise at river')
            pot += 4
            stacks[0] -= 4
            player_1_raise = True
        elif decision_at_river_player_1(player_2_raise) == 'c':
            print('player_1 calls at river')
            player_1_raise = False

        if decision_of_opponent_at_river(opponent_hand_rank) == 'c':
            print('player_2 calls at river')
            if player_1_raise:
                pot += 4
                stacks[1] -= 4
        elif decision_of_opponent_at_river(opponent_hand_rank) == 'r':
            print('player_2 raise at river')
            if player_1_raise:
                pot += 8
                stacks[1] -= 8
            else:
                pot += 4
                stacks[1] -= 4
            player_2_raise = True

        if player_2_raise:
            if decision_at_river_player_1(player_2_raise) == 'c':
                pot += 4
                stacks[0] -= 4
            elif decision_at_river_player_1(player_2_raise) == 'f':
                print('player_1 folds')
                stacks[1] += pot
                print('player_2 wins ${}'.format(pot))
                break

    else:
        if decision_of_opponent_at_river(opponent_hand_rank) == 'r':
            print('player_2 raise at river')
            pot += 4
            stacks[1] -= 4
            player_2_raise = True
        elif decision_of_opponent_at_river(opponent_hand_rank) == 'c':
            print('player_2 calls at river')
            player_2_raise = False

        if decision_at_river_player_1(player_2_raise) == 'c':
            print('player_1 calls at river')
            if player_2_raise:
                pot += 4
                stacks[0] -= 4

        elif decision_at_river_player_1(player_2_raise) == 'r':
            print('player_1 raise at river')
            if player_2_raise:
                pot += 8
                stacks[0] -= 8
            else:
                pot += 4
                stacks[0] -= 4
            player_1_raise = True

        if player_1_raise:
            if decision_of_opponent_at_river(opponent_hand_rank) == 'c':
                pot += 4
                stacks[1] -= 4
            elif decision_of_opponent_at_river(opponent_hand_rank) == 'f':
                print('player_2 folds')
                stacks[0] += pot
                print('player_1 wins ${}'.format(pot))
                break

    p1_cards_for_game, p1 = find_winner(player_1_cards_at_river)
    p2_cards_for_game, p2 = find_winner(player_2_cards_at_river)

    # print('player 1 history {}'.format(p1))
    # print('player 2 history {}'.format(p2))
    if p1_cards_for_game > p2_cards_for_game:
        print('player 1 wins {}'.format(p1[1]))
        # print(jhand_flop+','+did_win,file=outfile)


    elif p1_cards_for_game == p2_cards_for_game:
        if p1[1] > p2[1]:
            # print(jhand_flop+','+did_win,file=outfile)
            print('player 1 wins {}'.format(p1))
        elif p1[1] < p2[1]:
            # print(jhand_flop+','+did_loss,file=outfile)
            print('player 2 wins {}'.format(p2))

        else:
            1+1
            print('draw')
    else:
        # print(jhand_flop+','+did_loss,file=outfile)
        print('player 2 wins {}'.format(p2))

    print('player 1 {}'.format(player_1_bet_history))
    print('player 2 {}'.format(player_2_bet_history))

    bomb = False
