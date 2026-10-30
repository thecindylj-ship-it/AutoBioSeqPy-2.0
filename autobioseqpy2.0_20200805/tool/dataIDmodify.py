#/usr/bin/python

import os, sys
#import numpy as np
#import re
helpStr = '''
python tool/dataIDmodify.py examples/T3T4/feature/testT3_AAC_DC.txt ../tryPython/tmpKFold/tmp/tmpOut.txt /any/path/of/file/like/newHeader_001.123 _ 1
'''
def headerAnalysis(fileIn,sep = None, startPos = 0, endPos = None, colSep = ','):
    str1 = None
    str2 = None
    with open(fileIn) as FID:
        for line in FID:
            if line.startswith('#'):
                continue
            header = line.strip().split(colSep)[0]
#            print(line)
#            print(header)
            if sep is None or endPos is None:
                if str1 is None:
                    str1 = header
                else:
                    str2 = header
                    str1 = strOverlapFinder(str1,str2)
                    if len(str1) < 1:
                        return str1
            else:
                eles = header.split(sep)
#                print(eles)
                str1 = sep.join(eles[startPos:endPos])
                return str1 + sep
                    
    return str1
    
def strOverlapFinder(str1,str2):
    subStr = str2
    while len(subStr) > 0:
        if subStr in str1:
            return subStr
        subStr = subStr[:-1]
    return subStr

def fileHeaderReplace(fileIn,fileOut,fileRef,delHeader, colSep = ','):
    refStr = os.path.split(fileRef)[-1]
    outFolder = os.path.split(fileOut)[0]
    try:
        if not os.path.exists(outFolder):
            os.makedirs(outFolder,exist_ok=True)
    except:
        pass
    with open(fileIn) as FID:
        with open(fileOut,'w') as FIDO:
            for line in FID:
                if line.startswith('#'):
                    FIDO.write(line)
                    continue
                eles = line.split(colSep)
                header = eles[0]
                header = refStr + '_' + header.replace(delHeader,'')
                FIDO.write(colSep.join([header]+eles[1:]))
            

def main():
#    fileIn = r'D:\workspace\autoBioSeqpy\examples\T3T4\feature\testT3_AAC_DC.txt'
#    fileOut = r'D:\workspace\tryPython\tmpKFold\tmp\tmpOut.txt'
#    fileRef = r'D:\workspace\autoBioSeqpy\examples\T3T4\feature\trainT3.txt_scale0.6_fold0_train.txt'
#    sep = '_'
    fileIn = sys.argv[1]
    fileOut = sys.argv[2]
    fileRef = sys.argv[3]
    sep = sys.argv[4]
    startPos = 0
    endPos = int(sys.argv[5])
    delHeader = headerAnalysis(fileIn,sep,startPos,endPos)
#    print(delHeader)
    fileHeaderReplace(fileIn,fileOut,fileRef,delHeader)
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    