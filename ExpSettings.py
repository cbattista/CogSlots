import pickle
import cfg

class Payouts:
	def __init__(self, payouts = [20., 12., 10., 5., 3., 2., 1.], betsizes = [1, 2, 5, 10, 50], odds = 85, rounds = 100, seed=20):
		self.payouts = payouts
		self.betsizes = betsizes
		self.odds = odds
		self.rounds = rounds
		self.seed = seed

	def getPayoff(self, i, j):
		#returns the payoff given indeces of the payout size and bet size  
		payout = self.payouts[i] * self.betsizes[j]
		return payout

	def getPayoffRow(self, i):
		#returns the payoff row for a given payout size
		payouts = []
		for b in self.betsizes:
			payouts.append(self.payouts[i] * b)
		return payouts

	def getWinnings(self, i, j):
		#returns the winnings given indeces of the payout size and bet size  
		op =  self.odds / float(len(self.payouts))
		winnings = op * self.payouts[i] * self.betsizes[j]
		return winnings
		
	def getMaxPay(self):
		#returns the maximum amount of money that can be won
		maxpay = self.seed
		subtractor = (self.rounds * self.betsizes[0] * ((100-self.odds)/100.))
		for j in range(0, len(self.payouts)):
			maxpay = maxpay + self.getWinnings(j, -1) 
		maxpay = maxpay - subtractor
		return maxpay

	def getMinPay(self):
		#returns the minimum amount of money that can be one
		minpay = self.seed
		subtractor = (self.rounds * self.betsizes[-1] * ((100-self.odds)/100.))
		for j in range(0, len(self.payouts)):
			minpay = minpay + self.getWinnings(j, 0)
		minpay = minpay - subtractor
		return minpay

	def __str__(self):
		output = ""
		for i in range(0, len(self.payouts)):
			line = ""
			for j in range(0, len(self.betsizes)):
				line = "%s %s" % (line, round(self.getWinnings(i, j), 2))
			output="%s\n%s" % (output, line)
		return output

	def preserve(self):
		#preserves the payouts table as a pickled file with extension .payout
		f = open("%s.payout" % self.name, "w")
		pickle.dump(self, f)
		f.close()

class Symbols:
	def __init__(self, payoffs = [20., 12., 10., 5., 3., 2., 1.], symbols = [cfg.IM_GOLDBARS, cfg.IM_TREASURECHEST, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL]):
		self.payoffs = payoffs
		self.symbols = symbols
		self.createCombos()

	def createCombos(self):
		#create combos from available symbols
		combos = []
		for s in self.symbols:
			combos.append([s, s, s])

		combos.append([s, s, cfg.IM_EMPTY])
		combos.append([s, cfg.IM_EMPTY, cfg.IM_EMPTY])
		self.combos = combos

	def setPayoff(self, i, value, combo):
		#set the value of a particular payoff given an index, value, and combination of symbols [str]
		self.combos[i] = combo
		self.payoffs[i] = value

	def getPayoff(self, i):
		#get a list of 3 imgs and payoff value given an index
		if len(self.payoffs) > i:
			row = [self.combos[i][0], self.combos[i][1], self.combos[i][2], self.payoffs[i]]
		else:
			row = ""
		return row

	def hasDuplicates(self):
		#returns whether there are duplicate entries in the combo list (a bad thing)
		dupes = False
		for c in self.combos:
			if self.combos.count(c) > 1:
				dupes = True

		return dupes

	def __str__(self):
		output = ""		
		for i in range(0, len(self.combos)):
			output = "%s\n%s" % (output, self.getPayoff(i))
		return output

class Bets:
	def __init__(self, rounds=100, debt=False, seed=20, currency="Credits", betsizes = [1, 2, 5, 10, 50]):
		self.rounds = rounds
		self.debt = debt
		self.seed = seed
		self.currency = currency
		self.betsizes = betsizes

	def __str__(self):
		output = "Rounds : %s\nDebt : %s\nSeed : %s\nCurrency : %s\nBetsizes : %s" % (self.rounds, self.debt, self.seed, self.currency, self.betsizes)
		return output

class Odds:
	def __init__(self, odds="85", auto=True, kind="equal", payouts=[20., 12., 10., 5., 3., 2., 1.]):
		self.odds = odds
		self.kind = kind
		self.payouts = payouts
		self.payoutOdds = []
		self.setAutoOdds()

	def setAutoOdds(self):
		num = len(self.payouts)

		if self.kind=="equal":
			for i in range(0, num):
				self.payoutOdds.append(self.odds / num)
		elif self.kind=="linear":
			for p in self.payouts:
				self.payoutOdds.append((1./float(p)/max(self.payouts)) * self.odds)
			

	def setCustomOdds(self):
		pass

	def __str__(self):
		output = ""
		for i, j in zip(self.payouts, self.payoutOdds):
			output="%s\n%s, %s" % (output, i, j)
		return output

class Settings:
	def __init__(self, name="unnamed", betsizes=[], payouts=[20., 12., 10., 5., 3., 2., 1.], symbols=[], rounds=100, winOdds=85, seed=20):
		#Main class with which to access and set experimental settings (Bets, Symbols, Payouts)
		self.name = name
		self.winOdds = winOdds
		
		self.symbol_imgs = symbols
		self.payouts = payouts
		self.seed = seed
		self.rounds = rounds
		self.setBets(betsizes, rounds, seed)

	def setBets(self, betsizes, debt, currency):
		#set bets, set payouts
		if betsizes:
			self.bets = Bets(self.rounds, debt, self.seed, currency, betsizes)
		else:
			self.bets = Bets(rounds=self.rounds, seed=self.seed)
		self.setPayouts(self.payouts)

	def setPayouts(self, payouts):
		#set payouts, set symbols
		if payouts:
			self.payoffs = Payouts(payouts = payouts, rounds = self.bets.rounds, seed = self.bets.seed, betsizes = self.bets.betsizes, odds = self.winOdds)
		else:
			self.payoffs = Payouts(rounds = self.bets.rounds, seed = self.bets.seed, betsizes = self.bets.betsizes, odds = self.odds)
		self.setOdds()
		self.setSymbols()

	def setOdds(self, auto=True, kind="equal"):
		self.odds = Odds(self.winOdds, auto, kind, self.payoffs.payouts)

	def setSymbols(self):
		if self.symbol_imgs:
			self.symbols = Symbols(payoffs = self.payoffs.payouts, symbols=self.symbols_imgs)
		else:
			self.symbols = Symbols(payoffs = self.payoffs.payouts)

	def preserve(self):
		f = open("%s.set" % self.name, "w")
		pickle.dump(self, f)
		f.close()

	def __str__(self):
		output = "%s\n%s\n%s\n%s" % (self.bets, self.payoffs, self.symbols, self.odds)
		return output

s = Settings()
print s
s.setBets([0, 1, 5, 10], 50, 2) 
s.setPayouts([10, 8, 5, 2, 1, 1])

print s
s.preserve()

	
