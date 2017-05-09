import make_sketch as ms

"""
Calculats the percent probablility of an attack based on a single user, given a packet trace.
Probabilities are calculated based on a quadratic function that has been pre-set.
Output os an array of floats representing percent probabilities.
"""
def calc_probability(filename):
    sketch = ms.process_packets(filename)
    probabilities = []
    lst = list(sketch.values())
    for value in lst:
        val = value
        if value >= 7:
            y = 0.1880976*val*val - 2.64461*val + 9.551436
        else:
            y = 0
        probabilities.append(y)
    return probabilities

"""
Calculates the set of probabilities based on given normal user packet traces.
Probabilities are calculated based on the number of times that a specifice event occures within the data.
Percents are used to do a quadratic curve fit to calculate probabilities on future traces.
"""
def set_probabilities(filename):
    packets = ms.process_packets(filename)
    vals = list(packets.values())
    total = len(vals)
    probabilities = {}
    sketch = {}
    for i in range(0, len(vals)):
        sketch = ms.make_sketch(sketch, vals[i])
    keys = sorted(list(sketch.keys()))
    for j in range(0, len(keys)):
        probabilities[keys[j]] = round((sketch[keys[j]] / total) * 100, 3)
    print(total)
    print(probabilities)
    probabilities = reverse(probabilities)
    print(probabilities)

"""
Reverses the calculated event probabilities to account for the fact that, in normal traffic,
events which occure the most frequently are the least likely to be an attack.
"""
def reverse(probabilities):
    vals = sorted(list(probabilities.values()))
    keys = list(probabilities.keys())
    max = vals[len(vals) - 1]
    for i in range(0, len(keys)):
        probabilities[keys[i]] = (max - probabilities[keys[i]])/10
    return probabilities