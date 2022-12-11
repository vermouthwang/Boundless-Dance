import torch

class LSTM_Dance(torch.nn.Module):
    def __init__(self,num_layers):
        super(LSTM_Dance, self).__init__()
        self.L = torch.nn.LSTM(6,6,num_layers)
    def forward(self, sentence):

        sentence = sentence.to(torch.float32)

        return self.L(sentence.view(len(sentence), 1, -1))

model = torch.load('model.pkl')
print("请输入第一个舞者的足部坐标")
x1 = float(input()) 
y1 = float(input()) 
z1 = float(input()) 
print("请输入第一个舞者的手部坐标")
x2 = float(input()) 
y2 = float(input()) 
z2 = float(input()) 

K = [x1,y1,z1,x2,y2,z2]

print(K)
data_in = torch.tensor(K)
data_out = model.forward(data_in.unsqueeze(0).to(torch.float32))
data_out = data_out[0]


print("预测的第二个舞者相对坐标为：",data_out)