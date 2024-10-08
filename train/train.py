import torch
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import models, datasets, transforms
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('datasets/bf1icons.csv')

class_labels = ["allowed", "not_allowed"]
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
        image = Image.open(self.df.icon[idx])
        label = self.class_list.index(self.df.label[idx])
  
        if self.transform:
            image = self.transform(image)
        return image, label


icons_dataset = Bf1Icons(csv_file='datasets/bf1icons.csv', class_list=class_labels, transform=data_transform)

train_loader = torch.utils.data.DataLoader(icons_dataset, batch_size=4, shuffle=True)
train_features, train_labels = next(iter(train_loader))

f, axarr = plt.subplots(2, 2)

indx = 0
for r in range(0, 2):
    for c in range(0, 2):
        img = train_features[indx].squeeze()
        label = train_labels[indx]
        axarr[r, c].set_facecolor('black')
        axarr[r, c].imshow(transforms.ToPILImage()(img))
        axarr[r, c].set_title(class_labels_map.get(str(label.item())))
        indx += 1

plt.show()