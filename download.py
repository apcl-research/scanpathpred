from huggingface_hub import hf_hub_download, snapshot_download
import fire

def main(repo_id:str = 'apcl/java52m', # the repo that you want to download the file
        filename:str='',     # if you only want to download a single file, specify the name of that file
        local_dir:str='jam_eyeseq', # the local directory for the dataset file
        repo_type:str='None' # set to dataset if you want to download file from dataset repo
        ):
    if(filename==''):
        snapshot_download(repo_id=repo_id, local_dir=local_dir, repo_type=repo_type)
    else:
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir = local_dir, repo_type=repo_type)

if __name__=='__main__':
    fire.Fire(main)

