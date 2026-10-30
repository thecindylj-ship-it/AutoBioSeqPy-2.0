# iPromoter-MFF

## Multimodal Feature Fusion for Prokaryotic Promoter Identification

** Corresponding author:** ljs@swmu.edu.cn

## Overview

iPromoter-MFF is a multimodal deep learning framework for identifying prokaryotic promoters across multiple species. It integrates DNA sequence information with complementary features describing nucleotide composition, DNA shape, and physicochemical properties.The framework combines an FNet sequence encoder with dense neural networks for additional feature modalities. During model development, 2,047 nonempty combinations of 11 complementary feature types are evaluated to identify species-specific fusion configurations. The selected configuration is subsequently used for independent test-set evaluation.This distribution includes the training framework, model definitions, processed datasets for 27 species, and one saved multimodal model configuration.

## Preparation

1)Download and extract the repository.

2)Place the entire iPromoter-MFF folder inside the examples directory of autobioseqpy2.0_20200805. Create the examples directory if necessary.

3)Install the dependencies required by the selected models, including TensorFlow/Keras, NumPy, scikit-learn, and plotting libraries. Some models require additional packages, such as keras_nlp for FNet. Refer to the bundled autoBioSeqpy documentation for further details.

The working directory structure should be:

autobioseqpy2.0_20200805/
  running.py
  predicting.py
  README.md
  manual.docx
  examples/
    iPromoter-MFF/
      1.txt
      generateCMD.py
      generateCMD-test.py
      data/
      model/
      train_models/   

Run all commands below from the autobioseqpy2.0_20200805 directory containing running.py.Model and dataset paths should begin with examples/iPromoter-MFF/. Legacy paths beginning with examples/PDD/ must be updated before execution. Paths containing spaces must be enclosed in double quotes.The supplied code uses legacy library APIs. A pinned software environment is not included, and compatibility with newer package versions should be checked before running the experiments.

## Processed datasets

Processed datasets for 27 species are provided in examples/iPromoter-MFF/data/, with a separate directory for each species.

Each species directory includes:

¡ñ single_model_data/: Training and test sequences for sequence-based models.
¡ñ train_test/: Sequences and corresponding features for multimodal models.

### Sequence-based inputs

 The single_model_data/ directory contains:

¡ñ pos_train.txt: Positive training sequences.
¡ñ neg_train.txt: Negative training sequences.
¡ñ pos_test.txt: Positive test sequences.
¡ñ neg_test.txt: Negative test sequences.

### Multimodal inputs

The train_test/ directory contains sequence files and corresponding feature files.

The filename prefixes indicate the sample partition and label:

¡ñ potr: Positive training samples.
¡ñ netr: Negative training samples.
¡ñ pote: Positive test samples.
¡ñ nete: Negative test samples.

For example, potr.txt contains positive training sequences, while potr-TetraNC.txt contains their corresponding TetraNC features.

The 11 complementary feature types are:

HexaNC, TetraNC, PentaNC, MGW, ProT, Roll, HelT, EP, Nucleosome, DnaseI, RFHC

Sequence files use FASTA-style formatting despite their .txt extension. Feature files contain numerical inputs. Sequence and feature records must refer to the same samples in the same order.

## Experimental workflow

The project provides separate entry points for model development and independent test-set evaluation:

1) Run the sequence-based model commands in 1.txt.

2) Run generateCMD.py to evaluate multimodal feature combinations.

3) Select the configuration using development-stage validation results.

4) Evaluate the selected configuration on the independent test set.

The independent test set should not be used to select feature combinations or tune hyperparameters.

## Sequence-based model experiments

Commands for sequence-based experiments are provided in:

examples/iPromoter-MFF/1.txt

This file is a collection of command-line examples. Copy and execute the required commands from the autoBioSeqpy root directory.Before execution, update the data paths to the selected species¡¯ single_model_data/ directory and the model paths to examples/iPromoter-MFF/model/.

Available model implementations include:

¡ñ BiLSTM: bilstm.py

¡ñ CNN-RNN: cnnrnn.py

¡ñ RCNN: rcnn.py

¡ñ TextCNN: text_cnn.py

¡ñ FNet: FNet.py

¡ñ RNN-CNN: rnncnn.py

¡ñ Multi-Text-CNN: multi_text_cnn.py

¡ñ Transformer: transformer.py

## Example command

The following command uses the sequence training files for Acinetobacter baumannii ATCC 17978. It retains the internal-split setting used in 1.txt and adds model-saving options.

python running.py --dataType dna --dataEncodingType dict --dataTrainFilePaths "examples/iPromoter-MFF/data/1.Acinetobacter baumannii ATCC 17978 promoters/single_model_data/pos_train.txt" "examples/iPromoter-MFF/data/1.Acinetobacter baumannii ATCC 17978 promoters/single_model_data/neg_train.txt" --dataTrainLabel 1 0 --dataSplitScale 0.8 --modelLoadFile examples/iPromoter-MFF/model/FNet.py --verbose 1 --outSaveFolderPath out/Abaumannii_FNet-1 --savePrediction 1 --showFig 0 --saveFig 1 --batch_size 64 --epochs 25 --shuffleDataTrain 1 --spcLen 81 --noGPU 0 --paraSaveName parameters.txt --optimizer "optimizers.Adam(lr=0.001,amsgrad=False,decay=False)" --useKMer 1 --KMerNum 3 --modelSaveName trained_model.json --weightSaveName trained_weights.bin

The command internally splits the supplied training files. It does not load pos_test.txt or neg_test.txt.For repeated runs, use separate output directories to avoid overwriting results.

## Multimodal feature-combination experiments

Multimodal experiments are generated by:

examples/iPromoter-MFF/generateCMD.py

The script uses sequence and feature inputs from the selected species¡¯ train_test/ directory. It evaluates 2,047 nonempty combinations of 11 feature modalities, each combined with a sequence-based model, over five runs.

Before running the script:

¡ñ Update the sequence and feature paths to the selected species¡¯ train_test/ directory.

¡ñ Update model paths to examples/iPromoter-MFF/model/.

¡ñ Set the intended sequence model in the command template. The supplied template currently uses rnncnn.py; use FNet.py when running the FNet-based fusion experiments described in the manuscript.

¡ñ Ensure that generated paths containing spaces and the optimizer expression are correctly quoted.

¡ñ Add model-saving options if checkpoints are required for each configuration.

Run:

python examples/iPromoter-MFF/generateCMD.py

The complete script launches 10,235 training runs. Results are saved under outs0 through outs4, with a subdirectory for each feature combination.

The supplied script uses --dataSplitScale 0.8 and does not explicitly load the separately provided test files. It does not automatically generate Table_S1.csv.





