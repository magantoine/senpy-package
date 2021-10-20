"""

The training of a convolutional neural network can be pretty cumbursome and long. 
SenPy helps you keep track of the training runtime and the evolution of the 
training error.

"""


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR

# We import the SenPy
from senpy import notify_me, ntm

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv = nn.Conv2d(1, 32, 3, 1)

    def forward(self, x):
        x = self.conv(x)
        output = F.relu(x)
        return output

def train(args, model, device, train_loader, optimizer, epoch):
    model.train()

    # ========================================== #
    with ntm(enumerate(train_loader)) as stats :
    # with ntm, SenPy helps us keep track of the computation
    # ==========================================
    
        for batch_idx, (data, target) in stats :
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % args.log_interval == 0:
                
                # ================================================================== #
                # we let SenPy notify us of the current training loss for this epoch
                notify_me('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * len(data), len(train_loader.dataset),
                    100. * batch_idx / len(train_loader), loss.item()))
                # ================================================================== #

                if args.dry_run:
                    break
