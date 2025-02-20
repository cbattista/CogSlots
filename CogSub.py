import time
import pickle
import os

class Subject:
	def __init__(self, s_id="000", age=0, sex="unknown", hand="unknown", session=0, expname="unnamed"):		
		self.s_id = s_id
		self.age = age
		self.sex = sex
		self.hand = hand
		self.date = time.strftime("%d_%b_%y_%I_%M%p")
		self.session = session
		self.expname = expname
		#create dictionary to hold trial results
		self.results = {}
		self.fpath = ""

	def inputData(self, trial, condition, value):
		trial = str(trial)
		if self.results.has_key(trial):
			data = self.results[trial]
			data[condition] = value
			self.results[trial] = data
		else:
			data = {}
			data[condition] = value
			self.results[trial] = data					


	def printData(self):	
		if not self.fpath:
			fname = "%s_%s_%s %s.csv" % (self.expname, self.s_id, self.session, self.date)
			fpath = os.path.join(os.getcwd(), fname)
		else:
			fpath = self.fpath
		
		trials = self.results.keys()
		intTrials = []
		for t in trials:
			intTrials.append(int(t))
		intTrials.sort()
		trials = []
		for t in intTrials:
			trials.append(str(t))
		f = open(fpath, "w")
		for t in trials:
			line = t
			trial = self.results[t]
			trialKeys = trial.keys()
			trialKeys.sort()
			header = "trial"
			for tk in trialKeys:
				header = "%s,%s" % (header, tk)
				line = "%s,%s" % (line, trial[tk])
			header = header + "\n"			
			line = line + "\n"
			if t == "1":
				f.write(header)
			f.write(line)
		f.close()

	def preserve(self):
		if not self.fpath:
			fname = "%s_%s.cogsub" % (self.s_id, self.expname)
			fpath = os.path.join(os.getcwd(), fname)
		else:
			fpath = self.fpath
			fpath = fpath.replace(".csv", "")
			fpath = fpath + ".cogsub"
		f = open(fpath, "a")
		pickle.dump(self, f)
		f.close()


