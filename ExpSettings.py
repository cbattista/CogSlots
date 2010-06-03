import pickle

class Payouts:
	def __init__(self, values= [20., 12., 10., 5., 3., 2., 1.], betsizes = [0, 0.01, 0.05, 0.1, 0.25], odds = 85, rounds = 100, seed=5, name = "unnamed"):
		self.values = values
		self.betsizes = betsizes
		self.odds = odds
		self.rounds = rounds
		self.seed = seed
		self.name = name

	def getPayoff(self, i, j):
		#returns the payoff given indeces of the payout size and bet size  
		payout = self.values[i] * self.betsizes[j]
		return payout

	def getWinnings(self, i, j):
		#returns the winnings given indeces of the payout size and bet size  
		op =  self.odds / float(len(self.values))
		winnings = op * self.values[i] * self.betsizes[j]
		return winnings
		
	def getMaxPay(self):
		#returns the maximum amount of money that can be won
		maxpay = self.seed
		subtractor = (self.rounds * self.betsizes[0] * ((100-self.odds)/100.))
		for j in range(0, len(self.values)):
			maxpay = maxpay + self.getWinnings(j, -1) 
		maxpay = maxpay - subtractor
		return maxpay

	def getMinPay(self):
		#returns the minimum amount of money that can be one
		minpay = self.seed
		subtractor = (self.rounds * self.betsizes[-1] * ((100-self.odds)/100.))
		for j in range(0, len(self.values)):
			minpay = minpay + self.getWinnings(j, 0)
		minpay = minpay - subtractor
		return minpay

	def __str__(self):
		output = ""
		for i in range(0, len(self.values)):
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
	def __init__(self, payoffs = [100, 50, 20, 10, 5, 3, 1], symbols = ["gold", "chest", "bar", "cherry", "bell"]):
		self.payoffs = payoffs
		self.symbols = symbols
		self.createCombos()

	def createCombos(self):
		#create combos from available symbols
		combos = []
		for s in self.symbols:
			combos.append([s, s, s])

		combos.append([s, s, None])
		combos.append([s, None, None])
		self.combos = combos

	def setPayoff(self, i, value, combo):
		#set the value of a particular payoff given an index, value, and combintation of symbols [str]
		self.combos[i] = combo
		self.payoffs[i] = value

	def getPayoff(self, i):
		#get a list of 3 imgs and payoff value given an index
		row = [self.combos[i][0], self.combos[i][1], self.combos[i][2], self.payoffs[i]]
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

p = Payouts()
print p

