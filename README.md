# ASEWA-Project
Artistic Style Exploration with ANNs - Project within the course 'Implementing ANNs with Tensorflow' at the University of Osnabrueck

## Abstract
In this project, we explore the artistic style transfer performed with CNNs like the VGG19 and the ResNet50 and compare different angles regarding for example performance and aesthetics. We look at the theoretical basics of a style transfer and how its feature extraction works. Later we try to compare the networks' results by using an art-style-classifying ResNet and our subjective opinion. Additionally, we will have a look at how the ratio of the weights, different learning rates layer selection and the input image influences the style transfer.

## Remark
To ensure a better understanding of the project and the different experiments and explorations that were conducted, we suggest to have a look at the code in the order of this ReadMe document. 

## Contents
- VGG19 performing the Style Transfer
- ResNet50 performing the Style Transfer
- ResNet classifying the art style of an image
- Visualization scripts
- Datasets
- Paper "Artistic Style Exploration with Artificial Neural Networks" that explains our approach and results

## VGG19
### Own Model and Training
`ASEWA_Own_Model.ipynb` contains a self-implemented VGG19 model, its training and the Style Transfer performed on a content image of a Labrador and a Kandinsky style image.

### Own Model and Loaded Weights
`ASEWA_VGG19_Own_Model_Plus_Weights.ipynb`: Uses the own VGG19 implementation but loads weights from a pretrained model that was trained with Imagenet data.

### Pretrained VGG19
`ASEWA_VGG19_Pretrained_Model.ipynb`: Taking a pretrained VGG19 and performing the Style Transfer.

## ResNet50
`ASEWA-ResNet50.ipynb`: The Style Transfer using a pretrained ResNet50 and adjusted Style Extraction and Training models.

## Art Discrimination Model
### Art Transfer Discrimination Model
https://www.kaggle.com/datasets/lkuehl/art-transfer-discrimination-model-resv2: Classifies the art style of an input image.
(The trained Art-Transfer-Discrimination model could not be uploaded due to its size)

### Art Epoch Discrimination ResNet
`ASEWA_Art_Epoch_Discrimination_ResNet.ipynb`: Calculates the accuracies of the art style classification by the Art-Transfer-Discrimination model.

## Visualization
`ASEWA_Visualisation_Artistic_Style_Transfer_Exploration.ipynb`: Visualizing different architectures, exploring weights and performing mass Style Transfer.

## Datasets
### Style Dataset
https://www.kaggle.com/datasets/torres07/art-movements: 'Art Movement' dataset used as style images.

### Results Art Style Transfer
- ResNet Style Transferred images: https://www.kaggle.com/datasets/lkuehl/resnet-style-transferred-images
- VGG Style Transferred Images with Noise Image as Input: https://www.kaggle.com/datasets/lkuehl/vgg19-augmented-from-noise
- VGG Style Transferred Images with Content Image as Input: https://www.kaggle.com/datasets/lkuehl/vgg19-augmented-from-content-image

## Paper
`Artistic_Style_Exploration_With_ANNs.pdf`: The paper that explains our project, the experiments and studies that were conducted and different approaches to different problems.
