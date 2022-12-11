import torch
import numpy as np


class LSTM_Dance(torch.nn.Module):

    def __init__(self,num_layers):
        super(LSTM_Dance, self).__init__()
        self.L = torch.nn.LSTM(6,6,num_layers)
    
    def forward(self, sentence):

        sentence = sentence.to(torch.float32)

        return self.L(sentence.view(len(sentence), 1, -1))


def get_std_mean():
    nans = None
    nvs = None
    for i in range(1,10):
        if(i==1):
            nans,nvs = get_data(i)
            continue
        nan,nv = get_data(i)
        nans = torch.cat((nans,nan),0)
        nvs = torch.cat((nvs,nv),0)
    nan_means = [0,0,0,0,0,0]
    nan_std = [0,0,0,0,0,0]
    nv_means = [0,0,0,0,0,0]
    nv_std = [0,0,0,0,0,0]

    for i in range(0,6):

        nan_means[i] = nans[:,i].mean()
        nan_std[i] = nans[:,i].std()
        nv_means[i] = nv[:,i].mean()
        nv_std[i] = nv[:,i].std()
    print(nan_means,nan_std,nv_means,nv_std)
    return nan_means,nan_std,nv_means,nv_std

def normization():
    nan_means,nan_std,nv_means,nv_std = get_std_mean()
    nans = []
    nvs = []
    for j in range(1,10):
        nan,nv = get_data(j)
        tmp = nan
        nan_means = torch.tensor(nan_means)
        nv_means = torch.tensor(nv_means)
        nan_std = torch.tensor(nan_std)
        nv_std = torch.tensor(nv_std)
        l = nv.shape[0]
        for i in range(l):
            temp = nan[i,:]
            nan[i,:] = (temp-nan_means)/nan_std
            temp = nv[i,:]
            nv[i,:] = (temp-nv_means)/nv_std
        nans.append(nan)
        nvs.append(nv)
    return nans,nvs


def get_data(i):
    nan_left_toe_file = "dongzuo1_0"+str(i)+"nan_left_toe_node.npy"
    nan_right_hand_file = "dongzuo1_0"+str(i)+"nan_right_hand_node.npy"
    nv_right_toe_file = "dongzuo1_0"+str(i)+"nv_right_toe_node.npy"
    nv_left_hand_file = "dongzuo1_0"+str(i)+"nv_left_hand_node.npy"

    nan_left_toe = np.load(nan_left_toe_file)
    nan_right_hand = np.load(nan_right_hand_file)

    nv_right_toe = np.load(nv_right_toe_file)
    nv_left_hand = np.load(nv_left_hand_file)

    t1 = torch.tensor(nan_left_toe)
    t2 = torch.tensor(nan_right_hand)
    nan = torch.cat((t1,t2),1)
    t1 = torch.tensor(nv_right_toe)
    t2 = torch.tensor(nv_left_hand)
    nv = torch.cat((t1,t2),1)
    return nan,nv

# get_std_mean()
# nans, nvs = normization()

# model = LSTM_Dance(3)
# print(model)
# loss_function = torch.nn.L1Loss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# epochs = 200

# for epoch in range(epochs):
#     print(epoch)
#     for i in range(1,10):
#         nan= nans [i-1]
#         nv = nvs [i-1]
#         nan = nan.unsqueeze(1).to(torch.float32)

#         nv = nv.unsqueeze(1).to(torch.float32)

#         optimizer.zero_grad()
#         nv_pred,_ = model(nan)

#         loss = loss_function(nv_pred, nv)
#         loss.backward()
#         optimizer.step()
#         print("loss",loss)
# torch.save(model, 'model.pkl')