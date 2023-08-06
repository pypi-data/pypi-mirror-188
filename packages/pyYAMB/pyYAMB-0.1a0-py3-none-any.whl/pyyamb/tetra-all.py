#!/usr/bin/env python3
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
import os
from collections import Counter
import re
import regex

def tetra_substr(seq):
	i = 0
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	l = len(seq)
	d = {}
	while i < l-3:
		word = seq[i:i+4]
		d[word] = d.get(word, 0) + 1
		i+=1
	
	return "\t".join([str(d.get(i,0)) for i in tetras])


def tetra_count(seq):
	i = 0
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	l = len(seq)
	d = {}
	words = [seq[i:i+4] for i in range(l-3)]
	cnt = Counter(words)

	return "\t".join([str(cnt.get(i,0)) for i in tetras])


def tetra_re(seq):
	i = 0
	d = {}
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	patterns = [(i, re.compile(i)) for i in tetras]
	for (i,j) in patterns:
		d[i] = (len(j.findall(str(seq))))

	return "\t".join([str(d.get(i,0)) for i in tetras])
	

def tetra_rere_compile(seq):
	i = 0
	d = {}
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	patterns = [(i, re.compile("(?=(%s))" % i)) for i in tetras]
	for (i,j) in patterns:
		d[i] = (len(j.findall(str(seq))))

	return "\t".join([str(d.get(i,0)) for i in tetras])

def tetra_rere(seq):
	i = 0
	d = {}
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	patterns = [(i, r'(?=(%s))' % i) for i in tetras]
	for (i,j) in patterns:
		d[i] = (len(re.findall(j, str(seq))))

	return "\t".join([str(d.get(i,0)) for i in tetras])


def tetra_regex(seq):
	i = 0
	d = {}
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	patterns = [(i, regex.compile(i)) for i in tetras]
	for (i,j) in patterns:
		d[i] = len(regex.findall(j, str(seq), overlapped=True))

	return "\t".join([str(d.get(i,0)) for i in tetras])

def tetra_regex_generator(seqlist):
	verbose = True
	if verbose: print("Calculating tetranucleotide composition:")
	acgt = ['A','C','G','T']
	tetras = [f"{a}{b}{c}{d}" for a in acgt for b in acgt for c in acgt for d in acgt]
	patterns = [(i, regex.compile(i)) for i in tetras]
	OF = open("tetra.new.csv", 'w')
	for (id, seq) in seqlist:
		d={}
		for (i,j) in patterns:
			d[i] = len(regex.findall(j, str(seq), overlapped=True))
		seq = seq[::-1]
		for (i,j) in patterns:
			d[i] = d.get(i, 0) + len(regex.findall(j, str(seq.reverse_complement()), overlapped=True))
		p = "\t".join([str(d.get(i,0)) for i in tetras])
		print(f"{id}\t{p}", file=OF)
	OF.close()


def main(use_generator=True):
	filename = sys.argv[1]
	if use_generator:
		g = ((record.id, record.seq) for record in SeqIO.parse(filename, "fasta"))
		tetra_regex_generator(g)
	else:
		OF = open("tetra.csv", 'w')
		i = 0
		for record in SeqIO.parse(filename, "fasta"):
			p = tetra_regex(record.seq)
			#p = tetra_rere_compile(record.seq)
			#p = tetra_substr(record.seq)
			#p = tetra_count(record.seq)
			print(f"{record.id}\t{p}", file=OF)
			#print(record.seq)
			if i % 1000 == 0: print(i)
			i+=1
		OF.close()

if __name__ == '__main__':
	use_generator = True
	main(use_generator)

