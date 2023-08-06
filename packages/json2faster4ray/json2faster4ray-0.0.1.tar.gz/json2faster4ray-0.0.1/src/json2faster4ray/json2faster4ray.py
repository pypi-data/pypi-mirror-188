import json
import os

# 讀取label_file與對應id
def label_id(label_file):
    label_id = []
    f = open(label_file)
    for line in f:
        label_id.append(line.split("\n")[0])
    f.close
    return label_id

# 讀取json檔，並將圖片中所有bndbox與相對應label_id回傳
def j_load(json_file, label_file):
    with open(json_file)as f:
        data = json.load(f)
    msg = ''
    label = []
    for i in range(len(data['shapes'])):
        label_ch = label_id(label_file)
        for n in range(len(label_ch)):
            if data['shapes'][i]['label'] == label_ch[n]:
                label.append(n)
    for i in range(len(data['shapes'])):
        msg = msg + str(int(data['shapes'][i]['points'][0][0])) + ',' + str(int(data['shapes'][i]['points'][0][1])) + ',' + str(int(data['shapes'][i]['points'][1][0])) + ',' + str(int(data['shapes'][i]['points'][1][1])) + ',' + str(label[i]) + ' '
    return(msg)

def j2f(json_path, img_path, save_path, label_file):
    for filename in os.listdir(json_path):
        if filename.split(".")[1]=="json":
            json_file = json_path + filename
            msg = j_load(json_file, label_file)
            with open(save_path + "train_carpl.txt", "a") as path_file:
                path_file.write(img_path + filename.split(".")[0] + ".jpg " + msg + "\n")


def main():
    json_path = 'C:/Users/USER/Desktop/tjson/'
    img_path = 'C:/Users/USER/Desktop/labelmejson/'
    save_path = 'C:/Users/USER/Desktop/tjson/'
    label_file = 'C:/Users/USER/Desktop/tjson/carpl-classes.txt'
    
    j2f(json_path, img_path, save_path, label_file)


if __name__=='__main__':
    main()