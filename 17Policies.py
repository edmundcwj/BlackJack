"""
Black Jack Spring21
CSCI-154
The Deckers: Mark Ragasa, Francisco Gomez, Edmund Chin

This program checks 17 policies to find which one is the best policy.

Output:
This program ouputs data as csv file and updates if the file name matches a
file in the directory. If the old csv file needs to be keep move the csv file to
a diferent directory.
"""
#import plotly.graph_objects as go
import random
import copy
import pdb
import csv

def dealCard(deck, deckType):
    if deckType == 1:
        card = random.choice(deck)
    else:
        card = deck.pop(0)
    return card 
def isHard(hand):
    r = True
    c = len(hand)
    i = 0
    while ( i < c ):
        if hand[i] == 11:
            #print(hand[i])
            #print("False")
            return False
            break
        i += 1
    return r
def buildDeck():
    d = [11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10]
    return d
    
def writeData(policy,dc, games, deckType, checkHard, stats, wins, winsBj, losses, lossesBj, pushes, pushesBj, mc):
     #pdb.set_trace()
     policyType = "Stand when hand is >= "
     if dc == 0:
        policyType = policyType + str(policy) 
     else: 
        policyType = policyType + str(policy) + " & dealer face up card is = " + str(dc) 
     infiteDeck = "Infinite deck on  every run a card is drawn with equal probability."
     oneDeck = "One deck of cards is used. The deck is reshuffled after every game."
     if deckType == 1:
         dT = infiteDeck
     else:
         dT = oneDeck
     if checkHard:
         policyType = policyType + " & Player's hand is hard."
     
     fields = [ 'Policy', 'Type of deck', 'Number of Games', 'Player wins', 'Player Wins with Blackjack', 'Dealer Wins', 'Dealer wins with Blackjack', 'Pushes', 'Pushes with Blackjack', 'Monte Carlo'] 
     rows = [policyType, dT, games, wins, winsBj, losses, lossesBj, pushes, pushesBj,mc]
     filename = "17Policies.csv"
     i = 0
     with open(filename, 'a', newline='') as csvfile:
         csvwriter = csv.writer(csvfile)
         csvwriter.writerow(rows)
       
def monteCarlo(wins,games):
    return float(wins) / games
"""
This function takes: 1) A player policy. 2) Dealer's card if dealer card is zero then it does not 
is forced to the dealer otherwise a card is forced to the dealer.
3) Number of games. 4) Type of deck. 5) A bool to check if the player's hand is hard.
"""
def sim( policy, dc, games, deckType, checkHard):
    policyType = "Stand when hand is >= "
    gamesTracker = []
    funds = []
    award = 100
    bet = award
    stringPolicy = str(policy)
    c =  wins = winsBj = losses = lossesBj = pushes = pushesBj = 0
    deck =  buildDeck()
    stats = (wins, winsBj, losses, lossesBj, pushes, pushesBj)
    #pdb.set_trace()
    random.shuffle(deck)
    deck2 = copy.deepcopy(deck)
    while c < games: 
        c += 1
        if deckType == 2:
            random.shuffle(deck)
        deck2 = copy.deepcopy(deck)
        stats = game(policy,dc,deck2, deckType, checkHard, wins, winsBj, losses, lossesBj, pushes, pushesBj)
        wins = stats[0]
        winsBj = stats[1]
        losses = stats[2]
        lossesBj = stats[3]
        pushes = stats[4]
        pushesBj = stats[5]

    if dc == 0:
        policyType = policyType + str(policy) 
    else: 
       policyType = policyType + str(policy) + " & dealer face up card is = " + str(dc) 
    infiteDeck = "Infinite deck on  every run a card is drawn with equal probability."
    oneDeck = "One deck of cards is used. The deck is reshuffled after every game."
    if deckType == 1:
        dT = infiteDeck
    else:
        dT = oneDeck
    if checkHard:
        policyType = policyType + " & Player's hand is hard."
   
    print("Tuple of stats: ", stats)
    print()
    print("Simulation Stats")
    print("Number of Games:              ", games)
    #print("Number of Games:              ", c)
    print("Player Wins:                  ", wins)
    print("Player Wins with Blackjack:   ", winsBj)
    print("Dealer Wins:                  ", losses)
    print("Dealer wins with Blackjack:   ", lossesBj)
    print("Pushes:                       ", pushes)
    print("Pushes with Blackjack:        ", pushesBj)
    mc = monteCarlo(wins,games)
    print("Monte Carlo:                  ", mc)
    writeData(policy, dc, games, deckType, checkHard, stats, wins, winsBj, losses, lossesBj, pushes, pushesBj,mc)
    
    return mc

