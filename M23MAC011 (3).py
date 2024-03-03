# -*- coding: utf-8 -*-
"""M23MAC011.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BwRLNYdIfU2_r2nwyjLB2238pGuJX0wy
"""

!pip install idx2numpy

from google.colab import drive
drive.mount('/content/drive')

#importing required libraries
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import idx2numpy
from sklearn.metrics import confusion_matrix
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import torch.nn.functional as F

# Defining the CNN architecture
class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()

        # Convolutional Layer 1
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=7, stride=1, padding=3)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)



        # Convolutional Layer 2
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=8, kernel_size=5, stride=1, padding=2)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)



        # Convolutional Layer 3
        self.conv3 = nn.Conv2d(in_channels=8, out_channels=4, kernel_size=3, stride=2, padding=1)
        self.relu3 = nn.ReLU()
        self.avgpool3 = nn.AvgPool2d(kernel_size=2, stride=2)


        # Output Layer
        self.output_layer = nn.Linear(4 * 2 * 2, num_classes)
        self.softmax = nn.Softmax(dim=1)



    def forward(self, x):


        x = self.maxpool1(self.relu1(self.conv1(x)))
        x = self.maxpool2(self.relu2(self.conv2(x)))
        x = self.avgpool3(self.relu3(self.conv3(x)))


        # Flatten for the fully connected layer
        x = x.view(x.size(0), -1)
        x = self.output_layer(x)


        return x

# Defining the IMPROVED CNN architecture
class improved_CNN(nn.Module):
    def __init__(self, num_classes):
        super(improved_CNN, self).__init__()

        # Convolutional Layer 1
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=7, stride=1, padding=3)
        self.batch_norm1 = nn.BatchNorm2d(16)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)



        # Convolutional Layer 2
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=8, kernel_size=5, stride=1, padding=2)
        self.batch_norm2 = nn.BatchNorm2d(8)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)



        # Convolutional Layer 3
        self.conv3 = nn.Conv2d(in_channels=8, out_channels=4, kernel_size=3, stride=2, padding=1)
        self.batch_norm3 = nn.BatchNorm2d(4)
        self.relu3 = nn.ReLU()
        self.avgpool3 = nn.AvgPool2d(kernel_size=2, stride=2)



        # Output Layer
        self.output_layer = nn.Linear(4 * 2 * 2, num_classes)
        self.softmax = nn.Softmax(dim=1)



    def forward(self, x):
        x = self.maxpool1(self.relu1(self.batch_norm1(self.conv1(x))))
        x = self.maxpool2(self.relu2(self.batch_norm2(self.conv2(x))))
        x = self.avgpool3(self.relu3(self.batch_norm3(self.conv3(x))))




        # Flatten for the fully connected layer
        x = x.view(x.size(0), -1)
        x = self.output_layer(x)


        return x

def plot(epoch, losses, accuracies, val_losses):
    # Plot loss per epoch and accuracy
    plt.figure(figsize=(12, 5))

    # Plot Loss
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(epoch)+1), losses, label='Training Loss')
    plt.plot(range(1, len(epoch)+1), val_losses, label='Validation Loss', color='red')
    plt.title('Training and Validation Loss per Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    # Plot Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(epoch) + 1), accuracies, label='Validation Accuracy', color='orange')
    plt.title('Validation Accuracy per Epoch')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim(top = 100)
    plt.legend()

    plt.tight_layout()
    plt.show()

def accuracy_score(true_labels, predicted_labels):
    correct_predictions = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == pred)
    total_samples = len(true_labels)

    accuracy = correct_predictions / total_samples
    return accuracy

