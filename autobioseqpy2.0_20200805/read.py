import re
import numpy as np


def openFile(input_file): 
    with open(input_file) as f:
         contents = f.readlines()
    return contents


def readFasta(inpFile,maxlen):
    _hash = {}
    _seq = []
    _id = []

    for line in open(inpFile):
        if line.startswith('>'):
           name = line.replace('>','').split()[0]
           _id.append(name)
           _hash[name] = ''
        else:
           _hash[name] += line.replace('\n','')

    for i in _hash.keys():
        if len(_hash[i]) <= maxlen:
           Subseq = _hash[i]
        else:
           Subseq = _hash[i]
        _seq.append(Subseq)

    return _seq, _id