def game(policy, dc, inDeck,deckType, checkHard, wins, winsBj, losses, lossesBj, pushes, pushesBj):
    playerHand = []
    dealerHand = []
    playerPoints = 0
    dealerPoints = 0
    #if the dealer card is 0 then no card is forced on dealer
    if dc == 0:
        playerHand.append(dealCard(inDeck,deckType))
        dealerHand.append(dealCard(inDeck,deckType))

    #if the dealer card is not 0 then the first card is forced on the dealer
    else: 
        playerHand.append(dealCard(inDeck,deckType))
        dealerHand.append(dc)
        #if one deck remove the card forced to the dealer
        if deckType == 2:
            inDeck.remove(dc)

    # The second card given to the player and dealer 
    playerHand.append(dealCard(inDeck,deckType))
    dealerHand.append(dealCard(inDeck,deckType))

    playerPoints = sum(playerHand)
    dealerPoints = sum(dealerHand)

    # after the first 4 cards of the game are dealt
    ## check if the if two Acces
    
    if playerPoints == 22:
        playerHand[0] = 1
        playerPoints -= 10

    if dealerPoints == 22:
        dealerHand[1] = 1
        playerPoints -= 10

    # Check if player wins with a natural black jack or pushes
    if playerPoints == 21:
        if dealerPoints != 21:
            wins += 1
            winsBj += 1
            return wins, winsBj, losses, lossesBj, pushes, pushesBj
        else:
            pushes += 1
            pushesBj += 1
            return wins, winsBj, losses, lossesBj, pushes, pushesBj
    # Player policies
    while playerPoints < 21:
        #pdb.set_trace()
        # if the first card is not forced to the dealer dont check dealer card
        if dc==0:
            # check if a hand is hard
            if checkHard:
                #print(checkHard)
                #print(playerHand) 
                if isHard(playerHand) and playerPoints >= policy:
                    break
            elif not checkHard:
                #print(checkHard)
                #print(playerHand) 
                #pdb.set_trace()
                if playerPoints >= policy: # and dealerHand[0] == dc:
                    break
        # if the first card is forced to the dealer
        else:
            if checkHard:
                #print(checkHard)
                #print(playerHand) 
                if isHard(playerHand) and playerPoints >= policy and dealerHand[0] == dc:
                    #print(isHard(playerHand))
                    break
            elif not checkHard:
                #print(checkHard)
                #print(playerHand) 
                #pdb.set_trace()
                if playerPoints >= policy and dealerHand[0] == dc:
                    #print(isHard(playerHand))
                    break
                    
        # Deal a new card to player
        playerCard = dealCard(inDeck,deckType)
        playerHand.append(playerCard)
        playerPoints += playerCard
        # if player hand excess 21 turn Ace(s) to be worth 1 pointinsted of 11
        c = 0
        while playerPoints > 21 and c < len(playerHand):
                if playerHand[c] == 11:
                    playerHand[c] = 1
                    playerPoints -= 10
                c += 1
    # After player stop hiting check if player has busted if so end game  
    if playerPoints > 21:
        losses += 1
        if dealerPoints == 21:
            lossesBj += 1
        return  wins, winsBj, losses, lossesBj, pushes, pushesBj
    # Check if dealer got a black black 
    if dealerPoints == 21:
        if playerPoints != 21:
            losses += 1
            lossesBj += 1
            return  wins, winsBj, losses, lossesBj, pushes, pushesBj
        if playerPoints == 21:
            pushes += 1
            pushesBj += 1
            return wins, winsBj, losses, lossesBj, pushes, pushesBj
             
    # Dealer 
    while dealerPoints < 17:
        # Dealer gets new card
        dealerCard = dealCard(inDeck, deckType)
        dealerHand.append(dealerCard)
        dealerPoints += dealerCard
        # if dealer hands excess 21 turn Ance(s) to be worth 1 point insted of 11 
        c = 0
        while dealerPoints > 21 and c < len(dealerHand):
            if dealerHand[c] == 11:
                dealerHand[c] = 1
                dealerPoints -= 10
            c += 1
     
     # After daler stops heating check if dealer has busted
    if dealerPoints > 21:
        wins += 1
        return wins, winsBj, losses, lossesBj, pushes, pushesBj
    # if player has higher points then the dealer and no bust, player wins
    elif playerPoints > dealerPoints:
       wins += 1
       return wins, winsBj, losses, lossesBj, pushes, pushesBj
    
    elif playerPoints < dealerPoints:
        losses += 1
        return wins, winsBj, losses, lossesBj, pushes, pushesBj
    else:
        pushes += 1
        return wins, winsBj, losses, lossesBj, pushes, pushesBj

if __name__ == '__main__':
     ## Policies
        # Policy 1: if your hand => 17, stick, else hit
        # Policy 2: If you hand => 17 and is hard, stick. Else hit unless your hand = 21
        # Alays stick
        # My policie
            # Policy 4: Always hit
            # Policy 5: If you hand => 12 and is hard, stick. Else hit unless your hand = 21

 

    ## Type of deck
        # 1: for Infinite deck: On every run a card is drawn with equal probability.
        # 2: for One deck of cards is used. The deck is reshuffled after every game.

   
    q = 0
    bools = [True,False]
    while q < 2:
        games = 0 
        while games < 1:
            games += 1000000
            deckType = 1 
            while deckType < 3:
                pPoints = 4 
                while pPoints < 22:
                    sim(pPoints,0,games,deckType,bools[q]) 
                    pPoints += 1
                deckType += 1
        q += 1
