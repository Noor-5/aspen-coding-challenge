import random

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

def play_war():
    ranks =  ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = deal_cards()
    player1_deck = deck[:26]
    player2_deck = deck[26:]
    player1_pile = []
    player2_pile = []
    war_cards = []
    round = 1

    while True:
        print(f"Round {round}:")
        player1_card = player1_deck.pop(0)
        player2_card = player2_deck.pop(0)
        print(f"Player 1 plays: {player1_card[0]} {player1_card[1]}")
        print(f"Player 2 plays: {player2_card[0]} {player2_card[1]}")
        if ranks.index(player1_card[0]) > ranks.index(player2_card[0]):
            player1_pile.extend([player1_card, player2_card] + war_cards)
            war_cards = []
            print("Player 1 wins the round!")
            round += 1
        elif ranks.index(player1_card[0]) < ranks.index(player2_card[0]):
            player2_pile.extend([player1_card, player2_card] + war_cards)
            war_cards = []
            print("Player 2 wins the round!")
            round += 1
        elif ranks.index(player1_card[0]) == ranks.index(player2_card[0]):
            print("WAR!")
            war_cards.extend([player1_card, player2_card])
            if (len(player1_deck)> 0 and len(player2_deck) > 0):
                war_cards.append(player1_deck.pop(0))
                war_cards.append(player2_deck.pop(0))

        print(f"Player 1 deck: {len(player1_deck)} cards")
        print(f"Player 2 deck: {len(player2_deck)} cards")
        print()

        if len(player1_deck) == 0:
            if ((len(player2_pile) + len(player2_deck) + len(war_cards)) == 52 and len(player1_pile) == 0) :
                print("Player 1 has no more cards left. Player 2 wins!")
                return 2
            else:
                player1_deck = player1_pile
                player1_pile = []
                random.shuffle(player1_deck)
        if len(player2_deck) == 0:
            if ((len(player1_pile) + len(player1_deck)+ len(war_cards)) == 52 and len(player2_pile) == 0):
                print("Player 2 has no more cards left. Player 1 wins!")
                return 1
            else:
                player2_deck = player2_pile 
                player2_pile = []
                print(player2_deck)
                random.shuffle(player2_deck)


def main():
    play_war();


if __name__ == "__main__":
    main()