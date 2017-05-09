from sip_generator import gen_packets, set_attack_seconds
from calc_probability import calc_probability
from make_sketch import combine_traces
from threshold import calculate_hellinger,calculate_threshold
import numpy as np
import time
import copy

class FloodDetection(object):

	"""
	Initializes an estimation freeze mechanisim with the specified 
	SIP attribute stream. There are also four tunable parameters 
	initialized on startup for use when adjusting the dynamic 
	threshold. These are as follows: 
	1) a              --> alpha
	2) b              --> beta
	3) l              --> lambda: multiplication factor, used to set a safe margin for threshold.
	4) u              --> omega: multiplication factor, used to set a safe margine for threshold.
	5) aggregate_file --> File that contains all the traces for one round of the simulation
	"""
	def __init__(self,a, b, l, u, aggregate_file):
		self.aggregate_file = aggregate_file
		self.a = a
		self.b = b
		self.l = l
		self.u = u

	"""
	Estimation_freeze mechanisim that operates with a second of traffic at a time. Probability vectors 
	are gathered using calc_probability from calc_probability.py, and the mechanisim works by comparing the
	calculated hellinger's distance with the dynamic threshold. If the hellinger's distance is larger at that point,
	then the second's trace is flagged. Here we are looking for consecutive seconds of possible malicious traffic. 
	"""
	def estimation_freeze(self, seconds, cutoff):
		timer = 0 
		ending_time = 0 
		starting_time = 0
		attack_duration = 0
		hellinger = 0.0
		current_prob = 0.0
		previous_prob = 0.0
		stream = copy.copy(self)
		param_a = stream.a
		param_b = stream.b
		param_l = stream.l 
		param_u = stream.u
		param_agg = stream.aggregate_file
		attacks_disovered = {}
		tempfile = 'current_second.csv'
		attack_times = set_attack_seconds(seconds, 1000)
		while(timer < seconds):
			if attack_times.__contains__(timer):
				result = gen_packets(timer, tempfile, 200, 50, 25, 75, 60)
			else:
				result = gen_packets(timer, tempfile, 200, 50, 25, 75)
			combine_traces(tempfile, param_agg)
			if(timer == 0):
				previous_prob = calc_probability(tempfile)
				timer += 1
			elif(timer == 1):
				current_prob = calc_probability(tempfile)
				hellinger = calculate_hellinger(current_prob, previous_prob)
				threshold, prev_hellinger, prev_deviation = calculate_threshold(1, 1, hellinger, param_a, param_b, param_l, param_u)
				previous_prob = current_prob
				timer += 1
			else:
				current_prob = calc_probability(tempfile)
				hellinger = calculate_hellinger(current_prob, previous_prob)
				threshold, prev_hellinger, prev_deviation = calculate_threshold(prev_hellinger, prev_deviation, hellinger, param_a, param_b, param_l, param_u)
				previous_prob = current_prob
				if(hellinger > threshold):
					starting_time = timer
					ending_time = starting_time
					while(hellinger > threshold):
						previous_prob = current_prob
						result = gen_packets(timer, tempfile, result[1], 50, 25, 75, 60)
						current_prob = calc_probability(tempfile)
						hellinger = calculate_hellinger(current_prob, previous_prob)
						previous_prob = current_prob
						combine_traces(tempfile, param_agg)
						ending_time += 1
						timer += 1
				else:
					attack_duration = (ending_time - starting_time)
					if(attack_duration > cutoff):
						attacks_disovered[(starting_time, ending_time)] = attack_duration
						timer += 1	
		return attacks_disovered


