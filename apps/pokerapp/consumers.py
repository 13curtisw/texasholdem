# In consumers.py
from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from . import game
from . import views
from .models import User,Table
import time

global PLAYERS #keeps track of players in game
global TURN #keeps track of current players turn
global GAME #game object
global ROUNDOVER #keeps track of game state
ROUNDOVER = False
GAME = game.PokerGame()
PLAYERS = []
TURN = 0
# Connected to websocket.connect <-- Called when user visits the page
def ws_add(message):
	print message.content
	print message.channel
	print message.reply_channel.name
	print message.content['path'][1:-1]
	print "ws_add"
	Group("table").add(message.reply_channel)
	global PLAYERS
	PLAYERS.append({ "reply_channel": message.reply_channel, "channel_name": message.reply_channel.name})
	Group("table").send({"text": "reset"})
	print PLAYERS



# Connected to websocket.receive <-- Called when user sends a message to the server (buttons)
def ws_message(message):
	print "*"*60
	print message.content
	print message.content['text']
	print message.reply_channel
	print message.content["path"][1:-1]
	print "ws_message"
	global ROUNDOVER
	if message.content['text'] == "fold" and ROUNDOVER == False: #User pressed fold button
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name: #Runs when the socket connection matches
				global GAME
				if GAME.players[GAME.turn].name == player['username']: #Runs if it is the current players turn
					move = "move" + str(GAME.turn + 1) + "Fold."
					GAME.fold(player) # Folds the player and moves turn to next player
					Group("table").send({"text": move}) # Sends the fold message to template
					playersRemaining = 0
					temp = game.Player(100, "Temp")
					for x in GAME.inGame:
						if GAME.inGame[x]: # Checks how many players remain active in the game
							playersRemaining += 1
							temp = x
					if playersRemaining < 2: # Case where everybody but 1 person has folded
						s = GAME.awardWinner(temp)
						Group("table").send({"text": s}) # Sends a win message to template
						for client in PLAYERS:
							for user in GAME.players:
								if user.name == client['username']: 
									client['chips'] = user.money  # Updates each players money pool
						ROUNDOVER = True
						time.sleep(10) # Wait 10 seconds until the next game starts
						GAME.newGame()
						GAME = game.play(PLAYERS) # Makes a new game
						ROUNDOVER = False
						Group("table").send({"text": "reset"}) # Resets messages on template
						index = 0
						for player in PLAYERS:
							index += 1
							user = User.objects.get(username=player['username'])
					 		s = "prof" + str(index) + "../../static/" + user.picture # Shows the profile pictures of each player in their respective seats
							Group("table").send({"text": s})
						for player in GAME.players:
							cards = "hand" + GAME.deal(player) 
							cash = "cash" + str(player.money) 
							for client in PLAYERS:
								if player.name == client['username']:
									client['reply_channel'].send({"text": cards}) # Shows each player their personal hand
									client['reply_channel'].send({"text": cash}) # Shows each player their personal wallet
						GAME.preflop()
						for player in PLAYERS:
								global ROUNDOVER
								if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False: # Highlists the current turn players buttons
									player['reply_channel'].send({"text": "active"})
								else:
									player['reply_channel'].send({"text": "inactive"}) #Dehighlights everybody elses buttons
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s}) #Sends the current turn players name to template
					phase = 0
					if GAME.checkRoundEnd(): #Check if everybody has finished betting
						Group("table").send({"text": "bet$0"}) # Resets everybodys current round bet to 0
						phase = GAME.nextRound()
						if phase == 1: # Case where going from preflop to flop
							s = GAME.flop() 
							Group("table").send({"text": s})
						elif phase == 2: # Case where going from flop to turn
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3: # Case where going from turn to river
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4: # Case where going from river to showdown
							global ROUNDOVER
							s = GAME.showdown()
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money # Updates each players money
							ROUNDOVER = True
							Group("table").send({"text": s}) # Sends the winner message to template
							time.sleep(10) # Waits 10 seconds until next game starts
							GAME.newGame()
							GAME = game.play(PLAYERS) # Starts new game
							ROUNDOVER = False
							Group("table").send({"text": "reset"}) # Resets messages on template
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture # Shows profile pictures of every player in their respective seats
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player) # Shows each players personal hands
								cash = "cash" + str(player.money) # Shows each players personal wallets
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})
							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False: # Enables the current turn players buttons
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"}) # Disables everybody elses buttons
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name #Does not go to the next turn when its the game end
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})
	elif message.content['text'] == "check" and ROUNDOVER == False: # Case where user presses check
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username']:
					move = "move" + str(GAME.turn + 1) + "Check."
					GAME.check(player)
					Group("table").send({"text": move})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							s = GAME.showdown()
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							global ROUNDOVER
							ROUNDOVER = True
							Group("table").send({"text": s})
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})
							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})

	elif message.content['text'] == "call" and ROUNDOVER == False: # Case where user presses call button
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username']:
					move = "move" + str(GAME.turn + 1) + "Call."
					playerturn = GAME.turn
					GAME.call(player)
					cash = "cash" + str(GAME.players[playerturn].money)
					message.reply_channel.send({"text": cash})
					Group("table").send({"text": move})
					pot = "pot$" + str(GAME.pot)
					Group("table").send({"text": pot})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							s = GAME.showdown()
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							global ROUNDOVER
							ROUNDOVER = True
							Group("table").send({"text": s})
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})
							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})
				
	elif message.content['text'].isnumeric() and ROUNDOVER == False: # Case where user presses raise button
		global PLAYERS
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				global GAME
				if GAME.players[GAME.turn].name == player['username'] and (GAME.highestBet + int(message.content['text']) - GAME.players[GAME.turn].roundBet) <= GAME.players[GAME.turn].money:
					move = "move" + str(GAME.turn + 1) + "Raise $" + message.content['text']
					playerturn = GAME.turn
					GAME.raiseBet(player, message.content['text'])
					cash = "cash" + str(GAME.players[playerturn].money)
					message.reply_channel.send({"text": cash})
					Group("table").send({"text": move})
					pot = "pot$" + str(GAME.pot)
					Group("table").send({"text": pot})
					bet = "bet$" + str(GAME.highestBet)
					Group("table").send({"text": bet})
					phase = 0
					if GAME.checkRoundEnd():
						Group("table").send({"text": "bet$0"})
						phase = GAME.nextRound()
						if phase == 1:
							s = GAME.flop()
							Group("table").send({"text": s})
						elif phase == 2:
							s = GAME.turnphase()
							Group("table").send({"text": s})
						elif phase == 3:
							s = GAME.river()
							Group("table").send({"text": s})
						elif phase == 4:
							s = GAME.showdown()
							Group("table").send({"text": s})
							for client in PLAYERS:
								for user in GAME.players:
									if user.name == client['username']:
										client['chips'] = user.money
							global ROUNDOVER
							ROUNDOVER = True
							time.sleep(10)
							GAME.newGame()
							GAME = game.play(PLAYERS)
							ROUNDOVER = False
							Group("table").send({"text": "reset"})
							index = 0
							for player in PLAYERS:
								index += 1
								user = User.objects.get(username=player['username'])
						 		s = "prof" + str(index) + "../../static/" + user.picture 
								Group("table").send({"text": s})
							for player in GAME.players:
								cards = "hand" + GAME.deal(player)
								cash = "cash" + str(player.money)
								for client in PLAYERS:
									if player.name == client['username']:
										client['reply_channel'].send({"text": cards})
										client['reply_channel'].send({"text": cash})

							GAME.preflop()
							for player in PLAYERS:
									global ROUNDOVER
									if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
										player['reply_channel'].send({"text": "active"})
									else:
										player['reply_channel'].send({"text": "inactive"})
							s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
							Group("table").send({"text": s})
					if not phase == 4:
						s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
						Group("table").send({"text": s})
					break
		for player in PLAYERS:
			global ROUNDOVER
			if GAME.players[GAME.turn].name == player['username'] and ROUNDOVER == False:
				player['reply_channel'].send({"text": "active"})
			else:
				player['reply_channel'].send({"text": "inactive"})

	elif ROUNDOVER == False:
		global PLAYERS
		index = 0
		for player in PLAYERS:
			if player['channel_name'] == message.reply_channel.name:
				player['username'] = message.content['text']
				user = User.objects.get(username=player['username'])
				player['chips'] = user.balance
			index += 1
			user = User.objects.get(username=player['username'])
	 		s = "prof" + str(index) + "../../static/" + user.picture 
			Group("table").send({"text": s})
		if len(PLAYERS) > 1:
			global GAME
			GAME = game.play(PLAYERS)
			for player in GAME.players:
				cash = "cash" + str(player.money)
				cards = "hand" + GAME.deal(player)
				for client in PLAYERS:
					if player.name == client['username']:
						client['reply_channel'].send({"text": cards})
						client['reply_channel'].send({"text": cash})
			GAME.preflop()
			for player in PLAYERS:
					if GAME.players[GAME.turn].name == player['username']:
						player['reply_channel'].send({"text": "active"})
					else:
						player['reply_channel'].send({"text": "inactive"})
			s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
			Group("table").send({"text": s})
			# Group("table").send({
   #      		"text": message.content['text'],
   #  		})

	print PLAYERS
