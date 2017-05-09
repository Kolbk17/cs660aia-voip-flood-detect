import random
import graph_pps
import make_sketch as ms

"""
Assigns a specific range of values within the maximum and minumum packets per second to a percent.
The percent represents the number of packets within a range of the normal distribution.
The percents used are: 0.1, 0.5, 1.7, 3.4, 8.2, 13.0, 23.1
"""
def get_distance(min, max, avg, percents):
    lst = []
    min_range = avg - min
    min_set = min_range / 7
    max_range = max - avg
    max_set = max_range / 7
    j = 0
    for i in range(0, len(percents)):
        lst.append((min + min_set * j, min + min_set * (j + 1)))
        j += 1
    j = 0
    for i in range(0, len(percents)):
        lst.append((avg + max_set * j, avg + max_set * (j + 1)))
        j += 1
    return lst

"""
Uses psuedo random number generators to calculate a value between the minimum and maximum values given,
Then uses a set of probabilities to create a normal distribution of packets per second.
"""
def gen_pps(avg_pack, min_pack=0, max_pack=0):
    percents = [0.1, 0.5, 1.7, 3.4, 8.2, 13.0, 23.1]
    ranges = get_distance(min_pack, max_pack, avg_pack, percents)
    do_pps = True
    if min_pack == 0 and max_pack == 0:
        do_pps = False
        pps = avg_pack
    while do_pps:
        pps = random.randint(min_pack, max_pack)
        percent = random.randrange(0, 231, 1) / 10
        loc = 0
        for i in range(0, len(percents)):
            if percent <= percents[i]:
                loc = i
                break
        if pps < avg_pack:
            if pps >= ranges[loc][0] and pps < ranges[loc][1]:
                break
        elif pps > avg_pack:
            if pps > ranges[13 - loc][0] and pps <= ranges[13 - loc][1]:
                break
        elif pps == avg_pack:
            if pps >= ranges[13 - loc][0] and pps <= ranges[13 - loc][1]:
                break
    return pps

"""
A pseudo packet generator that takes a time second, a csv file to write traces to, the total number of packets to write,
the max, min, and average number of packets to write per second, and a number of attack packets.
First gets the packets per second, while the pps is greater than 0, continue selecting packets for users.
Random numbers are used to mimic network errors, timeouts, and no responses from callee in normal SIP traffic.
Returns the next time second and the number of packets left, so they can be used as parameters for the next iteration.
"""
def gen_packets(timer, tempfile, packets, avg_pack, min_pack=0, max_pack=0, atk=0):
    with open(tempfile, 'w+') as f:
        f.write('')
    pps = gen_pps(avg_pack, min_pack, max_pack)
    total = pps
    timer += 1
    packets -= pps
    while pps > 0:
        sipid = get_sipid()
        accept = False
        gen_inv(tempfile, timer, sipid)
        pps -= 1
        for i in range(0, 3):
            if random.random() < .5:
                gen_inv(tempfile, timer, sipid)
                pps -= 1
        for i in range(0, 2):
            if random.random() < .7:
                gen_acc(tempfile, timer, sipid)
                pps -= 1
                accept = True
        if(accept == True):
            gen_ack(tempfile, timer, sipid)
            pps -= 1
            for i in range(0, 2):
                if random.random() < .5:
                    gen_ack(tempfile, timer, sipid)
                    pps -= 1
            gen_bye(tempfile, timer, sipid)
            pps -= 1
        if atk > 0:
            atk_sipid = get_sipid(True)
            count = random.randint(int(atk/2), atk)
            total += count
            for i in range(0, count):
                gen_inv(tempfile, timer, atk_sipid)
    with open('pps.txt', 'a') as f:
        f.write(str(total) + '\n')
    return (timer, packets)

"""
Set of functions used to write a single packet to a csv file of traces
"""
def gen_inv(tempfile, timer, sipid):
    with open(tempfile, 'a') as f:
        f.write(str(timer) + '\t' + str(sipid) + '\tINV\n')

def gen_acc(tempfile, timer, sipid):
    with open(tempfile, 'a') as f:
        f.write(str(timer) + '\t' + str(sipid) + '\tACC\n')

def gen_ack(tempfile, timer, sipid):
    with open(tempfile, 'a') as f:
        f.write(str(timer) + '\t' + str(sipid) + '\tACK\n')

def gen_bye(tempfile, timer, sipid):
    with open(tempfile, 'a') as f:
        f.write(str(timer) + '\t' + str(sipid) + '\tBYE\n')
"""
Generates a string in the standard SIP ID form of 'name@example.com' by randomly selecting a name, a set of numbers,
and a hostname from the defined arrays.
"""
def get_sipid(attack=False):
    names = ['alice', 'bob', 'carol', 'dave', 'evan', 'fin', 'gale', 'hana', 'ingres', 'jake', 'kely', 'lilly', 'mark',
             'nora', 'ozpin', 'pira', 'quest', 'rose', 'stella', 'tim', 'umbra', 'vic', 'will', 'xeno', 'yarl', 'zest']
    extentions = ['@gmail.com', '@yahoo.com', '@skype.com', '@discord.com', '@hotmail.com', '@sketchyvoip.net']
    n = random.randint(0, len(names)-1)
    e = random.randint(0, len(extentions)-1)
    sipid = str(names[n])
    for i in range(0, 4):
        if random.random() > .7:
            sipid += str(random.randint(0, 9))
    if attack == True:
        sipid += '@attackers_haven.tor'
    else:
        sipid += str(extentions[e])
    return sipid

"""
Sets an array of time seconds of when an attack will occure based on a maximum value and an interval
"""
def set_attack_seconds(max, interval):
    attacks = []
    i = interval
    while i < max:
        attacks.append(i)
        i += interval
    return attacks
