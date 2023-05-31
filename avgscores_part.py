import matplotlib.pyplot as pl
import numpy as np
from statistics import mean

scores = list()


with open("byParticipantAllPairs.txt","r") as f:
    for line in f.readlines():
        l = line.split("\t")
        newl = l[1].replace("[","").replace("]","")
        newl = newl.split(",")
        scorelist = [float(x) for x in newl]
        scores.extend(scorelist)


print(mean(scores))













































