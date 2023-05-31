import argparse
import os
from thefuzz import fuzz


def fil(com):
    ret = list()
    for w in com:
        if not '<' in w:
            ret.append(w)
    return ret


def compute_ratio(preds, refs):
    ref_fids = list(refs.keys())
    ref_vals = list(refs.values())
    total_score = 0
    
    for i in range(len(ref_fids)):
        ref_fid = ref_fids[i]
        ref_val = ref_vals[i]
        total_fun = len(ref_fids)
        pred_val = preds[ref_fid]
        
        score = 0
        for j in range(len(pred_val)):
            score += fuzz.ratio(pred_val[j], ref_val[j])
        total_score += score / len(pred_val)
    total_score /= total_fun
    return total_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input', type=str, default=None)
    parser.add_argument('--ref-filename', type=str, default='data/eyeseq/eyeseq_testref.txt')
    
    args = parser.parse_args()

    input_file = args.input
    reffilename = args.ref_filename
    
    if input_file is None:
        print('Please provide an input file to test')
        exit()

    preds = dict()
    predicts = open(input_file, 'r')

    n_all_fun = 0
    for c, line in enumerate(predicts):
        n_all_fun += 1
        (fid, pred) = line.split('\t')
        fid = int(fid)
        pred = pred.split()
        pred = fil(pred)
        preds[fid] = pred
    predicts.close()

    refs = dict()
    targets = open(reffilename, 'r')

    for line in targets:
        (fid, com) = line.split('\t')
        fid = int(fid)
        com = com.split()
        com = fil(com)
        refs[fid] = com

        if len(com) < 1:
            continue

    ratio = round(compute_ratio(preds, refs)/100, 2) 

    print(f"score: {ratio}")
    

