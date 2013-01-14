#!/usr/bin/env python
#TODO dürfen die Wahrscheinlichkeiten hier bedingt sein?
def match(current, crowd):
	return current * crowd + (1 - current) * ((1 - crowd) / 4)

def mismatch(current, crowd):
	return 1 - match(current, crowd)

def error(conf):
	return 1 - conf

def predict(current, crowd, debug):
	"""Calculate predictand for confidence"""
	print("Current confidence: %0.2f, crowd confidence %0.2f" % (current, crowd))
	# new confidence value for matching answers * probability of match
	c_match = 1 - error(current) * error(crowd)
	matched = c_match * match(current, crowd)
	if (debug): print("e_cur %f, e_crowd %f, match %f, result %f" % (error(current), error(crowd), match(current, crowd), c_match))
	# new confidence value for mismatching answer * probabilityof mismatch
	c_mismatch = error(current) * error(crowd)
	mismatched = c_mismatch * mismatch(current, crowd)
	if (debug): print("e_cur %f, e_crowd %f, mismatch %f, result %f" % (error(current), error(crowd), mismatch(current, crowd), c_mismatch))
	# add up
	predicted = matched + mismatched
	print("\tNew confidence if match: %0.2f, if mismatch: %0.2f" % (c_match, c_mismatch))
	print("\tPredicted confidence: %0.2f" % predicted)

for i in range(0, 11):
	for j in range(0, 11):
		predict(float(i) / 10, float(j) / 10, False)

