from Cards.Card import Card, Rank

# TODO (TASK 3): Implement a function that evaluates a player's poker hand.
#   Loop through all cards in the given 'hand' list and collect their ranks and suits.
#   Use a dictionary to count how many times each rank appears to detect pairs, three of a kind, or four of a kind.
#   Sort these counts from largest to smallest. Use another dictionary to count how many times each suit appears to check
#   for a flush (5 or more cards of the same suit). Remove duplicate ranks and sort them to detect a
#   straight (5 cards in a row). Remember that the Ace (rank 14) can also count as 1 when checking for a straight.
#   If both a straight and a flush occur in the same suit, return "Straight Flush". Otherwise, use the rank counts
#   and flags to determine if the hand is: "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind",
#   "Two Pair", "One Pair", or "High Card". Return a string with the correct hand type at the end.
def evaluate_hand(hand: list[Card]):
    ranks = []
    suits = []
    for card in hand:
        ranks.append(card.rank.value)
        suits.append(card.suit)

    rank_count = {}
    for r in ranks:
        if r not in rank_count:
            rank_count[r] = 1
        else:
            rank_count[r] += 1
    ranks_values = list(rank_count.values())
    ranks_values.sort(reverse=True)

    suit_count = {}
    for s in suits:
        if s not in suit_count:
            suit_count[s] = 1
        else:
            suit_count[s] += 1

    flush = False
    for s in suit_count:
        if suit_count[s] >= 5:
            flush = True

    unique_ranks = list(set(ranks))
    unique_ranks.sort()

    if 14 in unique_ranks:
        unique_ranks.append(1)
        unique_ranks.sort()

    straight = False
    counter = 1

    for i in range(1,len(unique_ranks)):
        if unique_ranks[i] == unique_ranks [i-1] + 1:
            counter += 1
        else:
            counter = 1
        if counter >= 5:
            straight = True

    if straight and flush:
        return "Straight Flush"
    elif 4 in ranks_values:
        return "Four of a Kind"
    elif 3 in ranks_values and 2 in ranks_values:
        return "Full House"
    elif flush:
        return "Flush"
    elif straight:
        return "Straight"
    elif 3 in ranks_values:
        return "Three of a Kind"
    elif ranks_values.count(2) >= 2:
        return "Two Pair"
    elif 2 in ranks_values:
        return "One Pair"
    return "High Card" # If none of the above, it's High Card
