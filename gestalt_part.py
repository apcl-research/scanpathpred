import pickle
from metrics_seq_loop import main
import argparse


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--all-id-filename', type=str, default='/nublar/eyeseq_data/allpids.pkl')
    parser.add_argument('--out-filename', type=str, default='byParticipantAllPairs.txt')
    #parser.add_argument('ref-dir', type=str. default='/nublar/eyeseq_data/')
    #parser.add_argument('pred-dir', type=str, default='/nublar/eyeseq_preds/')
    
    args = parser.parse_args()
    all_id_filename = args.all_id_filename
    out_filename = args.out_filename
    #ref_dir = args.ref_dir
    #pred_dir = args.pred_dir


    
    all_id = pickle.load(open(all_id_filename,'rb'))

    f = open(out_filename, 'w')
    
    for id in all_id:
        reffilename = f'/nublar/eyeseq_data4/byParticipant_{id}/eyeseq_testref.txt'
        predfilename = f'predictions/eyeseqbyParticipant_{id}/predict_jam_eyeseq.txt'
        score = main(predfilename,  reffilename,'list')
        f.write(f'{id}\t{score}\n')
    f.close()





