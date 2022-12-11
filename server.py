import socket
import time
import torch
import train
import datetime
import random
class LSTM_Dance(torch.nn.Module):

    def __init__(self,num_layers):
        super(LSTM_Dance, self).__init__()
        self.L = torch.nn.LSTM(6,6,num_layers)
    
    def forward(self, sentence):

        sentence = sentence.to(torch.float32)

        return self.L(sentence.view(len(sentence), 1, -1))


s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


s.bind(('localhost',7002))

s.sendto(b'send me',('localhost',7003))

model = torch.load('model_discontinous.pkl')
nv_mean = torch.tensor([-0.0221,  0.0013,  0.0405, -0.0216,  0.0013,  0.0384])
nv_std = torch.tensor([0.9606, 0.1431, 0.6865, 1.1525, 0.7251, 1.0365])
pos = [0,0,0,0,0,0]
rate = 0.1
#data_out = null
data_backup = torch.tensor([0,0,0,0,0,0])
endtime = datetime.datetime.now()
while(1):
    starttime = datetime.datetime.now()
    try:
        data,addr = s.recvfrom(1024)
        x1 = float(str(data[:-3],'utf-8'))
        data,addr = s.recvfrom(1024)
        y1 = float(str(data[:-3],'utf-8'))
        data,addr = s.recvfrom(1024)
        z1 = float(str(data[:-3],'utf-8'))
        data,addr = s.recvfrom(1024)
        x2 = float(str(data[:-3],'utf-8'))
        data,addr = s.recvfrom(1024)
        y2 = float(str(data[:-3],'utf-8'))   
        data,addr = s.recvfrom(1024)
        z2 = float(str(data[:-3],'utf-8'))  
        K = [x1,y1,z1,x2,y2,z2]
        data_in = torch.tensor(K)
        # if(random.randint(0,10)==9):
        #     raise ValueError

    except ValueError:
        
        print("value error!")
        data_out = model.forward(data_backup.unsqueeze(0).to(torch.float32))[0]
        print(data_out)
        data_out = data_out.detach().numpy().tolist()[0][0]

        for i in range(6):
            s.sendto(str(data_out[i]).encode(encoding='utf-8'),('localhost',7003))    
        time.sleep(0.1)
        continue
    
    data_out = model.forward(data_in.unsqueeze(0).to(torch.float32))[0]
    #data_out = data_out*nv_std-2*nv_mean
    data_out = data_out.detach().numpy().tolist()[0][0]
    # for i in range(6):
    #     pos[i] = pos[i]+data_out[i]*rate
    #     print(pos[i])
    for i in range(6):
        #s.sendto(str(pos[i]).encode(encoding='utf-8'),('192.168.0.106',7000))    
        s.sendto(str(data_out[i]).encode(encoding='utf-8'),('localhost',7003))    
    time.sleep(0.1)
    print("total time :", (datetime.datetime.now()-endtime).microseconds)
    endtime = datetime.datetime.now()
    print("round time in python:", (endtime-starttime).microseconds)
    

    #s.sendto(b'send me',('192.168.0.106',7000))
    #time.sleep(0.5)