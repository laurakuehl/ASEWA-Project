# -*- coding: utf-8 -*-
"""ASEWA-VGG19-Own-Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12E42biilULav5MuoOGKVRUs_US16mTvU

# ASEWA Project - VGG19
Creating an own VGG19, training it and then perform Style Transfer
---
Janina Klarmann, Laura Kühl

## Setup
"""

import tensorflow as tf
import numpy as np
from torchvision import transforms
import tensorflow_datasets as tfds
from keras.preprocessing.image import ImageDataGenerator
import math

import PIL.Image
import IPython.display as display
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

import time
import functools

import tqdm
import datetime

"""## Own VGG19 Implementation and Training

### Loading Data

#### Cifar10
"""

# load the dataset, we use cifar10
(train_ds, test_ds, valid_ds), metadata = tfds.load('cifar10', split=['train[:70%]','train[70%:85%]', 'train[85%:]'], as_supervised

"""#### Imagenette"""

# imagenette/full-size-v2
(train_ds, test_ds, valid_ds), metadata = tfds.load('imagenette/full-size-v2', split=['train[:70%]','train[70%:85%]', 'train[85%:]'], as_supervised=True, with_info=True)

"""### Data Preprocessing"""

# data preprocessing
def preprocess(data):
  'preprocesses the dataset'
  #convert data from uint8 to float32
  data = data.map(lambda img, target: (tf.cast(img, tf.float32), target))
  #resize images
  # data = data.map(lambda img, target: (tf.image.resize(img, [224,224]), target))
  #normalization
  data = data.map(lambda img, target: ((img/128.)-1., target))
  # create one-hot targets
  data = data.map(lambda img, target: (img, tf.one_hot(target, depth=10)))
  #cache this progress in memory, as there is no need to redo it; it is deterministic after all
  data = data.cache().shuffle(1000).batch(64).prefetch(20)
  return data


train_data = train_ds.apply(preprocess)
valida_data = valid_ds.apply(preprocess) 
test_data = test_ds.apply(preprocess)

"""### VGG19 Model"""

# Creating a VGG19 Model
model_VGG19 = tf.keras.Sequential()
model_VGG19.add(tf.keras.layers.Conv2D(64, (3, 3), padding="same", activation='relu', name='convlayer11'))
model_VGG19.add(tf.keras.layers.Conv2D(64, (3, 3), padding="same", activation='relu', name='convlayer12'))
model_VGG19.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2))
model_VGG19.add(tf.keras.layers.Conv2D(128, (3, 3), padding="same", activation='relu', name='convlayer21'))
model_VGG19.add(tf.keras.layers.Conv2D(128, (3, 3), padding="same", activation='relu', name='convlayer22'))
model_VGG19.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
model_VGG19.add(tf.keras.layers.Conv2D(256, (3, 3), padding="same", activation='relu', name='convlayer31'))
model_VGG19.add(tf.keras.layers.Conv2D(256, (3, 3), padding="same", activation='relu', name='convlayer32'))
model_VGG19.add(tf.keras.layers.Conv2D(256, (3, 3), padding="same", activation='relu', name='convlayer33'))
model_VGG19.add(tf.keras.layers.Conv2D(256, (3, 3), padding="same", activation='relu', name='convlayer34'))
model_VGG19.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer41'))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer42'))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer43'))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer44'))
model_VGG19.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer51'))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer52'))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer53'))
model_VGG19.add(tf.keras.layers.Conv2D(512, (3, 3), padding="same", activation='relu', name='convlayer54'))
model_VGG19.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
model_VGG19.add(tf.keras.layers.GlobalAveragePooling2D())
model_VGG19.add(tf.keras.layers.Dense(4096, activation=tf.nn.relu))
model_VGG19.add(tf.keras.layers.Dense(4096, activation=tf.nn.relu))
model_VGG19.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
model_VGG19.build((None, None, None, 3))

"""### Training"""

