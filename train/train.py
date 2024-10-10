import torch
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import models, datasets, transforms
from torch import nn
from PIL import Image
import torch.nn.functional as F

import warnings
warnings.filterwarnings("ignore")

class_labels = ["artillery_truck", "heavy_bomber", "smg08", "rifle_launcher", "allowed"]
class_labels_map = {}
for indx, label in enumerate(class_labels):
    class_labels_map[str(indx)] = label

data_transform = transforms.Compose([transforms.Resize((64, 256)), 
                                             transforms.ToTensor()])

class Bf1Icons(Dataset):

    def __init__(self, csv_file, class_list, transform=None):
        """
        Arguments:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.df= pd.read_csv(csv_file)
        self.class_list = class_list
        self.transform = transform

    def __len__(self):
        return self.df.shape[0]

    def __getitem__(self, idx):
        image = Image.open(self.df.icon[idx]).convert("RGB")
        label = self.class_list.index(self.df.label[idx])
  
        if self.transform:
            image = self.transform(image)
        return image, label


train_dataset = Bf1Icons(csv_file='datasets/train/bf1iconstrain.csv', class_list=class_labels, transform=data_transform)
test_dataset = Bf1Icons(csv_file='datasets/test/bf1iconstest.csv', class_list=class_labels, transform=data_transform)

num_classes = len(class_labels)
batch_size = 5
epochs = 10
learning_rate = 1e-3

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size, shuffle=False)
train_features, train_labels = next(iter(train_loader))

f, axarr = plt.subplots(1, 5)

for r in range(0, 5):
    img = train_features[r].squeeze()
    label = train_labels[r]
    axarr[r].set_facecolor('black')
    axarr[r].imshow(transforms.ToPILImage()(img))
    axarr[r].set_title(class_labels_map.get(str(label.item())))

plt.show()

device = ("cuda" 
          if torch.cuda.is_available() 
          else "mps"
          if torch.backends.mps.is_available()
          else "cpu")

print(f"Using {device} device")

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.conv_layer1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3)
        self.conv_layer2 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3)
        self.max_pool1 = nn.MaxPool2d(kernel_size = 2, stride = 2)
        
        self.conv_layer3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)
        self.conv_layer4 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3)
        self.max_pool2 = nn.MaxPool2d(kernel_size = 2, stride = 2)
        
        self.fc1 = nn.Linear(64*13*61, 128) 
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(128, num_classes)
    def forward(self, input):
        out = self.conv_layer1(input)
        out = self.conv_layer2(out)
        out = self.max_pool1(out)
        
        out = self.conv_layer3(out)
        out = self.conv_layer4(out)
        out = self.max_pool2(out)
                
        out = out.reshape(out.size(0), -1)
        
        out = self.fc1(out)
        out = self.relu1(out)
        out = self.fc2(out)
        return out
    
model = NeuralNetwork().to(device)

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)

    model.train()
    for batch, (images, labels) in enumerate(dataloader):
        print(f"Batch {batch}: Image shape {images.shape}, Labels shape {labels.shape}")

        optimizer.zero_grad()
        pred = model(images)
        loss = loss_fn(pred, labels)

        loss.backward()
        optimizer.step()

        if batch % 10 == 0:
            loss, current = loss.item(), batch * batch_size + len(images)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test_loop(dataloader, model, loss_fn):
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0
    
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
model.to(device)
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train_loop(train_loader, model, loss_fn, optimizer)
    test_loop(test_loader, model, loss_fn)
print("Done!")

#torch.save(model.state_dict(), 'model_weights.pth')
#model.load_state_dict(torch.load('model_weights.pth', weights_only=True))

model.eval()

# data = Image.open('datasets/mp18test.png').convert("L")
# plt.imshow(data)
# plt.show()
# data = data_transform(data)
# output = model(data)
# prediction = torch.argmax(output)
# print(class_labels[prediction.item()])
