"""
Black Jack Spring21
CSCI-154
The Deckers: Mark Ragasa, Francisco Gomez, Edmund Chin

This program checks in who many games the player loses $100k if for every game they
bet $100. This is run 100 times and the data is collect a graph line for each using 
plotly. Only one policy is use for this siulations. The policy is to Stand when hand is >= 14 & is hard.

Output:
This porgram prints a plotly graph of 100 lines. To print the graph it takes max 4 minutes.
"""
import plotly.graph_objects as go
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
    while ( i < 0 ):
        if hand[i] == 1:
            r = False
            break
        i += 1
    return r
def buildDeck():
    d = [11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10]
    return d
    
def writeData(policy,dc, games, deckType, checkHard, stats, wins, winsBj, losses, lossesBj, pushes, pushesBj, mc, money):
     #pdb.set_trace()
     policyType = "Stand when hand is >= "
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
     rows = [policyType, dT, games, wins, winsBj, losses, lossesBj, pushes, pushesBj,mc,money]
     filename = "goingbroke.csv"
     i = 0
     with open(filename, 'a') as csvfile:
         csvwriter = csv.writer(csvfile)
         #csvwriter.writerow(fields)
         csvwriter.writerow(rows)
         """
         while i < len(rows):
             csvwriter.writerow(rows[i])
             i += 1
        """
def monteCarlo(wins,games):
    return float(wins) / games
"""
This function takes: 1) A player policy. 2) Dealer's card if dealer card is zero then it does not 
is forced to the dealer otherwise a card is forced to the dealer.
3) Number of games. 4) Type of deck. 5) A bool to check if the player's hand is hard.
"""
def sim( policy, dc, games, deckType, checkHard, money):
    #award = random.randint(10,100)
    gamesTracker = []
    funds = []
    award = 100
    bet = award
    stringPolicy = str(policy)
    c =  wins = winsBj = losses = lossesBj = pushes = pushesBj = 0
    deck =  buildDeck()
    stats = (wins, winsBj, losses, lossesBj, pushes, pushesBj, money )
    #pdb.set_trace()
    random.shuffle(deck)
    deck2 = copy.deepcopy(deck)
    while money > 0: #c < games: # and money > 100:
        c += 1
        if deckType == 2:
            random.shuffle(deck)
        deck2 = copy.deepcopy(deck)
        stats = game(policy,dc,deck2, deckType, checkHard, wins, winsBj, losses, lossesBj, pushes, pushesBj, money,award, bet)
        wins = stats[0]
        winsBj = stats[1]
        losses = stats[2]
        lossesBj = stats[3]
        pushes = stats[4]
        pushesBj = stats[5]
        money = stats[6]
        #pdb.set_trace()
        #print("Money: ", money)
        funds.append(money)
        #print("Game:", c)
        gamesTracker.append(c)
    return (funds,gamesTracker)#mc

def game(policy, dc, inDeck,deckType, checkHard, wins, winsBj, losses, lossesBj, pushes, pushesBj, money,award,bet):
    # deal the first 4 cards of the game
    playerHand = []
    dealerHand = []
    playerPoints = 0
    dealerPoints = 0

    playerHand.append(dealCard(inDeck,deckType))
    dealerHand.append(dealCard(inDeck,deckType))

    
    playerHand.append(dealCard(inDeck,deckType))
    #If a specific card is given to the dealer comment the below line
    dealerHand.append(dealCard(inDeck,deckType))

    playerPoints = sum(playerHand)
    dealerPoints = sum(dealerHand)

    # after the first 4 cards of the game are dealt
    ## check if player or dealer have 2 Aces
    
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
            money += (award*1.5)
            return wins, winsBj, losses, lossesBj, pushes, pushesBj, money
        else:
            pushes += 1
            pushesBj += 1
            return wins, winsBj, losses, lossesBj, pushes, pushesBj, money
    # Player policies
    while playerPoints < 21:
        if checkHard and playerPoints >= policy and isHard(playerHand):
            break
        else:
            #pdb.set_trace()
            if playerPoints >= policy: # and dealerHand[0] == dc:
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
        money -= bet
        if dealerPoints == 21:
            lossesBj += 1
        return  wins, winsBj, losses, lossesBj, pushes, pushesBj, money
    # Check if dealer got a black black 
    if dealerPoints == 21:
        if playerPoints != 21:
            losses += 1
            lossesBj += 1
            money -= bet
            return  wins, winsBj, losses, lossesBj, pushes, pushesBj, money
        if playerPoints == 21:
            pushes += 1
            pushesBj += 1
            return wins, winsBj, losses, lossesBj, pushes, pushesBj, money
             
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
     
     # After dealer stops heating check if dealer has busted
    if dealerPoints > 21:
        wins += 1
        money += award
        return wins, winsBj, losses, lossesBj, pushes, pushesBj, money
    # if player has higher points then the dealer and no bust, player wins
    elif playerPoints > dealerPoints:
       wins += 1
       money += award
       return wins, winsBj, losses, lossesBj, pushes, pushesBj, money
    
    elif playerPoints < dealerPoints:
        losses += 1
        money -= bet
        return wins, winsBj, losses, lossesBj, pushes, pushesBj, money
    else:
        pushes += 1
        return wins, winsBj, losses, lossesBj, pushes, pushesBj, money

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

    
    fig = go.Figure()
    gs = [[]]
    gslastelement = []
    m = []
    i = 0
    money = 100000
    # 100 Lines are created and put into the grpah
    while i < 100:
        stats1 = sim(14,0,10000,2,True,money)
        gs.append(stats1[1])
        gslastelement.append(stats1[1][len(stats1[1])-1])
        fig.add_trace(go.Line(x=stats1[1], y=stats1[0],
                             line=dict(color='darkseagreen', width=2)))
        i+=1

    gs.pop(0)
    
    # Treand line
    lasts = [i[-1] for i in gs] 
    m = [1]
    r = sum(lasts) // len(lasts)
    m.append(r)


    fig.add_trace(go.Line(x=m,y=[money,0],line=dict(color='crimson',width=2,dash='dash')))
    fig.update_layout(title='Money over time with policy: Stand when hand is >= 14 & is hard.',
                               xaxis_title='Games', yaxis_title='Money')
    

    
    fig.show()
  
