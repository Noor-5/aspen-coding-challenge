'''
Brief:
Program to simulate the card game War between two players.
'''

import random

# Player class to contain a given players deck and pile
class Player():
    def __init__(self, deck, pile):
        self.deck = deck
        self.pile = pile

# Create a deckof cards with 52 cards, 4 suits, and randomly shuffle.
def deal_cards():
    deck = []
    suits = ["clubs", "hearts", "spades", "diamonds"]
    ranks =  ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    for suit in suits:
        for rank in ranks:
            card = [rank, suit]
            deck.append(card)
    random.shuffle(deck)
    return deck


# Split deck between the two players. Each round the each player puts down
# a card. Player with the higher card adds both cards to their pile.
# If the cards are equal, there is War, and the winner takes all the cards.
# If the player runs out of cards in their deck, they use their pile after
# shuffling it. 
def play_war():
    ranks =  ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = deal_cards()
    player1 = Player(deck[:26], [])
    player2 = Player(deck[26:], [])
    war_cards = []
    round = 1

    while True:
        print(f"Round {round}:")
        # Players play the first card in their deck
        player1_card = player1.deck.pop(0)
        player2_card = player2.deck.pop(0)
        print(f"Player 1 plays: {player1_card[0]} {player1_card[1]}")
        print(f"Player 2 plays: {player2_card[0]} {player2_card[1]}")
        # Player 1's card is greater than player 2's card
        if ranks.index(player1_card[0]) > ranks.index(player2_card[0]):
            player1.pile.extend([player1_card, player2_card] + war_cards)
            war_cards = []
            print("Player 1 wins the round!")
            round += 1
        # Player 2's card is greater than player 1's card
        elif ranks.index(player1_card[0]) < ranks.index(player2_card[0]):
            player2.pile.extend([player1_card, player2_card] + war_cards)
            war_cards = []
            print("Player 2 wins the round!")
            round += 1
        # Cards are equal, so its war
        elif ranks.index(player1_card[0]) == ranks.index(player2_card[0]):
            print("WAR!")
            war_cards.extend([player1_card, player2_card])
            if (len(player1.deck)> 0 and len(player2.deck) > 0):
                war_cards.append(player1.deck.pop(0))
                war_cards.append(player2.deck.pop(0))

        print(f"Player 1 deck: {len(player1.deck)} cards")
        print(f"Player 2 deck: {len(player2.deck)} cards")
        print()

        # Player 1 has played all the cards in their deck
        if len(player1.deck) == 0:
            if ((len(player2.pile) + len(player2.deck) + len(war_cards)) == 52 and len(player1.pile) == 0) :
                print("Player 1 has no more cards left. Player 2 wins!")
                return 2
            else:
                # Move pile to deck and shuffle
                player1.deck = player1.pile
                player1.pile = []
                random.shuffle(player1.deck)
        # Player 1 has played all the cards in their deck
        if len(player2.deck) == 0:
            if ((len(player1.pile) + len(player1.deck)+ len(war_cards)) == 52 and len(player2.pile) == 0):
                print("Player 2 has no more cards left. Player 1 wins!")
                return 1
            else:
                 # Move pile to deck and shuffle
                player2.deck = player2.pile 
                player2.pile = []
                print(player2.deck)
                random.shuffle(player2.deck)


def main():
    play_war();


if __name__ == "__main__":
    main()