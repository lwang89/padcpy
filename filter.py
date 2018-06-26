# Apply hysteresis to stream of brain *category* data

# Send each new data point (category name) to us,
# we send back the appropriate new value to use.
# We retain as much data as we need to do the filtering.

# The filter wants to see nsame of the same category
# out of the last ntotal readings
# 	NB if ntotal > 2*nsame and if there is a tie, it will choose arbitrarily
#	But that would be an unlikely parameter choice anyway

import pad

class HystFilter:
	def __init__ (self, nsame=5, ntotal=7):
		self.nsame = nsame
		self.ntotal = ntotal

		# Saves as much recent input data as we'll use,
		# latest value at beginning
		self.data = []

		# Remembers our last output, in case nothing else wins
		self.lastOutput = None

	def process (self, inp):
		self.data.insert (0, inp)

		# Truncate to how many we use
		# BTW this creates new copy, can use "del" to delete in place
		self.data = self.data[:self.ntotal]

		# Count up our data to see if we have a winner
		# This just counts the number of times each brainCategory appears,
		# and returns winner as [count, category]
		# in weird functional programming style
		count = sorted (
			# make pairs of [count, category]
			map (lambda cat:
				     # calculate count for given category
				     [len (list (filter (lambda dat:
						dat==cat, self.data))), cat], pad.brainCategories))[-1]

		# See if we have a winner
		if count[0]>=self.nsame:
			self.lastOutput = count[1]

		# In case just getting started, no data yet
		if self.lastOutput == None:
			self.lastOutput = inp

		# If no winner, then we send same as our last ouput
		return self.lastOutput

#
# SIMPLE UNIT TEST
#

if __name__=="__main__":
	import sys

	myfilter = HystFilter()

	print ("B", "->", myfilter.process("B"))
	print ("B", "->", myfilter.process("B"))
	print ("C", "->", myfilter.process("C"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("B", "->", myfilter.process("B"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("B", "->", myfilter.process("B"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("C", "->", myfilter.process("C"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("A", "->", myfilter.process("A"))
	print ("C", "->", myfilter.process("C"))
	print ("A", "->", myfilter.process("A"))
	print ("C", "->", myfilter.process("C"))
	print ("C", "->", myfilter.process("C"))
	print ("C", "->", myfilter.process("C"))
	print ("C", "->", myfilter.process("C"))
	print ("C", "->", myfilter.process("C"))
	print ("C", "->", myfilter.process("C"))
	print ("C", "->", myfilter.process("C"))
	print ("B", "->", myfilter.process("B"))
