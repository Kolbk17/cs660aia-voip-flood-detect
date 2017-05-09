from sip_generator import gen_packets
from calc_probability import calc_probability
from flood_detection import FloodDetection
import numpy as np 
import random
import csv
import time 

def output_attacks(attacks, key):
	with open("possible_attacks{0}.csv".format(key), 'a') as output:
		writer = csv.writer(output, delimiter = '\t')
		if(output.tell() == 0):
			writer.writerow(['time_start', 'time_end', 'duration'])
		for k,v in attacks.items():
			x,y = k
			writer.writerow([x, y, v])

"""
This function iterates over the training set and the test set
and operates the estimation freeze mechanisim. When an anomaly 
is detected, the training set freezes and the test is iterated 
upon until end of attack is detected.
"""
def main():
	attacks = {}
	random.seed(time.time())
	key = random.randint(1,1000000)
	aggregate_file = 'aggregate_trace{0}.csv'.format(key)
	mechanisim = FloodDetection(.25, .125, .5, .5, aggregate_file)
	attacks = mechanisim.estimation_freeze(30000, 20)
	output_attacks(attacks, key)

if __name__ == '__main__':
	main()