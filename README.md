# Replication Package for "Modeling Programmer Attention as Scanpath Prediction" under reviw at ASE-NIER 2023

##Step 0 for all options: Create the dataset for experiment(s) at custom scan length 'n' using series of scripts in /data folder
First, make an empty directory called "eyesum" inside the data directory and run the following script from the data directory:
```
python3 0_dataprep.py
```
This processes the scanpath pickle file into individual text files for gpt tokenization. Then, you can run either:
```
python3 1_functionrunner.py
```
and/or:
```
python3 2_participantrunner.py
```
respectively to generate test/train/val bins for entire method-holdout and participant-holdout experiments respectively. At the end of these scripts you have several folders inside the data directory named byFunction_XXXXX and byParticipant_XXXX for each of the holdout experiments.

To be able to finetune the pre-trained jam model pleaee download it from [here](https://huggingface.co/apcl/jam) into a new directory named jam.

## Option 1: Run experiment for all holdouts 

There are 95 experiments for each scanpath length, this requires a Ampehere series GPU or better with atleast 16 GB of VRAM.

### Step 1: Finetuning and Inference

Our paper presents results from 95 experiments concurrently, therefore to reduce disk data space we do not store the weights or model for each run, which would be around 400GB in total. Instead our script automated the process of training and inference for each holdout experiment and saves only the small prediction files
```
time python3 multitrainer.py
```
inside this script, please adjust the location to the dataset as well as prediction directory.

Disclaimer : torchrun node flag --rdzv-endpoint=localhost:4444 needs a new port value if you wish run more than one instance on a single workstation to avoid same model weights being updated by separate experiments.

### Step 2: Metrics
To compute levenshtein metrics over all pairs for the method-holdout experiments run:
```
python3 levensthein_func.py
```
To compute levenshtein metrics over all pairs for the participant-holdout experiments run:
```
python3 levenshtein_part.py
```
These scripts produce a text file for each method-holdout and participant-holdout experiments, with all pair scores per method/participant. We also have ```avgscores_func.py``` and ```avgscores_part.py``` to print the mean of these scores.

Similar scripts are available for gestalt scores, please note the text files have the same name and are overwritten so you may run one metric at a time or change the file names within either script.

## Option 2: Partition dataset to train-val-test and run a single experiment (not in the paper)

To partition a single train-val-test split and customize the experiment, you can run the following scripts.

### Step 1: Custom Data
Run the following scripts from the data directory to create individual custom method-holdout and participant-holdout datasets:
```
python3 functionsplits.py {testfid} {valfid}
```
and

```
python3 participantsplits.py {testpid} {valpid}
```
Here the script excepts a single id for method or participant for each test and validation set to remove from all samples in /eyesum directory. Alternatively you can change this to use a list of ids for a bigger test/val set inside each script.

### Step 2: Single Finetuning
To finetune a single model, download the jam model from [here](https://huggingface.co/apcl/jam) into a new jam_eyeseq directory or copy from the jam directory if downloaded above. Note, the weights are overwritten during training so this directory cannot be for multiple experiments. Then run:

```
CUDA_DEVICE_ORDER='PCI_BUS_ID' CUDA_VISIBLE_DEVICES='3' OMP_NUM_THREADS=4 time torchrun --rdzv-backend=c10d --rdzv-endpoint=localhost:4444 --nnodes=1 --nproc_per_node=1 train.py config/finetune_eyeseq.py --dataset=/nublar/eyeseq_data4/{dirname}/
```
where {dirname} is the data directory for the experiment generated above.

### Step 3: Single Inference
```
CUDA_DEVICE_ORDER='PCI_BUS_ID' CUDA_VISIBLE_DEVICES='3' OMP_NUM_THREADS=4 time torchrun --rdzv-backend=c10d --rdzv-endpoint=localhost:4444 --nnodes=1 --nproc_per_node=1 sample_eyeseq.py --out_dir=jam_eyeseq --dataset=/nublar/eyeseq_data4/{dirname}/
```
### Step 4: Single Metrics

The way to compute metrics for single inference is same as the the multi experiment, by having a single folder in the predictions directory. Please refer to [Metrics](# Step 2: Metrics) above.
