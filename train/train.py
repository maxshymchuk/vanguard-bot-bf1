import torch
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import models, datasets, transforms
from torch import nn
from PIL import Image

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
        image = Image.open(self.df.icon[idx]).convert("L")
        label = self.class_list.index(self.df.label[idx])
  
        if self.transform:
            image = self.transform(image)
        return image, label


train_dataset = Bf1Icons(csv_file='datasets/train/bf1iconstrain.csv', class_list=class_labels, transform=data_transform)
test_dataset = Bf1Icons(csv_file='datasets/test/bf1iconstest.csv', class_list=class_labels, transform=data_transform)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=6, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=6, shuffle=False)
train_features, train_labels = next(iter(train_loader))

f, axarr = plt.subplots(1, 6)

indx = 0
for r in range(0, 6):
    img = train_features[indx].squeeze()
    label = train_labels[indx]
    axarr[r].set_facecolor('black')
    axarr[r].imshow(transforms.ToPILImage()(img))
    axarr[r].set_title(class_labels_map.get(str(label.item())))
    indx += 1

plt.show()

device = ("cuda" 
          if torch.cuda.is_available() 
          else "mps"
          if torch.backends.mps.is_available()
          else "cpu")

print(f"Using {device} device")

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(64*256, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 5),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
    
model = NeuralNetwork().to(device)
print(model)

learning_rate = 1e-3
batch_size = 64

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)

    model.train()
    for batch, (images, labels) in enumerate(dataloader):
        images, labels = images.to(device), labels.to(device)
        print(f"Batch {batch}: Image shape {images.shape}, Labels shape {labels.shape}")
        pred = model(images)
        loss = loss_fn(pred, labels)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

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
epochs = 10
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train_loop(train_loader, model, loss_fn, optimizer)
    test_loop(test_loader, model, loss_fn)
print("Done!")

#torch.save(model.state_dict(), 'model_weights.pth')
#model.load_state_dict(torch.load('model_weights.pth', weights_only=True))

model.eval()

data = Image.open('datasets/mp18test.png').convert("L")
plt.imshow(data)
plt.show()
data = data_transform(data)
output = model(data)
prediction = torch.argmax(output)
print(class_labels[prediction.item()])