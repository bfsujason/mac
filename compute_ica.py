import os
import argparse

import xml.etree.ElementTree as ET
#from nltk.metrics import masi_distance, jaccard_distance

def main():
    parser = argparse.ArgumentParser(description='Inter-coder Agreement Calculator')
    parser.add_argument('-a1', '--anno_1', type=str, required=True, help='Intertext alignment directory for annotator 1.')
    parser.add_argument('-a2', '--anno_2', type=str, required=True, help='Intertext alignment directory for annotator 2.')
    args = parser.parse_args()
    
    anno_1_files = [file for file in sorted(os.listdir(args.anno_1)) if len(file.split('.')) == 4]
    anno_2_files = [file for file in sorted(os.listdir(args.anno_2)) if len(file.split('.')) == 4]
    intersections = 0
    unions = 0
    for anno_1_file, anno_2_file in zip(anno_1_files, anno_2_files):
        alignments_1 = get_alignments(os.path.join(args.anno_1, anno_1_file))
        alignments_2 = get_alignments(os.path.join(args.anno_2, anno_2_file))
        len_intersection = len(alignments_1.intersection(alignments_2))
        len_union = len(alignments_1.union(alignments_2))
        #print("Len_intersection: {}".format(len_intersection))
        #print("Len_union: {}".format(len_union))
        #masi = masi_distance(alignments_1, alignments_2)
        #print("MASI: {}".format(masi))
        intersections += len_intersection
        unions += len_union
   
    jac = intersections / unions
    print("Jaccard Index: {:.3f}".format(jac))
    
def get_alignments(xml_file):
    doc = ET.parse(xml_file)
    links = []
    for link in doc.iterfind('link'):
        tgt_link, src_link = link.get('xtargets').split(';')
        src_bead = parse_link(src_link)
        tgt_bead = parse_link(tgt_link)
        links.append((src_bead, tgt_bead))
    alignments = set([(tuple(x), tuple(y)) for x, y in links])
    return alignments
    
def parse_link(link):
    bead = []
    if len(link) > 0:
        bead = [int(item.split(':')[1]) - 1 for item in link.split(' ')]
    return bead

if __name__ == '__main__':
    main()
