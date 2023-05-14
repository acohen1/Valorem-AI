# Necessary imports
import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from sklearn.utils import shuffle
from privtoken import file_path

class TimeSeriesDataset(Dataset):
    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return len(self.X_data)

def create_dataloaders():
    # Loading the data
    df = pd.read_csv(file_path)

    # Selecting the required columns
    selected_columns = ["time", "open", "high", "low", "close", "50 DMA", "200 DMA", "Volume", "Volume MA", "RSI", "MACD", "Signal"]
    df = df[selected_columns]

    # Handling missing values
    df = df.fillna(method="ffill")

    # Scaling the data
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    # Defining the sequence length and the prediction horizon
    sequence_length = 50
    prediction_horizon = 14

    # Preparing the data for the model
    X = [df_scaled[i - sequence_length:i].values for i in range(sequence_length, len(df_scaled) - prediction_horizon)]
    y = [df_scaled["close"][i:i + prediction_horizon].values for i in range(sequence_length, len(df_scaled) - prediction_horizon)]

    X = np.array(X)
    y = np.array(y)

    # Splitting the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creating PyTorch datasets
    train_dataset = TimeSeriesDataset(torch.from_numpy(X_train).float(), torch.from_numpy(y_train).float())
    val_dataset = TimeSeriesDataset(torch.from_numpy(X_val).float(), torch.from_numpy(y_val).float())

    # Creating PyTorch dataloaders
    batch_size = 32

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_dataloader = DataLoader(val_dataset, batch_size=batch_size)

    return train_dataloader, valid_dataloader

if __name__ == "__main__":
    train_dataloader, valid_dataloader = create_dataloaders()
