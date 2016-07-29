# Required dependencies
from random import shuffle

# Deck of cards

class Card(object):
    def __init__(self, suit, value, image=None):
        self.suit = suit
        self.value = value
        self.image = image

    def displayCard(self):
        s = ""
        if self.value == 14:
            s = "Ace"
        elif self.value == 11:
            s = "Jack"
        elif self.value == 12:
            s = "Queen"
        elif self.value == 13:
            s = "King"
        else:
            s = str(self.value)
        return "[" + self.suit + ", " + s + "] "

    def imageValue(self):
        s = ""
        if self.value == 10:
            s += "0"
        elif self.value == 11:
            s += "J"
        elif self.value == 12:
            s += "Q"
        elif self.value == 13:
            s += "K"
        elif self.value == 14:
            s += "1"
        else:
            s += str(self.value)
        if self.suit == "Hearts":
            s += "H"
        elif self.suit == "Diamonds":
            s += "D"
        elif self.suit == "Clubs":
            s += "C"
        else:
            s += "S"
        return s

class Deck(object):
    def __init__(self, suits, values):
        self.suits = suits
        self.values = values
        self.deck = []
        self.buildDeck()

    def buildDeck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck.append(Card(suit, value))
        self.shuffle()
        return self

    def shuffle(self):
        shuffle(self.deck)
        return self

    def deal(self):
        if self.deck: # empty lists return as False
            # removes and returns card from deck, shuffled or not
            return self.deck.pop()
        else:
            print "No more cards"

    def returnCard(self, card, reShuffle = False):
        self.deck.append(card)
        if reShuffle:
            self.shuffle()
        return self

    def resetDeck(self):
        self.deck = []
        self.buildDeck()
        return self


