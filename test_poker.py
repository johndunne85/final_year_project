import unittest
import casino

class TestPoker(unittest.TestCase):

    def test_find_winner(self):
        # Test for the value of a hand. Royal Flush.
        result = casino.find_winner(['AS','QS','JS','KS','TS'])
        self.assertEqual(result[1][0], 'royal_flush')
        # Test for the value of a hand. Straight Flush.
        result = casino.find_winner(['8H','6H','7H','TH','9H'])
        self.assertEqual(result[1][0], 'straight_flush')
        # Test for the value of a hand. Four of a Kind.
        result = casino.find_winner(['QS','QD','QC','AD','QH'])
        self.assertEqual(result[1][0], 'four_of_a_kind')
        # Test for the value of a hand. Flush.
        result = casino.find_winner(['8S','KS','JS','6S','AS'])
        self.assertEqual(result[1][0], 'flush')
        # Test for the value of a hand. Full House.
        result = casino.find_winner(['8S','8D','KC','KD','8C'])
        self.assertEqual(result[1][0], 'full_house')
        # Test for the value of a hand. Three of a Kind.
        result = casino.find_winner(['8S','8D','8C','AD','JS'])
        self.assertEqual(result[1][0], 'three_of_a_kind')
        # Test for the value of a hand. Straight.
        result = casino.find_winner(['7S','8D','9C','JD','TS'])
        self.assertEqual(result[1][0], 'straight')
        # Test for the value of a hand. Two Pair.
        result = casino.find_winner(['8S','8D','KC','AD','AS'])
        self.assertEqual(result[1][0], 'two_pair')
        # Test for the value of a hand. Pair.
        result = casino.find_winner(['8S','8D','KC','AD','JS'])
        self.assertEqual(result[1][0], 'pair')
        # Test for the value of a hand. High Card.
        result = casino.find_winner(['8S','6D','KC','AD','JS'])
        self.assertEqual(result[1][0], 'high_card')

        # Test for winning hand when both hands are the same. Three of a kind.
        result_1 = casino.find_winner(['8S','8D','8C','AD','JS'])[1][1]
        result_2 = casino.find_winner(['KS','KD','KC','AD','JS'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. Straight.
        result_1 = casino.find_winner(['6S','7D','8C','9D','TS'])[1][1]
        result_2 = casino.find_winner(['8S','9D','TC','JD','QS'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. Full House.
        result_1 = casino.find_winner(['7S','7D','7C','9D','9S'])[1][1]
        result_2 = casino.find_winner(['9S','9D','9C','JD','JS'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. Pair.
        result_1 = casino.find_winner(['6S','6D','8C','9D','TS'])[1][1]
        result_2 = casino.find_winner(['8S','8D','TC','JD','QS'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. Two Pairs.
        result_1 = casino.find_winner(['7S','7D','8C','8D','TS'])[1][1]
        result_2 = casino.find_winner(['KS','KD','TC','TD','QS'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. Four of a Kind.
        result_1 = casino.find_winner(['6S','6D','6C','6H','TS'])[1][1]
        result_2 = casino.find_winner(['KS','KD','KC','KH','QS'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. High Card.
        result_1 = casino.find_winner(['6S','7D','8C','9D','JS'])[1][1]
        result_2 = casino.find_winner(['8S','9D','TC','QD','6S'])[1][1]
        self.assertTrue(result_1 < result_2)

        # Test for winning hand when both hands are the same. Flush.
        result_1 = casino.find_winner(['JS','7S','8S','9S','TS'])[1][1]
        result_2 = casino.find_winner(['6S','9S','TS','JS','KS'])[1][1]
        self.assertTrue(result_1 < result_2)



if __name__=='__main__':
    unittest.main()
