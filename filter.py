# Apply hysteresis to stream of brain *category* data

# Send each new data point (category name) to us,
# we send back the appropriate new value to use.
# We retain as much data as we need to do the filtering.

# The filter wants to see nsame of the same category in a row,
# except permitting for nexceptions

class HystFilter:
	def __init__ (self, nsame=4, nexceptions=1):
		self.nsame = nsame
		self.nexceptions = nexceptions

		# Saves as much recent input data as we'd ever need,
		# latest value at beginning
		self.data = []

		# Remembers our last output, in case nothing else wins
		self.lastOutput = None

	def process (self, inp):
		self.data.insert (0, inp)

		# Truncate to the max we'll ever need
		# BTW this creates new copy, can use "del" to delete in place
		self.data = self.data[:(self.nsame + self.nexceptions)]

###		NOW count up see if we have nsame of the same
###			if so return that, ie self.lastOutput = xxx
###                	if tied, return most recent? ditto

		# When just getting started, no data yet
		if self.lastOutput == None:
			self.lastOutput = inp

		# If nothing wins, then we end up here with no change from last ouput
		return self.lastOutput

# Simple unit test
import sys

filter = HystFilter()

print ("A", filter.process("A"))
print ("B", filter.process("B"))
print ("C", filter.process("C"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("B", filter.process("B"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("B", filter.process("B"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("C", filter.process("C"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("A", filter.process("A"))
print ("C", filter.process("C"))
print ("A", filter.process("A"))
print ("C", filter.process("C"))
print ("C", filter.process("C"))
print ("C", filter.process("C"))
print ("C", filter.process("C"))
print ("C", filter.process("C"))
print ("C", filter.process("C"))
print ("C", filter.process("C"))
print ("B", filter.process("B"))
