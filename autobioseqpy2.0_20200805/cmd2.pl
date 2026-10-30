use strict;
use warnings;

my @model=("1D2D","AtomPairs2DFingerprintCount","AtomPairs2DFingerprinter","EStateFingerprinter","ExtendedFingerprinter","Fingerprinter","GraphOnlyFingerprinter","KlekotaRothFingerprinter","KlekotaRothFingerprintCount","MACCSFingerprinter","PubchemFingerprinter","Rdkit","SubstructureFingerprinter","SubstructureFingerprintCount");

foreach my $name (@model) {
    for (my $i=1;$i<=5;$i++) {
    my @a=split("_",$name);
         print "python running.py --dataType other --dataEncodingType other --dataTrainFilePaths examples/drug/data/pos_train-$a[0].txt examples/drug/data/neg_train-$a[0].txt --dataTrainLabel 1 0 --dataSplitScale 0.8 --modelLoadFile examples/drug/model/$name.py --verbose 1 --outSaveFolderPath out/$name-$i --savePrediction 1 --showFig 0 --saveFig 1 --batch_size 32 --epochs 15 --shuffleDataTrain 1 --spcLen 100 --modelSaveName tmpMod.json --weightSaveName tmpWeight.bin --noGPU 0 --paraSaveName parameters.txt --optimizer optimizers.Adam(lr=0.001,amsgrad=False,decay=False)\n";
        print "\n";
     }   
    print "\n"; 
}