# Defining the training phase
def train_network(train_loader, val_loader, learning_rate, num_epochs, model):
  # Loss function and optimizer
  cross_entropy = nn.CrossEntropyLoss()
  optimizer = optim.Adam(model.parameters(), lr=learning_rate)
  num_epoch = []
  num_accuracy = []
  num_loss = []
  num_val_loss = []
  # Training loop with validation set evaluation
  for epoch in range(num_epochs):
      model.train()
      total_loss = 0.0
      total_batches = 0

      for images, labels in train_loader:
          # Forward pass
          outputs = model(images)
          loss = cross_entropy(outputs, labels)

          # Backward pass and optimization
          optimizer.zero_grad()
          loss.backward()
          optimizer.step()

          total_loss += loss.item()
          total_batches += 1

      # Calculate average loss for the epoch
      average_loss = total_loss / total_batches

      # Calculate validation loss
      val_total_loss = 0.0
      val_total_batches = 0
      for val_images, val_labels in val_loader:
          val_outputs = model(val_images)
          val_loss = cross_entropy(val_outputs, val_labels)
          val_total_loss += val_loss.item()
          val_total_batches += 1
      val_average_loss = val_total_loss / val_total_batches


      # Evaluate the validation set
      true_labels, all_predicted_labels = model_test(val_loader, model)

      # Calculate validation accuracy
      accuracy = accuracy_score(true_labels, all_predicted_labels)
      print(f'Epoch [{epoch+1}/{num_epochs}], Training Loss: {average_loss:.4f}, Validation Loss: {val_average_loss:.4f}, Validation Accuracy: {accuracy*100:.2f}%')

      # Filling loss, epoch and accuracy in an array
      num_epoch.append(epoch+1)
      num_loss.append(average_loss)
      num_val_loss.append(val_average_loss)
      num_accuracy.append(accuracy*100)
  print("Model has been trained")
  plot(num_epoch, num_loss, num_accuracy, num_val_loss)

  return model

#Defining the testing phase
  def model_test(test_loader, model):
    model.eval()
    with torch.no_grad():
        all_predicted_labels = []
        true_labels = []

        for images, labels in test_loader:
            outputs = model(images)
            probabilities = F.softmax(outputs, dim=1)
            _, predicted = probabilities.max(1)

            all_predicted_labels.extend(predicted.numpy())
            true_labels.extend(labels.numpy())
    return all_predicted_labels , true_labels

def train_test_split(all_indices, test_size, random_state):

    if random_state is not None:
        random.seed(random_state)


    # Shuffle the indices randomly
    random.shuffle(all_indices)

    # Determine the split index
    split_index = int(len(all_indices) * (1 - test_size))

    # Split the indices
    train_indices = all_indices[:split_index]
    test_indices = all_indices[split_index:]

    return train_indices, test_indices

#Experiment number 1
# Load MNIST dataset from IDX files
images = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/train-images.idx3-ubyte')
labels = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/train-labels.idx1-ubyte')
test_images = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/t10k-images.idx3-ubyte')
test_labels = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/t10k-labels.idx1-ubyte')

# Scale down the pixel values to the range [0, 1]
images = images / 255.0
test_images = test_images / 255.0


# Convert to PyTorch tensors
train_images = torch.from_numpy(images).unsqueeze(1).float()  # Add channel dimension
train_labels = torch.from_numpy(labels).long()

test_images = torch.from_numpy(test_images).unsqueeze(1).float()  # Add channel dimension
test_labels = torch.from_numpy(test_labels).long()



# Split the dataset into train and validation sets
train_indices, val_indices = train_test_split(list(range(len(train_images))), test_size=0.1, random_state=42)

# Create datasets
train_dataset = TensorDataset(train_images[train_indices], train_labels[train_indices])
val_dataset = TensorDataset(train_images[val_indices], train_labels[val_indices])
test_dataset = TensorDataset(test_images, test_labels)

# Define training parameters
batch_size = 20
learning_rate = 0.001
num_epochs = 10


# Create data loaders
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)



# Instantiate the basic model
num_classes = 10  # MNIST has 10 classes (0 to 9)
model = CNN(num_classes=num_classes)
model = train_network(train_loader, val_loader, learning_rate, num_epochs, model)

# Instantiate the improved model
improved_model = improved_CNN(num_classes=num_classes)
improved_model = train_network(train_loader, val_loader, learning_rate, num_epochs, improved_model)



# Save the trained model
torch.save(model.state_dict(), 'cnn_model.pth')
torch.save(improved_model.state_dict(), 'improved_cnn_model.pth')

#  Testing Experimnent number 1
# Load the trained model state dictionary
model.load_state_dict(torch.load('cnn_model.pth'))

true_labels, all_predicted_labels = model_test(test_loader, model)

# Calculate accuracy
accuracy = accuracy_score(true_labels, all_predicted_labels)
print(f'Test Accuracy: {accuracy*100:.2f}%')