def train_step(model, input, target, loss_function, optimizer):
  # loss_object and optimizer_object are instances of respective tensorflow classes
  with tf.GradientTape() as tape:
    prediction = model(input)
    loss = loss_function(target, prediction)
    
  gradients = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))
  return loss


def test(model, test_data, loss_function):
  # test over complete test data

  test_accuracy_aggregator = []
  test_loss_aggregator = []

  for (input, target) in test_data:
    prediction = model(input)
    sample_test_loss = loss_function(target, prediction)
    sample_test_accuracy = np.argmax(target, axis=1) == np.argmax(prediction, axis=1)
    sample_test_accuracy = np.mean(sample_test_accuracy)
    test_loss_aggregator.append(sample_test_loss.numpy())
    test_accuracy_aggregator.append(sample_test_accuracy)

  test_loss = tf.reduce_mean(test_loss_aggregator)
  test_accuracy = tf.reduce_mean(test_accuracy_aggregator)

  return test_loss, test_accuracy

# Baseline model for comparison
tf.keras.backend.clear_session()

# load tensorboard extension
# %load_ext tensorboard

train_dataset = train_data
test_dataset = test_data
validation_dataset = valida_data

### Hyperparameters
num_epochs = 30
learning_rate = 0.00001

# Initialize the loss: categorical cross entropy. Check out 'tf.keras.losses'.
cross_entropy_loss = tf.keras.losses.CategoricalCrossentropy()
# Initialize the optimizer: Adam with default parameters. Check out 'tf.keras.optimizers'
optimizer = tf.keras.optimizers.Adam(learning_rate)


#define the date time to log Tensorboard
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
test_log_dir = 'logs/gradient_tape/' + current_time + '/test'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)
test_summary_writer = tf.summary.create_file_writer(test_log_dir)


# # open the tensorboard to inspect the data for the 100 steps
# %tensorboard --logdir logs/

model = model_VGG19
# Initialize lists for later visualization.
train_losses = []

valid_losses = []
valid_accuracies = []

test_losses = []
test_accuracies = []

#testing on the validation dataset once before we begin
valid_loss, valid_accuracy = test(model, validation_dataset, cross_entropy_loss)
valid_losses.append(valid_loss)
valid_accuracies.append(valid_accuracy)

# check how model performs on train data once before we begin
train_loss, _ = test(model, train_dataset,cross_entropy_loss)
train_losses.append(train_loss)

# We train for num_epochs epochs.
for epoch in range(num_epochs):
    print(f'Epoch: {str(epoch)} starting with accuracy {valid_accuracies[-1]}')

    #training (and checking in with training)
    epoch_loss_agg = []
    for input,target in train_dataset:
        train_loss = train_step(model, input, target, cross_entropy_loss, optimizer)
        epoch_loss_agg.append(train_loss)
    
    mean_train_loss = np.mean(epoch_loss_agg)
    

    # logging the validation metrics to the log file which is used by tensorboard
    with train_summary_writer.as_default():

        tf.summary.scalar("Train Loss", mean_train_loss, step=epoch)

    #testing, so we can track accuracy and test loss
    valid_loss, valid_accuracy = test(model, validation_dataset, cross_entropy_loss)
    valid_losses.append(valid_loss)
    valid_accuracies.append(valid_accuracy)

"""## Style Transfer

### Accessing Intermediate VGG19 Layers
"""

def Our_VGG19_Model(layer_names):
  """ Creates our model with access to intermediate layers. 
  
  This function will load the VGG19 model and access the intermediate layers. 
  These layers will then be used to create a new model that will take input image
  and return the outputs from these intermediate layers from the VGG model. 
  
  Returns:
    returns a keras model that takes image inputs and outputs the style and 
      content intermediate layers. 
  """
  # Load our model. We load pretrained VGG, trained on imagenet data (weights=’imagenet’)
  vgg = model_VGG19
  vgg.trainable = False
  # Get output layers corresponding to style and content layers 
  outputs = [vgg.get_layer(name).output for name in layer_names]
  # Build model 
  model = tf.keras.Model([vgg.input], outputs)

  return model

