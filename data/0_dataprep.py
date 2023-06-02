import pickle
import numpy

fundats = pickle.load(open('/nublar/datasets/jm52m/fundats-j1.pkl', 'rb'))

byParticipant = pickle.load(open("dataParticipant.pkl","rb"))

n = 10

for pid in byParticipant:

    for fid in byParticipant[pid]:

        firstn = byParticipant[pid][fid][:n] # first n fixations with their respective durations

        wordlist = list()
        timelist = list()

        for fixation in byParticipant[pid][fid]:
            wordlist.append(fixation[0])
            timelist.append(fixation[1])
        
        timearray = numpy.array(timelist)
        sort_index = numpy.argsort(timearray)
        
        topn = list()

        for index in sort_index[:10]:
            topn.append([wordlist[index],timelist[index]]) # top n longest fixations in time duration

        try:
            with open(f'eyesum/{pid}_{fid}.txt', 'w') as f:
                first2 = ' '.join([str(x[0]) for x in firstn[:2]])
                f.write(f'TDAT: {fundats[fid]} SEQ: <s> {first2} </s>')
            
        except IndexError as ex:
            print(f'error on participant {pid}, fid {fid}')
            print(byParticipant[pid][fid])
        
        #for tokview in firstn:
        #    print(tokview[0])
        
        #print(firstn) # for every participant, and each function they saw, this will print the first n fixations and their durations
        #print(topn) # for every participant, and each function they saw, this will print the top n longest fixations
        
        #print()