# Calculate confusion matrix
conf_matrix = confusion_matrix(true_labels, all_predicted_labels)


# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(true_labels), yticklabels=np.unique(true_labels))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

#  Testing Experimnent number 1 on improved cnn model
# Load the trained model state dictionary
improved_model.load_state_dict(torch.load('improved_cnn_model.pth'))
true_labels, all_predicted_labels = model_test(test_loader, improved_model)

# Calculate accuracy
accuracy = accuracy_score(true_labels, all_predicted_labels)
print(f'Test Accuracy: {accuracy*100:.2f}%')

# Calculate confusion matrix
conf_matrix = confusion_matrix(true_labels, all_predicted_labels)


# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(true_labels), yticklabels=np.unique(true_labels))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

#Experiment number 2
# Load MNIST dataset from IDX files
images = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/train-images.idx3-ubyte')
labels = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/train-labels.idx1-ubyte')
test_images = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/t10k-images.idx3-ubyte')
test_labels = idx2numpy.convert_from_file('/content/drive/MyDrive/DL Assignment 1/t10k-labels.idx1-ubyte')

# Scale down the pixel values to the range [0, 1]
images = images / 255.0
test_images = test_images / 255.0


# Convert to PyTorch tensors
train_images = torch.from_numpy(images).unsqueeze(1).float()  # Add channel dimension
train_labels = torch.from_numpy(labels).long()

test_images = torch.from_numpy(test_images).unsqueeze(1).float()  # Add channel dimension
test_labels = torch.from_numpy(test_labels).long()


# Combine classes to create 4 classes
class_mapping = {
    0: 0, 6: 0,  # Class 1
    1: 1, 7: 1,  # Class 2
    2: 2, 3: 2, 8: 2, 5: 2,  # Class 3
    4: 3, 9: 3  # Class 4
}

train_labels_combined = torch.tensor([class_mapping[label.item()] for label in train_labels])
test_labels_combined = torch.tensor([class_mapping[label.item()] for label in test_labels])




# Split the dataset into train and validation sets
train_indices, val_indices = train_test_split(list(range(len(train_images))), test_size=0.1, random_state=42)

# Create datasets
train_dataset = TensorDataset(train_images[train_indices], train_labels_combined[train_indices])
val_dataset = TensorDataset(train_images[val_indices], train_labels_combined[val_indices])
test_dataset = TensorDataset(test_images, test_labels_combined)



# Define training parameters
batch_size = 20
learning_rate = 0.001
num_epochs = 10


# Create data loaders
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)




# Instantiate the model
num_classes = 4  # MNIST has 4 combined classes
model2 = CNN(num_classes=num_classes)
model2 = train_network(train_loader, val_loader, learning_rate, num_epochs, model2)


# Instantiate the improved model
improved_model2 = improved_CNN(num_classes=num_classes)
improved_model2 = train_network(train_loader, val_loader, learning_rate, num_epochs, improved_model2)


# Save the trained model
torch.save(model2.state_dict(), 'cnn_model2.pth')
torch.save(improved_model2.state_dict(), 'improved_cnn_model2.pth')

#  Testing Experimnent number 2
# Load the trained model state dictionary
model2.load_state_dict(torch.load('cnn_model2.pth'))



true_labels, all_predicted_labels = model_test(test_loader, model2)


# Calculate accuracy
accuracy = accuracy_score(true_labels, all_predicted_labels)
print(f'Test Accuracy: {accuracy*100:.2f}%')

# Calculate confusion matrix
conf_matrix = confusion_matrix(true_labels, all_predicted_labels)


# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(true_labels), yticklabels=np.unique(true_labels))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

#  Testing Experimnent number 2 on improved cnn model
# Load the trained model state dictionary
improved_model2.load_state_dict(torch.load('improved_cnn_model2.pth'))
true_labels, all_predicted_labels = model_test(test_loader, improved_model2)

# Calculate accuracy
accuracy = accuracy_score(true_labels, all_predicted_labels)
print(f'Test Accuracy: {accuracy*100:.2f}%')

# Calculate confusion matrix
conf_matrix = confusion_matrix(true_labels, all_predicted_labels)


# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(true_labels), yticklabels=np.unique(true_labels))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()