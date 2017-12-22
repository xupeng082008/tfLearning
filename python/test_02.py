#!/usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'xupeng'

import torch
import torchvision
import torchvision.transforms as transforms
#import matplotlib.pyplot as plt
import numpy as np
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

        self.criterion = None
        self.optimizer = None

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def load_data(self):
        print("start loading data ...")
        transform = transforms.Compose(
            [transforms.ToTensor(),
             transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        self.trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                                download=True, transform=transform)
        self.trainloader = torch.utils.data.DataLoader(self.trainset, batch_size=4,
                                                  shuffle=True, num_workers=2)
        self.testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                               download=True, transform=transform)
        self.testloader = torch.utils.data.DataLoader(self.testset, batch_size=4,
                                                 shuffle=False, num_workers=2)
        self.classes = ('plane', 'car', 'bird', 'cat',
                   'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
        print("data load over")
        return self.trainset, self.trainloader, self.testset, self.testloader, self.classes

    def imshow(self, img):
        img = img / 2 + 0.5  # unnormalize
        npimg = img.numpy()
        #plt.imshow(np.transpose(npimg, (1, 2, 0)))

    def set_criterion(self):
        return nn.CrossEntropyLoss()

    def set_optimizer(self):
        return optim.SGD(self.parameters(), lr=0.001, momentum=0.9)

    def train(self):
        print("start training...")
        for epoch in range(2):  # loop over the dataset multiple times

            running_loss = 0.0
            for i, data in enumerate(self.trainloader, 0):
                # get the inputs
                inputs, labels = data
                # wrap them in Variable
                #inputs, labels = Variable(inputs), Variable(labels)
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                # zero the parameter gradients
                self.optimizer = self.set_optimizer()
                self.optimizer.zero_grad()
                # forward + backward + optimize
                outputs = self.forward(inputs)
                self.criterion = self.set_criterion()
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                # print statistics
                running_loss += loss.data[0]
                if i % 2000 == 1999:  # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0

        print('Finished Training')


def main():
    net = Net()
    #net()
    net.cuda()
    trainset, trainloader, testset, testloader, classes = net.load_data()
    """dataiter = iter(testloader)
    images, labels = dataiter.next()
    net.imshow(torchvision.utils.make_grid(images))
    print('GroundTruth: ', ' '.join('%s' % classes[labels[j]] for j in range(4)))"""

    net.train()
    # get some random training images
    """
    dataiter = iter(trainloader)
    images, labels = dataiter.next()
    # show images
    net.imshow(torchvision.utils.make_grid(images))
    # print labels
    print(' '.join('%5s' % classes[labels[j]] for j in range(4)))"""
    print("net run over")





if __name__ == '__main__':
    main()

