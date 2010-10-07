import pickle
import cfg

class Settings:
	def __init__(self, name="unnamed.set", betsizes=[1, 2, 5, 10, 50], numPayouts=5, numReels=3, payouts=[20, 12, 10, 5, 3, 2, 1], rounds=100, seed=20, debt=False, currency="$", probDict = {'obtain' : True, 'msg': "What do you think the odds of winning were?", 'interval' : 100, 'when' : "end"}, symbols=[cfg.IM_GOLDBARS, cfg.IM_TREASURECHEST, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL, cfg.IM_CLOVER, cfg.IM_BLANK], visibleSymbols = [cfg.IM_GOLDBARS, cfg.IM_TREASURECHEST, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL], showPayouts = True, saveAs = "Subject", session=1, subInfo = {'Name' : True, 'Age' : True, 'Sex': True, 'Handedness': True}, gamblersFallacy = False, stimList=[], override={'engage':False, 'odds':[], 'nearMiss':[]}, instructions = ""):
		#Main class with which to access and set experimental settings (Bets, Symbols, Payouts)
		self.name = name
		self.betsizes = betsizes
		self.symbols = symbols
		self.visibleSymbols = visibleSymbols
		self.numPayouts = numPayouts
		self.numReels = numReels
		self.payouts = payouts[0:numPayouts]
		self.seed = seed
		self.rounds = rounds
		self.debt = debt
		self.currency = currency
		self.probDict = probDict
		self.createInitCombos()
		self.showPayouts = showPayouts
		self.saveAs = saveAs
		self.session = session
		self.subInfo = subInfo
		self.gamblersFallacy = gamblersFallacy
		self.stimList = stimList
		self.override = override
		self.odds = [0] * len(self.payouts)
		if instructions == "":
			self.instructions = cfg.INSTRUCTIONS_HTML
		else:
			self.instructions = instructions
		
		
	def getWinnings(self, i, j):
		if self.override['engage']:
			odds = self.override['odds']
			odds = map(lambda x: x / 100., odds)
		else:
			odds = self.odds
				
		#returns the winnings given indeces of the payout size and bet size
		winnings = odds[i] * self.payouts[i] * self.betsizes[j]
		return winnings

	def getMaxPay(self):
		if self.override['engage']:
			odds = self.override['odds']
			odds = map(lambda x: x / 100., odds)
		else:
			odds = self.odds
		#returns the maximum amount of money that can be won
		maxpay = self.seed
		subtractor = self.rounds * self.betsizes[0] * (1-sum(odds))
		for j in range(0, len(self.payouts)):
			maxpay = maxpay + self.getWinnings(j, -1) 
		maxpay = maxpay - subtractor
		return maxpay

	def getMinPay(self):
		if self.override['engage']:
			odds = self.override['odds']
			odds = map(lambda x: x / 100., odds)
		else:
			odds = self.odds
				
		#returns the minimum amount of money that can be one
		minpay = self.seed
		subtractor = self.rounds * self.betsizes[-1] * (1-sum(odds))
		for j in range(0, len(self.payouts)):
			minpay = minpay + self.getWinnings(j, 0)
		minpay = minpay - subtractor
		return minpay

	def createInitCombos(self):
		#create combos from available symbols
		combos = []

		for s in self.symbols:
			combos.append([s]*self.numReels)

		combos.append([s, s, cfg.IM_EMPTY*(self.numReels-2)])
		combos.append([s, cfg.IM_EMPTY*(self.numReels-2)])
		self.combos = combos[0:self.numPayouts]
		self.pads = [0] * self.numPayouts

	def setPayoff(self, i, value, combo):
		#set the value of a particular payoff given an index, value, and combination of symbols [str]
		self.combos[i] = combo
		self.payoffs[i] = value

	def hasDuplicates(self):
		#returns whether there are duplicate entries in the combo list (a bad thing)
		dupes = False
		for c in self.combos:
			if self.combos.count(c) > 1:
				dupes = True

		return dupes

	def setBets(self, betsizes, debt, currency):
		self.betsizes = betsizes
		self.debt = debt
		self.currency = currency

	def preserve(self):
		f = open("%s" % self.name, "w")
		pickle.dump(self, f)
		f.close()

	def __str__(self):
		output = ""
		for i in range(0, len(self.payouts)):
			line = ""
			for j in range(0, len(self.betsizes)):
				line = "%s %s" % (line, round(self.getWinnings(i, j), 2))
			output="%s\n%s" % (output, line)

		for i in range(0, len(self.combos)):
			output = "%s\n%s" % (output, self.getPayoff(i))

		for i, j in zip(self.payouts, self.payoutOdds):
			output="%s\n%s, %s" % (output, i, j)

		return output
