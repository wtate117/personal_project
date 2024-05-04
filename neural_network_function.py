import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Function to load and preprocess the dataset
def load_and_preprocess_data(dataset):
    columns_to_drop = ['time', 'conversionType', 'conversionSymbol']
    df = dataset.drop(columns_to_drop, axis=1)
    df = df.drop(df.index[0])  # drop the first row
    df['Pct_Change'] = df['close'].pct_change()
    return df

# Function to split the dataset into training and testing sets
def split_data(df, response_column='Pct_Change'):
    X = df.drop([response_column], axis=1)
    y = pd.DataFrame(df[response_column])
    y.columns = ['Pct Change']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3, random_state=2)
    return X_train, X_test, y_train, y_test

# Function to convert dataframes to tensors
def convert_to_tensor(X_train, y_train, X_test, y_test):
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.float).view(-1, 1)
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.float).view(-1, 1)
    return X_train_tensor, y_train_tensor, X_test_tensor, y_test_tensor

# Neural Network class
class NN_Regression(nn.Module):
    def __init__(self, num_features):
        super(NN_Regression, self).__init__()
        self.layer1 = nn.Linear(num_features, 32)
        self.layer2 = nn.Linear(32, 16)
        self.layer3 = nn.Linear(16, 8)
        self.layer4 = nn.Linear(8, 4)
        self.layer5 = nn.Linear(4, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.layer3(x)
        x = self.relu(x)
        x = self.layer4(x)
        x = self.relu(x)
        x = self.layer5(x)
        return x

# Function to train the model
def train_model(model, X_train_tensor, y_train_tensor, num_epochs=1000, learning_rate=0.01):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    for epoch in range(num_epochs):
        optimizer.zero_grad()
        predictions = model(X_train_tensor)
        loss = criterion(predictions, y_train_tensor)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], MSE Loss: {loss.item()}')

# Function to evaluate the model
def evaluate_model(model, X_test_tensor, y_test_tensor):
    model.eval()
    with torch.no_grad():

        predictions = model(X_test_tensor)

        loss = nn.MSELoss()(predictions, y_test_tensor)
        print(f'Test MSE: {loss.item()}')
        print(f'Test RMSE: {np.sqrt(loss.item())}')
    return predictions

# These functions are prepared to be used in a workflow where data is provided as a filepath to the `load_and_preprocess_data` function.


# Function to run all other functions
def run_all_functions(df):
    df = load_and_preprocess_data(df)
    X_train, X_test, y_train, y_test = split_data(df)
    X_train_tensor, y_train_tensor, X_test_tensor, y_test_tensor = convert_to_tensor(X_train, y_train, X_test, y_test)
    model = NN_Regression(X_train.shape[1])
    train_model(model, X_train_tensor, y_train_tensor)
    eval = evaluate_model(model, X_test_tensor, y_test_tensor)
    return eval