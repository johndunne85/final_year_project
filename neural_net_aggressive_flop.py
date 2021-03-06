import pandas as pd
import torch
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


names_data = pd.read_csv('aggressive_flop.csv')

names_data.head()

from sklearn import preprocessing

le = preprocessing.LabelEncoder()
names_data['result'] = le.fit_transform(names_data['result'])
names_data['card1'] = le.fit_transform(names_data['card1'])
names_data['card2'] = le.fit_transform(names_data['card2'])
names_data['card3'] = le.fit_transform(names_data['card3'])
names_data['card4'] = le.fit_transform(names_data['card4'])
names_data['card5'] = le.fit_transform(names_data['card5'])
names_data['bet1'] = le.fit_transform(names_data['bet1'])
names_data['bet2'] = le.fit_transform(names_data['bet2'])
names_data.head()

features = ['card1','card2','card3','card4','card5','bet1','bet2']

poker_features = names_data[features]
poker_features.head()

poker_target = names_data[['result']]
poker_target.head()

from sklearn.model_selection import train_test_split
X_train, x_test, Y_train, y_test = train_test_split(poker_features,
                                                   poker_target,
                                                   test_size=0.2,
                                                   random_state=0)

X_train.shape, Y_train.shape

Xtrain_ = torch.from_numpy(X_train.values).float()
Xtest_ = torch.from_numpy(x_test.values).float()
Xtrain_.shape

Ytrain_ = torch.from_numpy(Y_train.values).view(1,-1)[0]
Ytest_ = torch.from_numpy(y_test.values).view(1,-1)[0]

Ytrain_.shape

input_size = 7
output_size = 2
hidden_size = 32
hidden_size2 = 64

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size2)
        self.fc3 = nn.Linear(hidden_size2, output_size)

    def forward(self, x):
        x = torch.sigmoid(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        x = self.fc3(x)

        return F.log_softmax(x, dim=-1)

model = Net()

import torch.optim as optim

optimizer = optim.Adam(model.parameters())

loss_fn = nn.NLLLoss()

epoch_data = []
epochs = 1501

# for epoch in range(1, epochs):
#
#     optimizer.zero_grad()
#     Ypred = model(Xtrain_)
#
#     loss = loss_fn(Ypred, Ytrain_)
#     loss.backward()
#
#     optimizer.step()
#
#     Ypred_test = model(Xtest_)
#     loss_test = loss_fn(Ypred_test, Ytest_)
#
#     _,pred = Ypred_test.data.max(1)
#
#     accuracy = pred.eq(Ytest_.data).sum().item() / y_test.values.size
#     epoch_data.append([epoch, loss.data.item(), loss_test.data.item(), accuracy])
#
#     if epoch % 100 == 0:
#         print('epoch - %d (%d%%) train loss - %.2f test loss - %.2f accuracy - %.4f'\
#              % (epoch, epoch/150 * 10, loss.data.item(), loss_test.data.item(), accuracy))
#
# torch.save(model.state_dict(),'checkpoint_agg_flop.pth')

state_dict_agg_flop = torch.load('checkpoint_agg_flop.pth')

model.load_state_dict(state_dict_agg_flop)

def test_cards_agg_flop(card):
    with torch.no_grad():
        logits = model.forward(card)

    ps = F.softmax(logits,dim=1)

    print('Probability from neural network at flop -> {}'.format(ps))
    if ps[0][0] > ps[0][1]:
        return('fold', ps)
    else:
        return('raise',ps)