"""### Content and Style Layers"""

content_layer_names = ['convlayer52']
style_layer_names = ['convlayer11', 'convlayer21','convlayer31','convlayer41','convlayer51']

"""### Input Images

#### Loading Images
"""

content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_

"""#### Image Preprocessing"""

# Define a function to load an image and limit its maximum dimension to 512 pixels.
def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

content_image = load_img(content_path)
style_image = load_img(style_path)

"""### Style Transfer Models

#### Style Extraction Model
"""

class StyleExtractionModel (tf.keras.models.Model):
  def __init__(self, style_layers, content_layers):
    super(StyleExtractionModel, self).__init__()
    self.vgg19 = Our_VGG19_Model(style_layers+content_layers)
    self.style_layers = style_layers
    self.content_layers = content_layers
    self.num_style_layers = len(style_layers)
    self.vgg19.trainable = False 

  def gram_matrix(self, input_tensor):
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1]*input_shape[2], tf.float32)
    return result/(num_locations)

  def call(self, inputs):
    "Expects float input in [0,1]"#
    inputs = inputs*255.0
    preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
    outputs = self.vgg19(preprocessed_input)
    style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                      outputs[self.num_style_layers:])

    style_outputs = [self.gram_matrix(style_output)
                    for style_output in style_outputs]

    content_dict = {content_name: value
                    for content_name, value
                    in zip(self.content_layers, content_outputs)}

    style_dict = {style_name: value
                  for style_name, value
                  in zip(self.style_layers, style_outputs)}

    return {'content': content_dict, 'style': style_dict}

"""#### Style Training Model"""

class StyleTrainingModel(tf.keras.models.Model):
  def __init__(self, style_layers, content_layers):
    super(StyleTrainingModel, self).__init__()
    self.ExtractionModel = StyleExtractionModel(style_layers, content_layers)
    self.opt = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)
    self.style_weight = 1e-2
    self.content_weight = 1e4
    self.style_targets = self.ExtractionModel(style_image)['style']
    self.content_targets = self.ExtractionModel(content_image)['content']
    self.num_style_layers = len(style_layers)
    self.num_content_layers = len(content_layers)

  def clip_0_1(self, image):
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

  def tensor_to_image(self, tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
      assert tensor.shape[0] == 1
      tensor = tensor[0]
    return PIL.Image.fromarray(tensor)
 
  def style_content_loss(self, outputs):
    style_outputs = outputs['style']
    content_outputs = outputs['content']
    style_loss = tf.add_n([tf.reduce_mean((style_outputs[name]-self.style_targets[name])**2) 
                          for name in style_outputs.keys()])
    style_loss *= self.style_weight / self.num_style_layers

    content_loss = tf.add_n([tf.reduce_mean((content_outputs[name]-self.content_targets[name])**2) 
                            for name in content_outputs.keys()])
    content_loss *= self.content_weight / self.num_content_layers
    loss = style_loss + content_loss
    return loss

  @tf.function()
  def train_step(self, img):
    with tf.GradientTape() as tape:
      outputs = self.ExtractionModel(img)
      loss = self.style_content_loss(outputs)

    grad = tape.gradient(loss, img)
    self.opt.apply_gradients([(grad, img)])
    image.assign(self.clip_0_1(img))

"""#### Transfer Style"""

def imshow(image, title=None):
  if len(image.shape) > 3:
    image = tf.squeeze(image, axis=0)

  plt.imshow(image)
  if title:
    plt.title(title)

content_image = load_img(content_path)
style_image = load_img(style_path)

plt.subplot(1, 2, 1)
imshow(content_image, 'Content Image')

plt.subplot(1, 2, 2)
imshow(style_image, 'Style Image')

MyModel = StyleTrainingModel(style_layer_names, content_layer_names)
image = tf.Variable(content_image)

for i in range(100):
  print(f'Working on Trainingstep {i}...')
  MyModel.train_step(image)
print('\n Final Image:')  
MyModel.tensor_to_image(image)