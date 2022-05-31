# bfsujason@163.com

import os
import argparse

import xml.etree.ElementTree as ET

def main():
    parser = argparse.ArgumentParser(description='Mark up disagreements between annotators')
    parser.add_argument('-a1', '--anno_1', type=str, required=True, help='Intertext alignment file for annotator 1.')
    parser.add_argument('-a2', '--anno_2', type=str, required=True, help='Intertext alignment file for annotator 2.')
    args = parser.parse_args()
    
    alignments_1 = get_alignments(args.anno_1)
    alignments_2 = get_alignments(args.anno_2)
    
    diff_1 = find_diff(alignments_1, alignments_2)
    diff_2 = find_diff(alignments_2, alignments_1)
    
    mark_diff(diff_1, args.anno_1)
    mark_diff(diff_2, args.anno_2)

def mark_diff(diff, xml_file):
    doc = ET.parse(xml_file)
    print(diff)
    i = 0
    for link in doc.iterfind('link'):
        link.attrib.pop('mark', None)
        if i in diff:
            link.set('mark', '1')
        i = i + 1  
    doc.write(xml_file)

def find_diff(alignments_1, alignments_2):
    idxs = []
    anno_1 = set([(tuple(x), tuple(y)) for x, y in alignments_1])
    anno_2 = set([(tuple(x), tuple(y)) for x, y in alignments_2])
    diff = list(anno_1 - anno_2)
    diff = [(list(x), list(y)) for x, y in diff]
    idxs = find_idxs(diff, alignments_1)
    return idxs

def find_idxs(links, alignments):
    idxs = []
    for link in links:
        idx = alignments.index(link)
        idxs.append(idx)   
    return sorted(idxs)

def get_alignments(xml_file):
    doc = ET.parse(xml_file)
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
    
if __name__ == '__main__':
    main()
