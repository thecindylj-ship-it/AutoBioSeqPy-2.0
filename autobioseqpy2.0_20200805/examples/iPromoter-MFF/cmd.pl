use strict;
use warnings;

my @model=("bilstm","cnnrnn","dpcnn","FastText","FNet","multi_text_cnn","rcnn","rnncnn","text_cnn","transformer");

foreach my $name (@model) {
    for (my $i=1;$i<=5;$i++) {
         print "python running.py --dataType dna --dataEncodingType dict --dataTrainFilePaths examples/iPromoter-MFF/data/pos_train.txt examples/iPromoter-MFF/data/neg_train.txt --dataTrainLabel 1 0 --dataSplitScale 0.8 --modelLoadFile examples/iPromoter-MFF/model/$name.py --verbose 1 --outSaveFolderPath out/$name-$i --savePrediction 1 --showFig 0 --saveFig 1 --batch_size 64 --epochs 25 --shuffleDataTrain 1 --spcLen 81 --noGPU 0 --paraSaveName parameters.txt --optimizer optimizers.Adam(lr=0.001,amsgrad=False,decay=False) --useKMer 1 --KMerNum 3\n";
        print "\n";
     }   
    print "\n"; 
}