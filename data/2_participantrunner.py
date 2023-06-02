import pickle
import os
import time

pids = pickle.load(open("allpids.pkl","rb"))
lenpids = len(pids)

for i in range(lenpids):
    testpid = pids[i]
    try:
        valpid = pids[i+1]
    except:
        valpid = pids[0] #for the last fid in the list, valfid is the first one.

    os.system(f'python3 participantsplits.py {testpid} {valpid}')
    print(f'{i} out of {lenpids}')
    #time.sleep(10) #i/o wait


