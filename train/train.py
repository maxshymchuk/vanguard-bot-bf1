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
        image = Image.open(self.df.icon[idx]).convert("L")
        label = self.class_list.index(self.df.label[idx])
  
        if self.transform:
            image = self.transform(image)
        return image, label


train_dataset = Bf1Icons(csv_file='datasets/train/bf1iconstrain.csv', class_list=class_labels, transform=data_transform)
test_dataset = Bf1Icons(csv_file='datasets/test/bf1iconstest.csv', class_list=class_labels, transform=data_transform)

num_classes = len(class_labels)
batch_size = 16
epochs = 50
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
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(12)
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=12, kernel_size=5, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(12)
        self.pool = nn.MaxPool2d(2,2)
        self.conv4 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn4 = nn.BatchNorm2d(24)
        self.conv5 = nn.Conv2d(in_channels=24, out_channels=24, kernel_size=5, stride=1, padding=1)
        self.bn5 = nn.BatchNorm2d(24)
        self.fc1 = nn.Linear(76128, num_classes)
    def forward(self, input):
        output = F.relu(self.bn1(self.conv1(input)))      
        output = F.relu(self.bn2(self.conv2(output)))     
        output = self.pool(output)                        
        output = F.relu(self.bn4(self.conv4(output)))     
        output = F.relu(self.bn5(self.conv5(output)))     
        output = output.view(output.size(0), -1)
        output = self.fc1(output)
        return output
    
model = NeuralNetwork().to(device)

# Function to save the model
def saveModel():
    path = "./model_weights.pth"
    torch.save(model.state_dict(), path)

def testaccuracy():
    model.eval()

    accuracy = 0.0
    total = 0.0
    
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            outputs = model(images.to(device))
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            accuracy += (predicted == labels.to(device)).sum().item()

    accuracy = (100 * accuracy / total)
    return accuracy

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

def train():
    model.train()

    best_accuracy = 0.0

    for epoch in range(epochs):
        running_loss = 0.0
        for batch, (images, labels) in enumerate(train_loader):
            print(f"Batch {batch}: Image shape {images.shape}, Labels shape {labels.shape}")

            optimizer.zero_grad()
            pred = model(images)
            loss = loss_fn(pred, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if batch % 1000 == 999:
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, batch + 1, running_loss / 1000))
                running_loss = 0.0
    
        accuracy = testaccuracy()
        print('For epoch', epoch+1,'the test accuracy over the whole test set is %d %%' % (accuracy))

        if accuracy > best_accuracy:
            saveModel()
            best_accuracy = accuracy

    print('Best accuracy', best_accuracy)

model.to(device)
train()
print("Done!")

#torch.save(model.state_dict(), 'model_weights.pth')
#model.load_state_dict(torch.load('model_weights.pth', weights_only=True))
def run_model(image_path):
    data = Image.open(image_path).convert("L")
    plt.imshow(data)
    plt.show()
    data = data_transform(data)
    data = data.unsqueeze(0)
    data = data.to(device)
    output = model(data)
    prediction = torch.argmax(output)
    print('File:', image_path, 'Classification:', class_labels[prediction.item()])

model.eval()

run_model('datasets/test/hatchet.png')
run_model('datasets/test/smg08_small.png')
run_model('datasets/train/artytruck_small.png')
run_model('datasets/farq.png')