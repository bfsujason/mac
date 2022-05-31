import os
import shutil
import argparse

from xml.etree.ElementTree import parse

def main():
    parser = argparse.ArgumentParser(description='Convert Intertext to TSV')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input directory for Intertext alignments.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output directory for TSV files.')
    args = parser.parse_args()
    
    make_dir(args.output)
    input_files = get_input_files(args.input)
    for src_file, tgt_file, align_file in input_files:
        out_file = align_file.replace('xml', 'tsv')
        print("Converting {} to {} ...".format(align_file, out_file))
        src_sents = get_sents(os.path.join(args.input, src_file))
        tgt_sents = get_sents(os.path.join(args.input, tgt_file))
        alignments = get_alignments(os.path.join(args.input, align_file))
        write_tsv(src_sents, tgt_sents, alignments, os.path.join(args.output, out_file))

def write_tsv(src_sents, tgt_sents, alignments, out_file):
    tsv = []
    for src_idx, tgt_idx in alignments:
        src_sent = find_sent_by_id(src_idx, src_sents)
        tgt_sent = find_sent_by_id(tgt_idx, tgt_sents)
        tsv.append(src_sent + "\t" + tgt_sent)
    
    with open(out_file, 'wt', encoding="utf-8") as f:
        f.write("\n".join(tsv))

def find_sent_by_id(idx, sents):
    sent = ''
    if len(idx) > 0:
        sent = ' '.join(sents[idx[0]:idx[-1]+1])
    return sent 

def get_alignments(file):
    doc = parse(file)
    links = []
    for link in doc.iterfind('link'):
        tgt_link, src_link = link.get('xtargets').split(';')
        src_bead = parse_link(src_link)
        tgt_bead = parse_link(tgt_link)
        links.append((src_bead, tgt_bead))
    return links
 
def parse_link(link):
    bead = []
    if len(link) > 0:
        bead = [ int(item.split(':')[1]) - 1 for item in link.split(' ')]
    return bead

def get_sents(file):
    doc = parse(file)
    sents = []
    for sent in doc.iterfind('p/s'):
        sents.append(sent.text)
    return sents
    
def get_input_files(dir):
    input_files = []
    for file in os.listdir(dir):
        names = file.split('.')
        if (len(names)) == 4:
            prj, src, tgt, suffix = names
            src_file = '.'.join([prj, src, suffix])
            tgt_file = '.'.join([prj, tgt, suffix])
            input_files.append([src_file, tgt_file, file])
    return input_files
    
def make_dir(dir):
    if os.path.isdir(dir):
        shutil.rmtree(dir)
    os.makedirs(dir, exist_ok=True)  
    
if __name__ == '__main__':
    main()
