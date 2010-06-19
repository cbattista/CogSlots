#SlotReels.py
import random
import cfg
import copy

class Slots:
	def __init__(self, reels=3):
		self.reels = []
		for i in range(0, reels):
			reel = Reel()
			self.reels.append(copy.deepcopy(reel))

	def spin(self):
		pres = [] 
		winners = []
		posts = []
		for r in self.reels:
			pre, sym, post = r.spin()
			pres.append(pre)
			winners.append(sym)
			posts.append(post)
		return pres, winners, posts

	def __str__(self):
		output = ""
		for r in self.reels:
			output = "%s%s" % (output, r)

		return output

class Reel:
	def __init__(self, symbols=[cfg.IM_GOLDBARS, cfg.IM_TREASURECHEST, cfg.IM_BAR, cfg.IM_CHERRIES, cfg.IM_BELL], stops=[]):
		#symbols are the images which can appear on the stops, stops is a list of which symbols (their indeces) appear when on each reel
		self.symbols = symbols
		random.seed()
		random.shuffle(self.symbols)
		if stops:
			self.stops = stops
		else:
			self.stops = range(0, len(symbols)) * 4

	def spin(self, before = 9, after = 2):
		#seed the num generator w the system time
		random.seed()
		#randomly select a stop
		stopNum = random.randrange(0, len(self.stops), 1)
		#which symbol does this correspond with?
		symbolIndex = self.stops[stopNum]

		#also we'll want to see the symbols which precede the selected stop
		if stopNum > before:
			pre = self.stops[stopNum-before-1 : stopNum-1]
		else:
			pre = self.stops[0 : stopNum-1]
			goback = stopNum - before
			pre = pre + self.stops[goback : -1]

		preSymbols = []
		for p in pre:
			preSymbols.append(self.symbols[p])

		#and a few that follow
		if len(self.stops) >= (stopNum + after + 1):
			post = self.stops[stopNum + 1 : stopNum + after + 1]
		else:
			post = self.stops[stopNum + 1 : -1]
			goforward = after - (len(self.stops) - stopNum)
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

