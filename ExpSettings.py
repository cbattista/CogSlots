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

	def printTable(self):
		#prints the payout table to the terminal
		for i in range(0, len(self.values)):
			line = ""
			for j in range(0, len(self.betsizes)):
				line = "%s %s" % (line, round(self.getWinnings(i, j), 2))
			print line				

	def preserve(self):
		#preserves the payouts table as a pickled file with extension .payout
		f = open("%s.payout" % self.name, "w")
		pickle.dump(self, f)
		f.close()


