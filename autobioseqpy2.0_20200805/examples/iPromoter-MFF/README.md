# iPromoter-MFF

Multimodal Feature Fusion for Prokaryotic Promoter Identification

## 1. Overview

iPromoter-MFF is a deep learning framework for identifying prokaryotic promoters through multimodal feature fusion. It combines an FNet sequence encoder with dense neural networks that process complementary nucleotide composition, DNA shape, and physicochemical features. The study compares nine sequence-based models across 27 prokaryotic datasets. FNet achieved the best overall performance and was selected as the sequence branch for multimodal fusion. For each dataset, the fusion experiments explore all 2,047 non-empty subsets of 11 additional feature types. The optimal feature combination is species-specific.

- Source code: [GitHub repository](https://github.com/thecindylj-ship-it/AutoBioSeqPy-2.0)
- Processed datasets: [Zenodo record](https://zenodo.org/records/23901516)

This directory supplies model definitions, training commands, a multimodal command generator, and example inputs. Saved model checkpoints are not included in the current project directory.

## 2. Requirements and setup

Use a compatible Python environment with the dependencies required by autoBioSeqpy and the selected models, including TensorFlow/Keras, NumPy, scikit-learn, plotting libraries, and `keras_nlp` for FNet. Refer to the framework's root README and `manual.docx` for installation and usage details.

The code uses legacy library APIs. Preserve the package versions from a working environment; installing the latest versions of every package may require code changes.

Download or clone the repository and locate `autobioseqpy2.0_20200805`. Run every command in this README from that directory, which contains `running.py` and `predicting.py`.

For Windows Anaconda Prompt, activate your configured environment and change to your installation directory before running the commands. The environment name and absolute installation path depend on your computer.

## 3. Directory structure

```text
autobioseqpy2.0_20200805/
+-- running.py
+-- predicting.py
+-- README.md
+-- manual.docx
\-- examples/
    \-- iPromoter-MFF/
        +-- readme.md
        +-- 1.txt
        +-- generateCMD.py
        +-- cmd.pl
        +-- data/
        \-- model/
```

The directory name is `examples` (plural). The commands below use paths relative to the framework root.

## 4. Data preparation

### Example inputs

The bundled example inputs are stored directly in `examples/iPromoter-MFF/data/`.

| Task | Training files | Separate test files |
|---|---|---|
| Single-model experiments | `pos_train.txt`, `neg_train.txt` | `pos_test.txt`, `neg_test.txt` |
| Multimodal sequence branch | `potr.txt`, `netr.txt` | `pote.txt`, `nete.txt` |
| Multimodal feature branches | `potr-<feature>.txt`, `netr-<feature>.txt` | `pote-<feature>.txt`, `nete-<feature>.txt` |

Positive and negative inputs use labels 1 and 0, respectively. Sequence files use FASTA-style records despite their `.txt` extension. Numerical feature files must correspond to the same samples as the sequence inputs. Keep sample identifiers consistent across all modalities.

The 11 additional feature types are:

`HexaNC`, `TetraNC`, `PentaNC`, `MGW`, `ProT`, `Roll`, `HelT`, `EP`, `Nucleosome`, `DnaseI`, and `RFHC`.

### Complete datasets

Download `data.zip` from the Zenodo record linked above and extract it. The archive contains species-specific directories under `data/`. Within each species directory:

- `single_model_data/` contains the sequence inputs for single-model experiments.
- `train_test_data/` contains the multimodal sequence and feature inputs.

Update the paths in the training commands or `generateCMD.py` to the selected species directory. The species-organized archive and the flat example directory have different layouts. Enclose paths containing spaces in double quotes, including paths inserted into generated commands.

## 5. Experimental workflow

1. Prepare the sequence inputs and matching feature files for the selected species.
2. Run the single-model commands to compare sequence-based architectures.
3. Run the FNet-based multimodal experiments.
4. Select the feature combination and training settings using validation results.
5. Evaluate the selected model on the independent test set, keeping that set excluded from training and model selection.
6. Retain the run parameters, predictions, evaluation results, and trained model files.

The supplied `1.txt` commands and `generateCMD.py` use `--dataSplitScale 0.8` on their training inputs. They do not automatically read the separate test files. In the current `running.py`, 10% of the resulting training portion is used for validation, giving approximately 72% training, 8% validation, and 20% internal testing of the supplied inputs.

This internal split is separate from an independently reserved test set. Repeating a command five times should not be described as five-fold cross-validation.

## 6. Single-model training

The [`1.txt`](1.txt) file contains 45 commands: five runs for each of nine models.

| Model | Definition |
|---|---|
| BiLSTM | `model/bilstm.py` |
| CNN_RNN | `model/cnnrnn.py` |
| FastText | `model/FastText.py` |
| FNet | `model/FNet.py` |
| Multi_Text_CNN | `model/multi_text_cnn.py` |
| RCNN | `model/rcnn.py` |
| RNN_CNN | `model/rnncnn.py` |
| Text_CNN | `model/text_cnn.py` |
| Transformer | `model/transformer.py` |

Open `1.txt`, copy the desired complete command, and execute it from the framework root. This is a command list, not a Python script; do not run `python 1.txt`.

### FNet example

Copy the following as a single command:

```bash
python running.py --dataType dna --dataEncodingType dict --dataTrainFilePaths examples/iPromoter-MFF/data/pos_train.txt examples/iPromoter-MFF/data/neg_train.txt --dataTrainLabel 1 0 --dataSplitScale 0.8 --modelLoadFile examples/iPromoter-MFF/model/FNet.py --verbose 1 --outSaveFolderPath out/FNet-1 --savePrediction 1 --showFig 0 --saveFig 1 --batch_size 64 --epochs 25 --shuffleDataTrain 1 --spcLen 81 --noGPU 0 --paraSaveName parameters.txt --optimizer "optimizers.Adam(lr=0.001,amsgrad=False,decay=False)" --useKMer 1 --KMerNum 3
```

Results are written to `out/FNet-1/`. The other commands use separate model and run names. Choose distinct output directories when switching species or preserving previous experiments.

## 7. Multimodal model training

Run:

```bash
python examples/iPromoter-MFF/generateCMD.py
```

The current script fixes `FNet.py` as the sequence branch and combines it with every non-empty subset of the 11 additional feature types. It schedules 2,047 combinations for each of five repetitions, giving 10,235 training tasks for the configured dataset.

Results are organized as follows:

```text
outs0/
    HexaNC/
    TetraNC/
    ...
    HexaNC__TetraNC/
    ...
outs1/
outs2/
outs3/
outs4/
```

A subdirectory name records the additional features; FNet is included in every combination. These output directories are created under the framework root.

Before running the full search, verify the dataset paths and preserve any existing output directories. For a short initial check, run a single generated command. The full search can take substantial time.

The generator prints failed commands at the end. It does not automatically select the best combination or produce `Table_S1.csv`; summarize results separately and select configurations using validation performance.

## 8. Independent test evaluation

### Training with explicitly supplied test files

To evaluate against separate test files using `running.py`, supply `--dataTestFilePaths` and `--dataTestLabel` instead of `--dataSplitScale`.

The following complete FNet example trains a new model, evaluates it on the separate sequence test files, and saves its architecture and weights:

```bash
python running.py --dataType dna --dataEncodingType dict --dataTrainFilePaths examples/iPromoter-MFF/data/pos_train.txt examples/iPromoter-MFF/data/neg_train.txt --dataTrainLabel 1 0 --dataTestFilePaths examples/iPromoter-MFF/data/pos_test.txt examples/iPromoter-MFF/data/neg_test.txt --dataTestLabel 1 0 --modelLoadFile examples/iPromoter-MFF/model/FNet.py --verbose 1 --outSaveFolderPath out/FNet-independent-example --savePrediction 1 --showFig 0 --saveFig 1 --batch_size 64 --epochs 25 --shuffleDataTrain 1 --spcLen 81 --noGPU 0 --paraSaveName parameters.txt --optimizer "optimizers.Adam(lr=0.001,amsgrad=False,decay=False)" --useKMer 1 --KMerNum 3 --modelSaveName trained_model.json --weightSaveName trained_weights.bin
```

This is a single-model usage example, not the species-specific optimal multimodal model or a claim to reproduce the manuscript's reported scores.

For a selected multimodal model, supply the corresponding test sequence files and feature pairs in the same branch order as the training inputs. Set `--dataTestModelInd` to map each positive/negative pair to its branch, matching `--dataTrainModelInd`. Keep the selected architecture, preprocessing, and feature dimensions consistent.

### Prediction using saved weights

Use `predicting.py` when loading a saved model for prediction without further training. A compatible complete architecture and its trained weights are required; model-definition `.py` files alone do not contain trained weights.

In this framework, `outSaveFolderPath` identifies the checkpoint directory for prediction, while `modelSaveName` and `weightSaveName` specify the existing architecture and weight filenames. Configure test inputs and preprocessing for that checkpoint.

The current project directory does not contain a ready-to-use checkpoint, so a universal pretrained prediction command is not supplied. Each species may require a different feature combination and checkpoint.

The prediction output must be matched to the true test labels for evaluation. The current `predicting.py` does not automatically calculate AUROC or AUPRC; its internal placeholder labels must not be used as ground truth.

## 9. Outputs and model saving

Training outputs are stored in the directory specified by `--outSaveFolderPath`. Depending on the enabled options, they include run parameters, prediction results, performance summaries, and plots.

The supplied training commands request parameters, predictions, and figures. They do not specify model saving by default. To retain the architecture and weights, append both options to the training command:

```text
--modelSaveName trained_model.json --weightSaveName trained_weights.bin
```

For the full multimodal search, add these options to the command template in `generateCMD.py` only if saving every trained model is intended, as this can require considerable storage.

Keep the architecture, all associated weight-checkpoint files, and the matching `parameters.txt` together. When TensorFlow saves an index/data checkpoint pair, use the shared prefix `trained_weights.bin` when loading it.

Preserve the software environment and run configuration alongside released results. A performance summary or model-definition file does not replace a trained checkpoint.

