import os
import torch
from torchvision import transforms
from torchvision.io import read_image
from torch.utils.data import Dataset
import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt


class Cleft(Dataset):
    def __init__(self, type, transform=None, target_transform=None, size=(256, 256)):
        self.img_dir = "../data/cleft/train3/images/"
        self.labels_dir = "../data/cleft/train3/landmarks/"

        self.size = size

        self.img_labels = os.listdir(self.img_dir)
        if type == 'train':
            self.img_labels = self.img_labels[:83]
        else:
            self.img_labels = self.img_labels[83:]

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            # transforms.Normalize(mean=[0.485, 0.456, 0.406],
            #                      std=[0.229, 0.224, 0.225])
        ])
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = self.img_dir + self.img_labels[idx]
        image = Image.open(img_path)\

        image = image.resize(self.size)

        label_path = self.labels_dir + self.img_labels[idx][:-4] + '.pts.npy'
        label = np.load(label_path)

        # plt.imshow(image)
        # for x,y in label:
        #     plt.plot(x*256,y*256,'r.',markersize=2)
        # plt.show()

        label = label.flatten()

        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label


if __name__ == "__main__":
    dataset = Cleft(type='train')
    print(len(dataset))
