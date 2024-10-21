import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
import cv2
import numpy as np
from PIL import Image



class CustomImageDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_filenames = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def __len__(self):
        return len(self.image_filenames)

    def __getitem__(self, idx):
        img_name = os.path.join(self.image_dir, self.image_filenames[idx])
        image = Image.open(img_name).convert("RGB")
        label_name = os.path.splitext(img_name)[0] + '.txt'
        with open(label_name, 'r') as file:
            label = np.array([float(x) for x in file.readline().strip().split()])
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label, dtype=torch.float32)



class RectangleNet(nn.Module):
    def __init__(self):
        super(RectangleNet, self).__init__()
        
        # Сверточные слои
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        
        # Полносвязные слои
        self.fc_layers = nn.Sequential(
            nn.Linear(32768, 512),
            nn.ReLU(),
            nn.Linear(512, 2)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x





transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((128, 128))
])
if __name__ == '__main__':
    batch_size = 128
    learning_rate = 0.001
    num_epochs = 20

    image_dir = "dataset"

    train_dataset = CustomImageDataset(image_dir=image_dir, transform=transform)
    train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    model = RectangleNet()
    model.load_state_dict(torch.load('MSE19.pth', weights_only=True))
    model.eval()

    model.cuda()

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    SAVE_EVERY = 5

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for images, targets in train_loader:
            images = images.cuda()
            targets = targets.cuda()
            outputs = model(images)
            loss = criterion(outputs, targets)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.8f}')
        if (epoch + 1) % SAVE_EVERY == 0:
                torch.save(model.state_dict(), f'MSE{epoch}.pth')