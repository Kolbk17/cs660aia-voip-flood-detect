import csv

"""
Appends the contents of a temporary csv file to a given csv file
"""
def combine_traces(tempfile, filename):
    with open(filename, 'a') as f:
        with open(tempfile, newline='\n') as t:
            reader = csv.reader(t, delimiter='\t')
            for row in reader:
                line = str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\n'
                f.write(line)

"""
Overwrites a csv file with the contents of a temporary csv file
"""
def set_traces(tempfile, filename):
    with open(filename, 'w+') as c:
        c.write('')
    with open(filename, 'a') as f:
        with open(tempfile, newline='\n') as t:
            reader = csv.reader(t, delimiter='\t')
            for row in reader:
                line = str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\n'
                f.write(line)

"""
Given a csv file in the form: time \t SIP ID \t ...
This function will return a dict object based on the number of times that a unique SIP ID appears
"""
def process_packets(filename):
    sketch = {}
    with open(filename, newline='\n') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            second = row[0]
            name = row[1]
            sketch = make_sketch(sketch, name)
    return sketch

"""
Takes a dict object and a SIP ID, adds the SIP ID if it is not in the dict and assigns the value 1,
otherwise increments the value associated with the SIP ID by 1. Returns the dict.
"""
def make_sketch(sketch, name):
    if name in sketch:
        sketch[name] += 1
    else:
        sketch[name] = 1
    return sketch