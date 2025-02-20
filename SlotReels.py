#SlotReels.py
import random
import cfg
import copy

class Slots:
	def __init__(self, reels={}, symbols=[], nms={}):
		self.reels = []
		rkeys = reels.keys()
		rkeys.sort()
		self.numreels = len(reels)
		self.symbols = symbols

		for k in rkeys:
			reel = Reel(reels[k], nms)
			self.reels.append(copy.deepcopy(reel))

	def spin(self, before = 1, after = 1):
		pres = [] 
		winners = []
		stopAt = []
		posts = []
		for r in self.reels:
			pre, sym, post, i = r.spin(before, after)
			pres.append(pre)
			winners.append(sym)
			stopAt.append(i)
			posts.append(post)

		outputList = []


		for j in range(0,before):
			for i in range(self.numreels):
				outputList.append(pres[i][j])

		outputList += winners
		

		for k in range(0,after):
			for l in range(self.numreels):
				outputList.append(posts[l][k])

		return outputList, winners, stopAt
		
	def getWeights(self):
		weights = []
		for s in self.symbols:
			w = []
			for r in self.reels:
				w.append(r.getWeight(s))
			weights.append(w)
		return weights

	def getComboOdds(self, combo):
		odds = 1
		for c, r in zip(combo, self.reels):
			odds *= r.getSymbolOdds(c)
		return odds

	def getNearMissOdds(self):
		odds = 1.
		for r in self.reels:
			odds *= r.getNearMissOdds()
		return odds
		
	def __str__(self):
		output = ""
		for r in self.reels:
			output = "%s%s" % (output, r)

		return output

class Reel:
	def __init__(self, symbols={}, nms={}):
		#symbols are the images which can appear on the stops, stops is a list of which symbols (their indeces) appear when on each reel
		self.symbols = symbols.keys()
		random.seed()
		random.shuffle(self.symbols)
		self.stops = []
		self.nms = nms
		for k in symbols.keys():
			self.stops = self.stops + ([self.symbols.index(k)] * symbols[k])

		#if there will be near misses
		if sum(nms.values()): 
			#add a blank if it's not in the symbol list already
			if cfg.IM_BLANK not in self.symbols:
				self.symbols.append(cfg.IM_BLANK)
			
			blankIndex = self.symbols.index(cfg.IM_BLANK)
			
			for k in nms.keys():
				if nms[k]:
					newstops = []
					stop = self.symbols.index(k)
					#si = self.stops.index(i)
					for stops in self.stops:
						if stops == stop:
							newstops = newstops + ([blankIndex] * nms[k])
							newstops.append(stops)
							newstops = newstops + ([blankIndex] * nms[k])
						else:
							newstops.append(stops)
					self.stops = newstops

	def getNearMissOdds(self):
		#returns the odds of near misses occuring on this reel
		total = 0.
		for k in self.nms.keys():
			if self.nms[k]:
				i = self.symbols.index(k)
				ss = self.stops.count(i)
				total = total + (ss * 2.)
		
		
		odds = total / float(len(self.stops))
		return odds
					
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

	def getWeight(self, s):
		stop = self.symbols.index(s)
		return self.stops.count(stop)
		
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

		return preSymbols, self.symbols[symbolIndex], postSymbols, stopNum

	def __str__(self):
		output = ""
		for s in self.stops:
			output = "%s\n%s" % (output, self.symbols[s])
		return "%s\n" % output
		
s = Slots()
