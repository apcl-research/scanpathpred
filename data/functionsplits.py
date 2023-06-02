import sys
import os
from tqdm import tqdm
import numpy as np
import tiktoken
from datasets import load_dataset # huggingface datasets
import shutil
import pickle

import re

testfid = int(sys.argv[1])

valfid = int(sys.argv[2])

filedir = 'eyesum/'

filelist = os.listdir(filedir)

datadir = f'byFunction_{str(testfid)}/'
traindir = f'eyeseq_train/'
testdir = f'eyeseq_test/'
valdir = f'eyeseq_val/'
current_directory = os.getcwd()
new_directory = os.path.join(current_directory, datadir)
train_directory = os.path.join(new_directory, traindir)
test_directory = os.path.join(new_directory, testdir)
val_directory = os.path.join(new_directory, valdir)

if not os.path.exists(new_directory):
   os.makedirs(new_directory)
   os.makedirs(train_directory)
   os.makedirs(test_directory)
   os.makedirs(val_directory)

txtfiles = list()
valtxtfiles = list()
testfiles = list()

num_proc = 8
for filename in filelist:
    if not filename.endswith('.txt'):
        continue

    fid = filename.split(".")[0].split("_")[1]
    fid = int(fid)
    fpath = filedir+filename

    if fid == testfid:
        shutil.copy(fpath,test_directory+filename) #copying test files into the new test folder for inference - TODO streamline into bin process like train/val
        testfiles.append(fpath)
                        
    elif fid == valfid:
        shutil.copy(fpath,val_directory+filename) 
        valtxtfiles.append(fpath)

    else:
        shutil.copy(fpath,train_directory+filename) 
        txtfiles.append(fpath)


dataset = load_dataset('text', data_files={'train': txtfiles, 'val': valtxtfiles}, sample_by="document")

enc = tiktoken.get_encoding("gpt2")
def process(example):
    ids = enc.encode_ordinary(example['text']) 
    ids.append(enc.eot_token) 
    out = {'ids': ids, 'len': len(ids)}
    return out

tokenized = dataset.map(
    process,
    remove_columns=['text'],
    desc="tokenizing the splits",
    num_proc=num_proc,
)

for split, dset in tokenized.items():
    arr_len = np.sum(dset['len'])
    filename = os.path.join(new_directory, f'{split}.bin')
    dtype = np.uint16 # (can do since enc.max_token_value == 50256 is < 2**16)
    arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

    print(f"writing {filename}...")
    idx = 0
    for example in tqdm(dset):
        arr[idx : idx + example['len']] = example['ids']
        idx += example['len']
    arr.flush()


pf = open(f'{datadir}eyeseq_testref.txt', 'w')


for testfile in tqdm(testfiles):
    fid = testfile.split('/')
    fid = fid[-1]
    fid = fid.split('.')
    fid = fid[0]

    with open(testfile, 'r') as f:
        start = f.read()

    try:
        start = start.replace('\n', '<NL>')
        start = re.search('(TDAT:.*SEQ:) (.*)', start, re.MULTILINE)
        start = start.group(2)
        start = start.replace('<NL>', '\n')
        pf.write(f'{fid}\t{start}\n')
    except AttributeError:
        pf.write(f'{fid}\t<s> none </s>\n')
        continue

    pf.flush()

pf.close()
