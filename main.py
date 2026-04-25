import sys
import time

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
import pandas as pd

import AppleDataLogger

if __name__ == "__main__":

    START = time.time()

    # load the data
    transform = transforms.Compose([
        transforms.Resize((128, 128)), transforms.ToTensor()
    ])

    train_data = datasets.ImageFolder("./data/train", transform=transform)
    train_loader = DataLoader(train_data, batch_size=128, shuffle=True, num_workers=4, pin_memory=True,
                              persistent_workers=True)

    print(f"Data loaded in {time.time() - START}")

    # Create CNN Model
    class TurtleCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
            self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
            self.conv3 = nn.Conv2d(32, 64, 3, padding=1)

            self.pool = nn.MaxPool2d(2, 2)

            self.fc1 = nn.Linear(64 * 16 * 16, 128)
            self.fc2 = nn.Linear(128, 2)

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))  # 224 → 112
            x = self.pool(F.relu(self.conv2(x)))  # 112 → 56
            x = self.pool(F.relu(self.conv3(x)))  # 56 → 28

            x = x.view(x.size(0), -1)

            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return x


    # Determine Device
    device = "cpu" # torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    # train the model
    model = TurtleCNN().to(device).float()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    cpu_util_df = None
    cpu_clock_df = None
    scalar_df = pd.DataFrame(columns=["cpu-power", "gpu-power", "gpu-utilization", "gpu-frequency", "time"])

    if sys.platform == "darwin":
        sampler = AppleDataLogger.Sampler()
    elif sys.platform == "linux":
        sampler = None
    else:
        print("Unable to run, no configurations exist for windows. Use linux or MacOS")
        exit(1)

    sampler.start()

    # iterate training
    for epoch in range(100):
        EPOCH_START = time.time()

        model.train()

        # run the training
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # collect the data
        averages = sampler.average_interval(EPOCH_START, time.time())
        # init dataframes
        if epoch == 0:
            cpu_util_df = pd.DataFrame(columns=averages["cpu-utilization"].keys())
            cpu_clock_df = pd.DataFrame(columns=averages["cpu-utilization"].keys())

        # print
        print(f"Epoch {epoch} ({time.time()}) |  Time-Elapsed: {time.time() - EPOCH_START}, Loss: {loss.item()}")

        # Fill N/A if no intervals found for an epoch.
        if not averages:
            averages = {
                "cpu-utilization": None,
                "cpu-frequency": None,
                "cpu-power": None,
                "gpu-power": None,
                "gpu-utilization": None,
                "gpu-frequency": None,
            }

        # add to dataframes
        cpu_util_df.loc[epoch] = averages["cpu-utilization"]
        cpu_clock_df.loc[epoch] = averages["cpu-frequency"]

        scalar_dict = {
            "cpu-power": averages["cpu-power"],
            "gpu-power": averages["gpu-power"],
            "gpu-utilization": averages["gpu-utilization"],
            "gpu-frequency": averages["gpu-frequency"],
            "time": time.time() - EPOCH_START
        }

        scalar_df.loc[epoch] = scalar_dict

    sampler.stop()
    print(f"Training completed in {time.time() - START}")

    # output data
    with pd.ExcelWriter("output.xlsx") as writer:
        cpu_util_df.to_excel(writer, sheet_name="CPU Utilization", index=False)
        cpu_clock_df.to_excel(writer, sheet_name="CPU Frequency", index=False)
        scalar_df.to_excel(writer, sheet_name="Scalars", index=False)






