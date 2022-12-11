import fbx
import os
import numpy as np
def get_fbxfiles():
    Filename= 'C:\\Users\\double\\Downloads\\双人舞蹈动捕数据\\dongzuo1_test.fbx'
    path = 'C:\\Users\\double\\Downloads\\双人舞蹈动捕数据'
    files = os.listdir(path)
    fbx_files = []
    for file in files:
        if file[-3:]=='fbx':
            fbx_files.append(file)
    return fbx_files

def get_start_nodes():
    path = 'C:\\Users\\double\\Downloads\\双人舞蹈动捕数据'
    
    fbx_files = 'dongzuo1_09'
    print(fbx_files)
    Filename = path+'\\'+fbx_files+'.fbx'

    fbxManager = fbx.FbxManager.Create()
    fbxScene = fbx.FbxScene.Create(fbxManager, "")
    fbxImporter = fbx.FbxImporter.Create(fbxManager, "")
    fbxImporter.Initialize(Filename)
    fbxImporter.Import(fbxScene)
    fbxRoot = fbxScene.GetRootNode()

    nan1  = fbxRoot.GetChild(1)
    nv1 = fbxRoot.GetChild(2)

    node_nv_count = nv1.GetChildCount()
    node_nan_count = nan1.GetChildCount()
    # 提取女 点
    # nv1- RIHAND LTOE

    nv_right_hand_node = None
    nv_left_toe_node = None
    for i in range(node_nv_count):
        # print(nv1.GetChild(i).GetName())
        if(nv1.GetChild(i).GetName()=="nv1:LIHAND"):
            nv_left_hand_node =  nv1.GetChild(i)
            print("get left hand of nv1")

        if(nv1.GetChild(i).GetName()=="nv1:RTOE"):
            nv_right_toe_node = nv1.GetChild(i)
            print("get right toe of nv1")

    nan_right_hand_node = None
    nan_left_toe_node = None
    for i in range(node_nan_count):
        # print(nan1.GetChild(i).GetName())
        if(nan1.GetChild(i).GetName()=="nan1:RIHAND"):
            nan_right_hand_node =  nan1.GetChild(i)
            print("get right hand of nan1")

        if(nan1.GetChild(i).GetName()=="nan1:LTOE"):
            nan_left_toe_node = nan1.GetChild(i)
            print("get left toe of nan1")
    t = fbx.FbxTime(0)
    t.SetMilliSeconds(5700)
    T = 100
    nan_left_toe_node_data = []
    nan_right_hand_node_data = []
    nv_left_hand_node_data = []
    nv_right_toe_node_data = []
    while(T<65280):
        t.SetMilliSeconds(T)
        T+=10
        x1 = nan_left_toe_node.EvaluateGlobalTransform(t)[3][0]
        y1 = nan_left_toe_node.EvaluateGlobalTransform(t)[3][1]
        z1 = nan_left_toe_node.EvaluateGlobalTransform(t)[3][2]
        nan_left_toe_node_data.append([x1,y1,z1])

        x2 = nan_right_hand_node.EvaluateGlobalTransform(t)[3][0]
        y2 = nan_right_hand_node.EvaluateGlobalTransform(t)[3][1]
        z2 = nan_right_hand_node.EvaluateGlobalTransform(t)[3][2]
        nan_right_hand_node_data.append([x2,y2,z2])

        x3 = nv_left_hand_node.EvaluateGlobalTransform(t)[3][0]
        y3 = nv_left_hand_node.EvaluateGlobalTransform(t)[3][1]
        z3 = nv_left_hand_node.EvaluateGlobalTransform(t)[3][2]
        nv_left_hand_node_data.append([x3,y3,z3])

        x4 = nv_right_toe_node.EvaluateGlobalTransform(t)[3][0]
        y4 = nv_right_toe_node.EvaluateGlobalTransform(t)[3][1]
        z4 = nv_right_toe_node.EvaluateGlobalTransform(t)[3][2]
        nv_right_toe_node_data.append([x4,y4,z4])

    print(nan_left_toe_node_data[-1])
    print(nan_right_hand_node_data[-1])
    print(nv_left_hand_node_data[-1])
    print(nv_right_toe_node_data[-1])

    np.save(fbx_files+'nan_left_toe_node.npy',np.asarray(nan_left_toe_node_data))
    np.save(fbx_files+'nan_right_hand_node.npy',np.asarray(nan_right_hand_node_data))
    np.save(fbx_files+'nv_left_hand_node.npy',np.asarray(nv_left_hand_node_data))
    np.save(fbx_files+'nv_right_toe_node.npy',np.asarray(nv_right_toe_node_data))





def main():
    fbx_files = get_fbxfiles()


if __name__ == '__main__':
    get_start_nodes()
    