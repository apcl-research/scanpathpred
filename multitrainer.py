import os
import sys
import pickle
import time


dirlist = os.listdir('/nublar/eyeseq_data/')


for dirname in dirlist:
    if 'byFunction' not in dirname and 'byParticipant' not in dirname:
        continue

    os.system("cp -r jam/ jam_eyeseq/") #copy outdir

    os.system(f"CUDA_DEVICE_ORDER='PCI_BUS_ID' CUDA_VISIBLE_DEVICES='3' OMP_NUM_THREADS=4 time torchrun --rdzv-backend=c10d --rdzv-endpoint=localhost:4444 --nnodes=1 --nproc_per_node=1 train.py config/finetune_eyeseq.py --dataset=/nublar/eyeseq_data4/{dirname}/")

    time.sleep(30) # wait 30 secs before inferring

    os.system(f"CUDA_DEVICE_ORDER='PCI_BUS_ID' CUDA_VISIBLE_DEVICES='3' OMP_NUM_THREADS=4 time torchrun --rdzv-backend=c10d --rdzv-endpoint=localhost:4444 --nnodes=1 --nproc_per_node=1 sample_eyeseq.py --out_dir=jam_eyeseq --dataset=/nublar/eyeseq_data4/{dirname}/")
    
    os.system("rm -r jam_eyeseq/ ")  #get rid of trained copy




















































































