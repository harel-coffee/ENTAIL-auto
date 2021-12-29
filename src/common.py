# This script check the repository integrity
# to made reproducible this work on different machine
# 


WALTZDB_PATH = "./datasets/waltzdb.csv";
AMYLOAD_PATH = "./datasets/amyload.csv"
PEP424_PATH = "./datasets/pep424.csv"
STRUCTURES_PATH ="./datasets/pdb"
SWAP_PATH ="./swap"
TRAINING_DESCRIPTORS_PATH = "./datasets/descriptors/TrainingSet";
TEST_DESCRIPTORS_PATH = "./datasets/descriptors/TestSet";
TARGET_SEQUENCE_LEN = 6

#DESCRIPTORS_TOUSE = ["QSOrder","SOCNumber","APAAC","PAAC","CKSAAGP","CKSAAP","NMBroto","Geary","Moran","BINARY","EAAC","AAINDEX","ZSCALE","BLOSUM62","EGAAC","AAC","DPC","DDE","TPC","GAAC","GDPC","GTPC","CTDC","CTDT","CTDD","CTriad","KSCTriad"]
DESCRIPTORS_TOUSE = ["QSOrder","SOCNumber","APAAC","PAAC","NMBroto","Geary","Moran","AAINDEX","ZSCALE","EGAAC","DDE","GAAC","GDPC","CTDC","CTDD"]

###################
# PLEASE NOTE:    #
###################
#
# ENTAIL classificators are trained using MATLAB R2021b. 
#
# The variable TRAININGSET_SIZE is refereed to the MATLAB training set, then
# you MUST consider it as TRAINING UNION VALIDATION sets.
# It is mandatory to use cross validation to protect the classificator against overfitting.
# The script will generate a balanced dataset composed by (TRAININGSET_SIZE / 2) sequences.
# Then, TRAININGSET_SIZE msut be EVEN!

TRAININGSET_SIZE = 700
TESTSET_SIZE = 66

print("ENTAIL: yEt aNoTher Amyloid fIbrilis cLassificator")
