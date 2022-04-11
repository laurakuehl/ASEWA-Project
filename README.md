# ASEWA-Project
Artistic Style Exploration with ANNs - Project within the course 'Implementing ANNs with Tensorflow' at the University of Osnabrueck

## Abstract
In this project, we explore the artistic style transfer performed with CNNs like the VGG19 and the ResNet50 and compare different angles regarding for example performance and aesthetics. We look at the theoretical basics of a style transfer and how its feature extraction works. Later we try to compare the networks' results by using an art-style-classifying ResNet and our subjective opinion. Additionally, we will have a look at how the ratio of the weights, different learning rates layer selection and the input image influences the style transfer.

## Content
- VGG19 performing the Style Transfer
- ResNet50 performing the Style Transfer
- ResNet classifying the art style of an image
- Visualization scripts
- Paper "Artistic Style Exploration with Artificial Neural Networks" that explains our approach and results

## VGG19

### Own Model and Training
`ASEWA_Own_Model.ipynb` contains a self-implemented VGG19 model, its training and the Style Transfer performed on a content image of a Labrador and a Kandinsky style image.

### Own Model and Loaded Weights
`ASEWA_VGG19_Own_Model_Plus_Weights.ipynb`: Uses the own VGG19 implementation but loads weights from a pretrained model that was trained with Imagenet data.

### Pretrained VGG19
`ASEWA_VGG19_Pretrained_Model.ipynb`: Taking a pretrained VGG19 and performing the Style Transfer
