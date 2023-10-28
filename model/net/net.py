import torch
from torch import nn
from torch.nn import functional as F

class Net(nn.Module):
    def __init__(self, num_classes: int = 10):
        super(Net, self).__init__()
        
        # Since the input image is a high-resolution 256x256 image (compared to the original 32x32 input size),
        # we need to adapt the convolutional layers to capture more information,
        # and potentially introduce additional layers or increase the kernel sizes.
        
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=2) # 1 input channel, 6 output channels, 5x5 kernel
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0)
        self.conv3 = nn.Conv2d(16, 120, kernel_size=5, stride=1, padding=0)
        
        # We also need to adapt the fully connected layers to handle the larger amount of information.
        # As the image size is significantly larger, the feature map size before the first fully connected layer
        # will be bigger than that in the original LeNet model for 32x32 images.

        # To calculate the size of the feature maps before the first fully connected layer,
        # one needs to account for the operations in the convolutional layers and the pooling layers.
        # Here, we assume that the feature map has a size of (120 * 28 * 28) before the fully connected layers.
        
        self.fc1 = nn.Linear(403680, 84)
        self.fc2 = nn.Linear(84, num_classes)
        
    def forward(self, x):
                # Convolutional layer followed by AvgPool
        x = F.relu(self.conv1(x))
        x = F.avg_pool2d(x, 2)

        # Second convolutional layer followed by AvgPool
        x = F.relu(self.conv2(x))
        x = F.avg_pool2d(x, 2)

        # Third convolutional layer
        x = F.relu(self.conv3(x))

        # Flattening the tensor to a vector for the fully connected layers
        x = torch.flatten(x, 1)

        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.fc2(x)  # No activation is applied in the output layer as it will be used in the loss calculation, e.g., CrossEntropy

        return x
