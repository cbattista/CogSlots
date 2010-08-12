#SlotReels.py
import random
import cfg
import copy

class Slots:
	def __init__(self, reels={}):
		self.reels = []
		rkeys = reels.keys()
		rkeys.sort()
		self.numreels = len(reels)
		for k in rkeys:
			reel = Reel(reels[k])
			self.reels.append(copy.deepcopy(reel))

	def spin(self, before = 1, after = 1):
		pres = [] 
		winners = []
		posts = []
		for r in self.reels:
			pre, sym, post = r.spin(before, after)
			pres.append(pre)
			winners.append(sym)
			posts.append(post)

		outputList = []


		for j in range(0,before):
			for i in range(self.numreels):
				outputList.append(pres[i][j])

		outputList += winners
		

		for k in range(0,after):
			for l in range(self.numreels):
				outputList.append(posts[l][k])

		return outputList, winners

	def getComboOdds(self, combo):
		odds = 1
		for c, r in zip(combo, self.reels):
			odds *= r.getSymbolOdds(c)
		return odds

	def __str__(self):
		output = ""
		for r in self.reels:
			output = "%s%s" % (output, r)

		return output

class Reel:
	def __init__(self, symbols={}):
		#symbols are the images which can appear on the stops, stops is a list of which symbols (their indeces) appear when on each reel
		self.symbols = symbols.keys()
		random.seed()
		random.shuffle(self.symbols)
		self.stops = []
		for k in symbols.keys():
			self.stops = self.stops + ([self.symbols.index(k)] * symbols[k])

	def getIndex(self, i):
		#returns the first symbol on the reel
		
		if i >= len(self.stops):
			return

		output = self.symbols[self.stops[i]]
		return output

	def getOdds(self):
		#returns a dictionary of the odds of each symbol on the reel
		d = {}
		for s in self.symbols:
			d[s] = self.getSymbolOdds(s)
		return d

	def getSymbolOdds(self, symbol):
		#returns the odds f a given symbol coming up, if i not provided returns the odds of each
		if symbol == cfg.IM_EMPTY:
			return 1

		i = self.symbols.index(symbol)
		howmany = self.stops.count(i)
		odds = float(howmany) / float(len(self.stops))
		return odds

	def spin(self, before = 2, after = 1):
		#seed the num generator w the system time
		random.seed()
		#randomly select a stop
		stopNum = random.randrange(0, len(self.stops) - 1, 1)
		#which symbol does this correspond with?

		symbolIndex = self.stops[stopNum]

		#also we'll want to see the symbols which precede the selected stop
		pre = []

		if stopNum >= before:
			pre = self.stops[stopNum-before : stopNum]
		elif stopNum == 0:
			pre = self.stops[-before : -1] + [self.stops[-1]]
		else:
			#pre = self.stops[0 : stopNum]
			goback = len(self.stops) - stopNum - before
			pre = pre + self.stops[goback : -1]

		preSymbols = []

		for p in pre:
			preSymbols.append(self.symbols[p])

		#and a few that follow
		if len(self.stops) >= (stopNum + after + 1):
			post = self.stops[stopNum + 1 : stopNum + after + 1]
		else:
			post = self.stops[stopNum + 1 : -1]
			goforward = after - len(self.stops) - stopNum
			post = post + self.stops[0 : goforward]

		postSymbols = []

		for p in post:
			postSymbols.append(self.symbols[p])

		return preSymbols, self.symbols[symbolIndex], postSymbols

	def __str__(self):
		output = ""
		for s in self.stops:
			output = "%s\n%s" % (output, self.symbols[s])
		return "%s\n" % output

s = Slots()