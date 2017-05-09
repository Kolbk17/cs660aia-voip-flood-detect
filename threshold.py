import numpy as np

"""
Calculates the hellinger's distance between two probability distributions.
p --> probability vector of current second.
q --> probability vector of the previous second. 
"""
def calculate_hellinger(p,q):
	if len(p) > len(q):
		for i in range(len(q)-1, len(p)-1):
			q.append(p[i])
	elif len(q) > len(p):
		for i in range(len(p)-1, len(q)-1):
			p.append(q[i])
	return np.sqrt(np.sum(np.sqrt(p) - np.sqrt(q)) **2) / np.sqrt(2)
	

"""
Calculates the dynamic threshold for estimation_freeze mechanisim. The parameters
are as follows:
H_n                --> The average hellinger's distance calculated at the current time interval
S_N                --> The deviation between the average hellinger's distance and the current hellingers distance. 
h_n                --> The current, calculated hellinger's distance for time interval n. 
h_prev             --> The average hellinger's for the previous time interval.
s_prev             --> The deviation between the previous average hellinger's distance and the previous calculated hellinger's distance
"""
def calculate_threshold(h_prev, s_prev, h_n, a, b, l, u):
	H_n = (1 - a) * h_prev + a * h_n
	S_n = (1 - b) * s_prev + b * abs(H_n - h_n)
	dynamic_thresh = (l * H_n) + (u * S_n)
	return (dynamic_thresh, H_n, S_n)