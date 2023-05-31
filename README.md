# Replication Package for "Modeling Programmer Attention as Scanpath Prediction" under reviw at ASE-NIER 2023

Step 0 for all options: Create the dataset for experiment(s) at custom scan length 'n' using series of scripts in /data folder

## Option 1: Run experiment for all holdouts 

There are 95 experiments for each scanpath length, this requires a Ampehere series GPU or better with atleast 16 GB of VRAM.

### Step 1: Training
```
time python3 multitrainer.py
```
inside this script, please adjust the location to the dataset

Disclaimer : torchrun node flag --rdzv-endpoint=localhost:4444 needs a new port value if you wish run more than one instance on a single workstation to avoid same model weights being updated by separate experiments.
### Step 2:


### Step 3:





## Option 2: Partition dataset to train-val-test and run a single experiment
