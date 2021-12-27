# This script merge together all the descriptors extracted via iFeature
import os
from src.common import *
from itertools import chain, combinations
from pathlib import Path

import shutil

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

SEQ_DATA = {}
DESCRIPTORS_ORDER = []
TRAINING_SET = "BALANCED_632_LEN6_3DSTRUCT"

TOTAL_Y = 0
TOTAL_N = 0

#Reading TARGET output
with open(TRAINING_PATH+"/"+TRAINING_SET+".csv") as reader:
    reader.readline()
    for SEQ in reader:
        SEQ = SEQ.replace("\n","")
        sData = SEQ.split("\t")        
        if (not sData[0] in SEQ_DATA):
            SEQ_DATA[sData[0]]={}
            SEQ_DATA[sData[0]]["TARGET"]=sData[1]
            if (sData[1]=="Yes"):
                TOTAL_Y+=1
            else:
                if (sData[1]=="No"):
                    TOTAL_N+=1
                    
print("Y:" + str(TOTAL_Y))
print("N:" + str(TOTAL_N))


ALL_DESCRIPTORS = ["YPredStruct","QSOrder","SOCNumber","APAAC","PAAC","CKSAAGP","CKSAAP","NMBroto","Geary","Moran","BINARY","EAAC","AAINDEX","ZSCALE","BLOSUM62","EGAAC","AAC","DPC","DDE","TPC","GAAC","GDPC","GTPC","CTDC","CTDT","CTDD","CTriad","KSCTriad"]
COMBINATIONS = powerset(ALL_DESCRIPTORS)
for descr in COMBINATIONS:
    if (len(descr)==0):
        continue

    INPUT_NAME = "TRAININGSET_"+str(TOTAL_Y+TOTAL_N)
    for d in descr:        
        INPUT_NAME += "_" + d

    print("Generating new set...")
    print(INPUT_NAME)
    

    #Write the header of the complete output
    print("Writing Header...")
    Path("./classificator_inputs/"+INPUT_NAME).mkdir(parents=True, exist_ok=True)
    with open("./classificator_inputs/"+INPUT_NAME+"/"+INPUT_NAME+".txt","w") as writer:
        writer.write("SEQUENCE\t")

        # Merge the headers for the descriptors that allows different length sequenceing
        #descr = c;#["YPredStruct","QSOrder","SOCNumber","APAAC","PAAC","CKSAAGP","CKSAAP","NMBroto","Geary","Moran","BINARY","EAAC","AAINDEX","ZSCALE","BLOSUM62","EGAAC","AAC","DPC","DDE","TPC","GAAC","GDPC","GTPC","CTDC","CTDT","CTDD","CTriad","KSCTriad"]    
        for d in descr:
            print("Merging descriptors " + str(d))
            #open descriptor data, then append the descriptor columns
            with open("./descriptors/"+TRAINING_SET+"/"+str(d)+".txt") as reader:
                head = reader.readline()
                head = head.replace("\n","")
                hData = head.split("\t")                        
                hData= hData[1:]
                #append the descriptors
                for h in hData:
                    writer.write(str(h)+"\t")
                    DESCRIPTORS_ORDER.append(str(h))

                #now read the file content and fill the SEQ_DATA dictionary
                for seq_data in reader:                
                    seq_data = seq_data.replace("\n","")
                    sData = seq_data.split("\t")
                    SEQ = sData[0]
                    if (SEQ=="SEQUENCE"):
                        continue;
                    if (not SEQ in SEQ_DATA):
                        if (d=="YPredStruct"):
                            continue
                        print("Incoerence detected:" + str(SEQ) + " not found in dictionary")
                        SEQ_DATA[SEQ]={}
                        exit()
                    #for each descriptor in hData fill the dictionary of the current
                    #sequence
                    sData = sData[1:]                
                    for i in range(0,len(hData)):
                        SEQ_DATA[SEQ][hData[i]]=sData[i]                           
                #go to the next descriptors file
        writer.write("TARGET\n")
        #write the output
        for SEQ in SEQ_DATA:
            writer.write(str(SEQ)+"\t")
            for d in DESCRIPTORS_ORDER:
                writer.write(SEQ_DATA[SEQ][d])
                writer.write("\t")
            writer.write(SEQ_DATA[SEQ]["TARGET"])
            writer.write("\n")

    print("There are " + str(len(DESCRIPTORS_ORDER))+ " descriptors available!")
    shutil.make_archive("./classificator_inputs/"+INPUT_NAME+".zip", 'zip', "./classificator_inputs/"+INPUT_NAME)
    shutil.rmtree("./classificator_inputs/"+INPUT_NAME, ignore_errors=True)
    

