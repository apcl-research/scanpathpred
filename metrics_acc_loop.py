import argparse
import os
from thefuzz import fuzz
import re

def fil(com):
    sremove = com.split(">",1)[1] # remove start tag
    eremove = sremove.rsplit("<",1)[0] #remove end tag
    ret= eremove.strip()
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
        
        score = fuzz.ratio(pred_val, ref_val)
        total_score += score
    total_score /= total_fun
    return total_score

def compute_ratiolist(preds, refs):
    ref_fids = list(refs.keys())
    ref_vals = list(refs.values())
    total_score = list()

    for i in range(len(ref_fids)):
        ref_fid = ref_fids[i]
        ref_val = ref_vals[i]
        total_fun = len(ref_fids)
        pred_val = preds[ref_fid]
        score = fuzz.ratio(pred_val, ref_val)
        total_score.append(score/100)
    return total_score


def main(input_file, reffilename,typeout):
    

    
    if input_file is None:
        print('Please provide an input file to test')
        exit()

    

    preds = dict()
    predicts = open(input_file, 'r')

    n_all_fun = 0
    for c, line in enumerate(predicts):
        n_all_fun += 1
        (fid, pred) = line.split('\t')[0], line.split('\t')[1]
        fid = int(fid)
        pred = fil(pred)
        preds[fid] = pred
    predicts.close()

    refs = dict()
    targets = open(reffilename, 'r')

    for line in targets:
        (fid, com) = line.split('\t')[0], line.split('\t')[1]
        fid = int(fid)
        com = fil(com)
        if com.isspace():  #skip over fids where refernce is just whitespace
            continue
        refs[fid] = com
    if typeout == 'mean':
        ratio = round(compute_ratio(preds, refs)/100, 2) 
    elif typeout == 'list':
        ratio = compute_ratiolist(preds,refs)
    
    return ratio
    

