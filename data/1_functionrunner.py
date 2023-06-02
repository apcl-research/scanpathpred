import pickle
import os
import time

fids = pickle.load(open("allfids.pkl","rb"))
lenfids = len(fids)

for i in range(lenfids):
    testfid = fids[i]
    try:
        valfid = fids[i+1]
    except:
        valfid = fids[0] #for the last fid in the list, valfid is the first one.

    os.system(f'python3 functionsplits.py {testfid} {valfid}')
    print(f'{i} out of {lenfids}')
    #time.sleep(10) #i/o wait