# Connected to websocket.disconnect <-- Called when user quits/leaves the page
def ws_disconnect(message):
	Group("table").discard(message.reply_channel)
	Group("table").send({"text": "resetall"})
	print message.reply_channel
	global PLAYERS
	for player in PLAYERS:
		print player
		if player['channel_name'] == message.reply_channel.name:
			PLAYERS.remove(player) # Removes player from game
			user = User.objects.get(username=player['username'])
			user.balance = player['chips']
			user.save() # Updates players money in database
	index = 0
	for player in PLAYERS:
		index += 1
		user = User.objects.get(username=player['username'])
 		s = "prof" + str(index) + "../../static/" + user.picture # Shows the profile pictures of each player in their respective seats
		Group("table").send({"text": s})
	if len(PLAYERS) > 1:
		global GAME
		GAME = game.play(PLAYERS)
		for player in GAME.players:
			cash = "cash" + str(player.money)
			cards = "hand" + GAME.deal(player)
			for client in PLAYERS:
				if player.name == client['username']:
					client['reply_channel'].send({"text": cards})
					client['reply_channel'].send({"text": cash})
		GAME.preflop()
		for player in PLAYERS:
				if GAME.players[GAME.turn].name == player['username']:
					player['reply_channel'].send({"text": "active"})
				else:
					player['reply_channel'].send({"text": "inactive"})
		s = "turn" + str(GAME.turn + 1) + GAME.players[GAME.turn].name
		Group("table").send({"text": s})
	print PLAYERS