class PokerGame(object):
    def __init__(self):
        self.pot=0
        self.players=[]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = range(2,15)
        self.deck = Deck(suits,values)
        self.table = []
        self.inGame = {}
        self.smallBlind = 10
        self.bigBlind = 20
        self.highestBet = 0
        self.turn = 0
        self.phase = 0 #0 --> preflop betting. #1 --> flop betting. #2 --> turn betting. #3 --> river betting
        self.counter = 0
    def add_player(self,player): #ADD A PLAYER TO THE POKER TABLE
        self.players.append(player)
        self.inGame[player] = True;
    def remove_player(self, player): #REMOVE A PLAYER FROM THE POKER TABLE
        self.players.remove(player)
        del self.inGame[player]
    def deal(self, player): # GIVES A PLAYER 2 CARDS
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
            s = ""
            for card in player.hand:
            	s += card.imageValue()
            return s

    def nextTurn(self):
    	self.counter += 1
    	if self.turn == len(self.players)-1:
    		self.turn = -1
    	self.turn += 1
    	while not self.inGame[self.players[self.turn]]:
    		if self.turn == len(self.players)-1:
    			self.turn = -1
    		self.turn += 1
    def checkRoundEnd(self):
    	moveOn = True
    	temp = 0
    	for player in self.players:
    		if self.inGame[player]:
    			temp += 1
    	for player in self.players:
			if self.inGame[player]:
				if player.roundBet < self.highestBet or self.counter < temp:
					moveOn = False
    	if moveOn:
			print "------------end of round-----------------"
    	return moveOn
    def nextRound(self):
		self.highestBet = 0
		self.turn = -1
		for player in self.players:
			player.roundBet = 0
		self.nextTurn()
		self.counter = 0
		self.phase += 1
		return self.phase
		# if self.phase == 0:
		# 	# self.flop()
		# 	self.phase += 1
		# elif self.phase == 1:
		# 	# self.turnphase()
		# 	self.phase += 1
		# elif self.phase == 2:
		# 	# self.river()
		# 	self.phase += 1
		# elif self.phase == 3:
		# 	# self.showdown()
		# 	# self.newGame()
    def fold(self, player):
    	if player['username'] == self.players[self.turn].name:
			print self.players[self.turn].name + " has folded."
			self.inGame[self.players[self.turn]] = False
			self.nextTurn()

    def check(self, player):
    	if player['username'] == self.players[self.turn].name:
	    	if self.highestBet ==self.players[self.turn].roundBet:
	    		print self.players[self.turn].name + " has checked."
	    		self.nextTurn()
    def call(self, player):
		if player['username'] == self.players[self.turn].name:
			if not self.highestBet == self.players[self.turn].roundBet:
				print self.players[self.turn].name + " has called."
				diff = self.highestBet - self.players[self.turn].roundBet
                if diff <= self.players[self.turn].money:
				    self.players[self.turn].money -= diff
				    self.players[self.turn].roundBet += diff
				    self.pot += diff
                else:
                    self.players[self.turn].roundBet += diff
                    self.pot += self.players[self.turn].money 
                    self.players[self.turn].money = 0
                self.nextTurn()
    def raiseBet(self, player, bet):
		if player['username'] == self.players[self.turn].name:
			bet = int(bet)
			print self.players[self.turn].name + " has raised $" + str(bet)
			self.highestBet += bet
			diff = self.highestBet - self.players[self.turn].roundBet
			self.pot += diff
			self.players[self.turn].money -= diff
			self.players[self.turn].roundBet = self.highestBet
			self.nextTurn()
    def newGame(self):
        self.pot=0
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = range(1,14)
        self.deck = Deck(suits,values)
        self.table = []
        self.inGame = {}
        self.smallBlind = 10
        self.bigBlind = 20
        self.highestBet = 0
        self.turn = 0
        self.phase = 0 #0 --> preflop betting. #1 --> flop betting. #2 --> turn betting. #3 --> river betting
        self.counter = 0
        for player in self.players:
        	self.inGame[player] = True;
        	player.hand = []
    def betting_round(self): # ALLOWS USER INPUTS FOR EACH PLAYER TO MAKE A BET. ALSO INCREASES POT SIZE
		counter = 0
		while True:
			self.turn = 0
			for player in self.players:
				if self.inGame[player]:
					print "Current highest bet: " + str(self.highestBet)
					print player.name + " bet so far: " + str(player.roundBet)
					print player.name + "'s turn & current money: " + str(player.money)
					if self.highestBet == player.roundBet:
						action = input("1.Fold 2.Check 3.Raise ")
						if action == 1:
							print player.name + " has folded."
							self.inGame[player] = False
						elif action == 2:
							print player.name + " has checked."
						else:
							bet = input(player.name + " make a bet : ")
							player.money -= bet
							player.roundBet += bet #MONEY PLAYER BET SO FAR
							self.pot += bet
							self.highestBet += bet #HIGHEST BET OF THE ROUND
					else:
						action = input("1.Fold 2.Call 3.Raise ")
						if action == 1:
							print player.name + " has folded."
							self.inGame[player] = False
						elif action == 2:
							print player.name + " has called."
							diff = self.highestBet - player.roundBet
							player.money -= diff
							player.roundBet += diff
							self.pot += diff
						else:
							bet = input(player.name + " make a raise : ")
							self.highestBet += bet
							diff = self.highestBet - player.roundBet
							self.pot += diff
							player.roundBet = self.highestBet
					counter += 1
					moveOn = True
					for player in self.players:
						if self.inGame[player]:
							if player.roundBet < self.highestBet or counter < len(self.players):
								moveOn = False
					if moveOn:
						self.highestBet = 0
						print "------------end of round-----------------"
						break
				self.turn += 1
    def showCard(self): #FLIPS A CARD FROM THE DECK ONTO THE PLAYING TABLE
        self.table.append(self.deck.deal())
    def preflop(self): #ROUND AFTER HANDS ARE DEALT
    	print "preflooooop"
        self.show_hand()
    def flop(self): #PUTS 3 CARDS ON THE TABLE AND PRINTS RELEVANT INFO
        self.showCard()
        self.showCard()
        self.showCard()
        self.show_table()
        self.show_hand()
        s = "flop"
        for card in self.table:
        	s += card.imageValue()
        return s
    def turnphase(self): #PUTS 1 CARD ON THE TABLE AND PRINTS RELEVANT INFO
        self.showCard()
        self.show_table()
        self.show_hand()
        s = "four"
        for card in self.table:
        	s += card.imageValue()
        return s
    def river(self): #PUTS 1 CARD ON THE TABLE AND PRINTS RELEVANT INFO
        self.showCard()
        self.show_table()
        self.show_hand()
        s = "rivr"
        for card in self.table:
        	s += card.imageValue()
        return s
    def show_table(self): #PRINTS THE POT SIZE AND THE CARDS ON THE TABLE
        print "\n"
        print  "Pot is: $" + str(self.pot)
        for x in self.table:
            print "Cards on the Table: " + x.displayCard()
    def show_hand(self): #PRINTS THE CARDS IN EACH PLAYERS HAND
        for x in self.players:
            if self.inGame[x]:
                temp = x.name + "'s Hand is: " 
                for hand in x.hand: 
                    temp += hand.displayCard()
                print temp
    def findBestHand(self, totalHand, start): #RECURSIVE FUNCTION TO FIND THE BEST HAND --> RETURNS A LIST OF TUPLES WHERE EACH TUPLE IS A POSSIBLE HAND COMBO CONTAINING THE COMBO SCORE AND COMBO TYPE
        if len(totalHand) == 5: #base case
            highcard = totalHand[0].value
            lowcard = totalHand[1].value
            for card in totalHand: #CHECKS FOR HIGHCARD
                if card.value > highcard:
                    highcard = card.value
                if card.value < lowcard:
                    lowcard = card.value
            handScore = highcard #HIGHCARD CASE
            handType = ["type", "kicker"]
            handType[0] = "High Card"


            counts = {}
            for card in totalHand: #COUNTS PAIRS/TRIPLES/FOURS
                if counts.has_key(card.value):
                    counts[card.value]+=1
                else:
                    counts[card.value]=1
            triples = [0, "key"]
            doubles = [0, "key"]
            for key in counts: #CHECKS FOR PAIRS/2PAIRS/TRIPLES/FOURS/FULLHOUSE
                if counts[key] == 4: #FOUR OF A KIND CASE
                    handScore = 70000 + key * 100 + highcard
                    handType[0] = "Four of a Kind"
                elif counts[key] == 3: 
                    if doubles[0] > 0: #FULL HOUSE CASE
                        handScore = 60000 + key * 200 + doubles[1] * 10 + highcard
                        handType[0] = "Full House"
                    else: #TRIPLES CASE
                        handScore = 30000 + key * 100 + highcard
                        handType[0] = "Three of a Kind"
                        triples[0] = 1
                        triples[1] = key
                elif counts[key] == 2:
                    if triples[0] == 1: #FULL HOUSE CASE
                        handScore = 60000 + triples[1] * 200 + key * 10 + highcard
                        handType[0] = "Full House"
                    elif doubles[0] > 0: #2 PAIRS CASE
                        handScore = 20000 + key * 100 + highcard
                        handType[0] = "Two Pairs"
                    else: #PAIR CASE
                        handScore = 10000 + key * 100 + highcard
                        handType[0] = "Pair"
                        doubles[0] += 1
                        doubles[1] = key

            flush = False
            straight = False
            flushCount = {}
            for card in totalHand: #COUNTS HOW MANY OF EACH SUIT IS IN THE 5 CARD HAND
                if flushCount.has_key(card.suit):
                    flushCount[card.suit] += 1
                else:
                    flushCount[card.suit] = 1

            for key in flushCount: #FLUSH CASE
                if flushCount[key] >= 5:
                    flush = True

            if highcard - lowcard == 4: #CHECK FOR STRAIGHT
                if doubles[0] == 0 and triples[0] == 0:
                    straight = True #STRAIGHT CASE

            if straight and flush: #STRAIGHT FLUSH CASE
                handScore = 80000 + highcard
                handType[0] = "Straight Flush"
            elif straight: #STRAIGHT CASE
                handScore = 40000 + highcard
                handType[0] = "Straight"
            elif flush: #FLUSH CASE
                handScore = 50000 + highcard
                handType[0] = "Flush"
            return (handScore, handType)

        else: #recursive case
            handScores = []
            for index in range(start, len(totalHand)):
                card = totalHand[index]
                totalHand.remove(card)
                hand = self.findBestHand(totalHand, index)
                if type(hand) == tuple:
                    handScores.append(hand)
                else:
                    handScores += hand
                totalHand.insert(index, card)
            return handScores
                        
    def showdown(self): #CHECKS TO SEE WHO HAS THE WINNING HAND AND PRINTS THE WINNER
        for x in self.players:
            if self.inGame[x]:
                totalHand = x.hand + self.table #LIST OF WHOLE 7 CARD HAND
                handScores = self.findBestHand(totalHand, 0)
                bestHand = handScores[0]
                for score in handScores:
                    if score[0] > bestHand[0]:
                        bestHand = score
                x.handScore = bestHand[0]
                x.handType = bestHand[1]
        winner = Player(100, "Temp")
        winners = []
        for player in self.players: #FINDS THE WINNER
            if self.inGame[player]:
                print player.name + "'s winning score: " + str(player.handScore)
                if player.handScore > winner.handScore:
                    winner = player
                    winners = [player]
                elif player.handScore == winner.handScore:
                    winners.append(player)
        if len(winners) > 1 and winner.handType[0] == "High Card": #TIE BREAKER FOR HIGH CARD
            for winner in winners:
                copy = [winner.hand[0].value, winner.hand[1].value]
                copy.sort(reverse=True)
                winner.handType[1] = copy
            high = winners[0] #CHECK FOR FIRST KICKER
            remove = []
            for winner in winners:
                if winner.handType[1][0] < high.handType[1][0]:
                    remove.append(winner)
                elif winner.handType[1][0] > high.handType[1][0]:
                    remove.append(high)
                    high = winner.handType[1][0]
            for loser in remove:
                winners.remove(loser)
            high = winners[0] #CHECK FOR SECOND KICKER
            remove = []
            for winner in winners:
                if winner.handType[1][1] < high.handType[1][1]:
                    remove.append(winner)
                elif winner.handType[1][1] > high.handType[1][1]:
                    remove.append(high)
                    high = winner
            for loser in remove:
                winners.remove(loser)

        if len(winners) == 1:
            return self.awardWinner(winners[0])
        else:
            return self.splitPot(winners)

    def awardWinner(self, winner):
        print str(winner.name) + " WINS with a " + str(winner.handType[0])
        winner.money += self.pot
        for player in self.players:
            print player.name + " now has $" + str(player.money)
        index = 0 
        for player in self.players:
            index +=1
            if player.name == winner.name: 
                if winner.handType[0] == 0:
                    return "wins" + winner.hand[0].imageValue() + winner.hand[1].imageValue() + str(index) + str(winner.name) + " WINS"
                else:
                    return "wins" + winner.hand[0].imageValue() + winner.hand[1].imageValue() + str(index) + str(winner.name) + " WINS with a " + str(winner.handType[0])
    def splitPot(self, winners):
        print "We have a tie"
        s = "tie!" + str(len(winners))
        for winner in winners:
            winner.money += self.pot / len(winners)
            index = 0
            count = 0
            for player in self.players:
                count += 1
                if player.name == winner.name:
                    index = count
            s += winner.hand[0].imageValue() + winner.hand[1].imageValue() + str(index)
        for player in self.players:
            print player.name + " now has $" + str(player.money)
        return s + "We have a tie!"


    # def findBestHand(self, totalHand, start): #RECURSIVE FUNCTION TO FIND THE BEST HAND --> RETURNS A LIST OF TUPLES WHERE EACH TUPLE IS A POSSIBLE HAND COMBO CONTAINING THE COMBO SCORE AND COMBO TYPE
    #     if len(totalHand) == 5: #base case
    #         highcard = totalHand[0].value
    #         lowcard = totalHand[1].value
    #         for card in totalHand: #CHECKS FOR HIGHCARD
    #             if card.value > highcard:
    #                 highcard = card.value
    #             if card.value < lowcard:
    #                 lowcard = card.value
    #         handScore = highcard #HIGHCARD CASE
    #         handType = "High Card"


    #         counts = {}
    #         for card in totalHand: #COUNTS PAIRS/TRIPLES/FOURS
    #             if counts.has_key(card.value):
    #                 counts[card.value]+=1
    #             else:
    #                 counts[card.value]=1
    #         triples = 0
    #         doubles = 0
    #         for key in counts: #CHECKS FOR PAIRS/2PAIRS/TRIPLES/FOURS/FULLHOUSE
    #             if counts[key] == 4: #FOUR OF A KIND CASE
    #                 handScore = 70000 + key * 100 + highcard
    #                 handType = "Four of a Kind"
    #             elif counts[key] == 3: 
    #                 if doubles > 0: #FULL HOUSE CASE
    #                     handScore = 60000 + key * 100 + highcard
    #                     handType = "Full House"
    #                 else: #TRIPLES CASE
    #                     handScore = 30000 + key * 100 + highcard
    #                     handType = "Three of a Kind"
    #                     triples = 1
    #             elif counts[key] == 2:
    #                 if triples == 1: #FULL HOUSE CASE
    #                     handScore = 60000 + key * 100 + highcard
    #                     handType = "Full House"
    #                 elif doubles > 0: #2 PAIRS CASE
    #                     handScore = 20000 + key * 100 + highcard
    #                     handType = "Two Pairs"
    #                 else: #PAIR CASE
    #                     handScore = 10000 + key * 100 + highcard
    #                     handType = "Pair"
    #                     doubles += 1

    #         flush = False
    #         straight = False
    #         flushCount = {}
    #         for card in totalHand: #COUNTS HOW MANY OF EACH SUIT IS IN THE 5 CARD HAND
    #             if flushCount.has_key(card.suit):
    #                 flushCount[card.suit] += 1
    #             else:
    #                 flushCount[card.suit] = 1

    #         for key in flushCount: #FLUSH CASE
    #             if flushCount[key] >= 5:
    #                 flush = True

    #         if highcard - lowcard == 4: #CHECK FOR STRAIGHT
    #             if doubles == 0 and triples == 0:
    #                 straight = True #STRAIGHT CASE

    #         if straight and flush: #STRAIGHT FLUSH CASE
    #             handScore = 80000 + highcard
    #             handType = "Straight Flush"
    #         elif straight: #STRAIGHT CASE
    #             handScore = 40000 + highcard
    #             handType = "Straight"
    #         elif flush: #FLUSH CASE
    #             handScore = 50000 + highcard
    #             handType = "Flush"
    #         return (handScore, handType)

    #     else: #recursive case
    #         handScores = []
    #         for index in range(start, len(totalHand)):
    #             card = totalHand[index]
    #             totalHand.remove(card)
    #             hand = self.findBestHand(totalHand, index)
    #             if type(hand) == tuple:
    #                 handScores.append(hand)
    #             else:
    #                 handScores += hand
    #             totalHand.insert(index, card)
    #         return handScores
                        
    # def showdown(self): #CHECKS TO SEE WHO HAS THE WINNING HAND AND PRINTS THE WINNER
	   #  for x in self.players:
    #     	if self.inGame[x]:
	   #          totalHand = x.hand + self.table #LIST OF WHOLE 7 CARD HAND
	   #          handScores = self.findBestHand(totalHand, 0)
	   #          bestHand = handScores[0]
	   #          for score in handScores:
	   #              if score[0] > bestHand[0]:
	   #                  bestHand = score
	   #          x.handScore = bestHand[0]
	   #          x.handType = bestHand[1]
	   #  winner = Player(100, "Temp")
	   #  for player in self.players:
	   #  	if self.inGame[player]:
	   #  		if player.handScore > winner.handScore:
	   #  			winner = player
	   #  return self.awardWinner(winner)

    # def awardWinner(self, winner):
	   #  print str(winner.name) + " WINS with a " + str(winner.handType)
	   #  winner.money += self.pot
	   #  for player in self.players:
	   #  	print player.name + "now has $" + str(player.money)
	   #  index = 0 
	   #  for player in self.players:
	   #  	index +=1
	   #  	if player.name == winner.name: 
	   #  		if winner.handType == 0:
	   #  			return "wins" + winner.hand[0].imageValue() + winner.hand[1].imageValue() + str(index) + str(winner.name) + " WINS"
	   #  		else:
	   #  			return "wins" + winner.hand[0].imageValue() + winner.hand[1].imageValue() + str(index) + str(winner.name) + " WINS with a " + str(winner.handType)

        # if self.players[0].handScore > self.players[1].handScore:
        #     print self.players[0].name + " WINS with a " + self.players[0].handType
        #     self.players[0].money += self.pot
        # elif self.players[0].handScore < self.players[1].handScore:
        #     print self.players[1].name + " WINS with a " + self.players[1].handType
        #     self.players[1].money += self.pot
        # else:
        #    print "draw..."
        # print self.players[0].name + " now has $" + str(self.players[0].money)
        # print self.players[1].name + " now has $" + str(self.players[1].money)


    # def showdown(self): #CHECKS TO SEE WHO HAS THE WINNING HAND AND PRINTS THE WINNER
    #     for x in self.players:
    #         totalHand = x.hand + self.table #LIST OF WHOLE 7 CARD HAND

    #         highcard = totalHand[0].value
    #         lowcard = totalHand[1].value
    #         for card in totalHand: #CHECKS FOR HIGHCARD
    #             if card.value > highcard:
    #                 highcard = card.value
    #             if card.value < lowcard:
    #                 lowcard = card.value
    #         x.handScore = highcard #HIGHCARD CASE


    #         counts = {}
    #         for card in totalHand: #COUNTS PAIRS/TRIPLES/FOURS
    #             if counts.has_key(card.value):
    #                 counts[card.value]+=1
    #             else:
    #                 counts[card.value]=1
    #         triples = 0
    #         doubles = 0
    #         for key in counts: #CHECKS FOR PAIRS/2PAIRS/TRIPLES/FOURS/FULLHOUSE
    #             if counts[key] == 4: #FOUR OF A KIND CASE
    #                 x.handType = 7
    #                 x.handScore = key * 100 + highcard
    #             elif counts[key] == 3: 
    #                 if doubles > 0: #FULL HOUSE CASE
    #                     x.handType = 6
    #                     x.handScore = key * 100 + highcard
    #                 else: #TRIPLES CASE
    #                     x.handType = 3
    #                     x.handScore = key * 100 + highcard
    #                     triples = 1
    #             elif counts[key] == 2:
    #                 if triples == 1: #FULL HOUSE CASE
    #                     x.handType = 6
    #                     x.handScore = key * 100 + highcard
    #                 elif doubles > 0: #2 PAIRS CASE
    #                     x.handType = 2
    #                     x.handScore = key * 100 + highcard
    #                 else: #PAIR CASE
    #                     x.handType = 1
    #                     x.handScore = key * 100 + highcard
    #                     doubles += 1

    #         flush = False
    #         straight = False
    #         flushCount = {}
    #         for card in totalHand: #COUNTS HOW MANY OF EACH SUIT IS IN THE 7 CARD HAND
    #             if flushCount.has_key(card.suit):
    #                 flushCount[card.suit] += 1
    #             else:
    #                 flushCount[card.suit] = 1

    #         for key in flushCount: #FLUSH CASE
    #             if flushCount[key] >= 5:
    #                 flush = True

    #         if highcard - lowcard == 4: #CHECK FOR STRAIGHT
    #             if doubles == 0 and triples == 0:
    #                 straight = True #STRAIGHT CASE

    #         if straight and flush: #STRAIGHT FLUSH CASE
    #             x.handType = 8
    #             x.handScore = highcard
    #         elif straight: #STRAIGHT CASE
    #             x.handType = 4
    #             x.handScore = highcard
    #         elif flush: #FLUSH CASE
    #             x.handType = 5
    #             x.handScore = highcard



    #     combos = {0: "High Card", 1: "Single Pair", 2: "Two Pairs", 3: "Three of a Kind", 4: "Straight", 5: "Flush", 6: "Full House", 7: "Four of a Kind", 8: "Straight Flush", 9: "Royal Flush"}

    #     #CHECKS WHO IS THE WINNER AND PRINTS THE WINNER     
    #     if self.players[0].handType > self.players[1].handType:
    #         print self.players[0].name + " WINS with a " + combos[self.players[0].handType]
    #     elif self.players[0].handType < self.players[1].handType:
    #         print self.players[1].name + " WINS with a " + combos[self.players[1].handType]
    #     elif self.players[0].handScore > self.players[1].handScore:
    #         print self.players[0].name + " WINS with a " + combos[self.players[0].handType]
    #     elif self.players[0].handScore < self.players[1].handScore:
    #         print self.players[1].name + " WINS with a " + combos[self.players[1].handType]
    #     else:
    #         print "draw??..."







class Player(object):
    def __init__(self,money,name):
        self.hand = []
        self.handType = 0
        self.handScore = 0
        self.money = money
        self.name = name
        self.roundBet = 0



#GAME LOOP
def play(players):
	game=PokerGame()
	for player in players:
		print player
		newplayer = Player(player['chips'], player['username'])
		game.add_player(newplayer)
	return game
	# game.betting_round()
	# game.flop()
	# game.betting_round()
	# game.turn()
	# game.betting_round()
	# game.river()
	# game.showdown()


# Features/Fixes to implement
# 1. Proper betting rounds (fold, call, check, raise)
# 2. Flexibility for more than 2 players
# 3. Blinds (big blind, small blind)
# 4. Bug fixes on scoring algorithm (what if two people get the same combo type? tiebreaker for equal hands? royal flush? )
# 5. Game reset option to play more than 1 round
# 6. Burn cards for flop/turn/river
# 7. Boundaries for players money (no negative money values)
# 8. All-in rules (pot splitting)
# 9. Code structure clean-up (factor out functions to help readability)

