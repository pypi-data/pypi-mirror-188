import os

def split(img_path, json_path):
    for imgname in os.listdir(img_path):
        if imgname.split(".")[1] == "jpg":
            print('ji')
            for filename in os.listdir(json_path):
                if filename.split(".")[0] == imgname.split(".")[0]:
                    os.replace(json_path + filename, img_path + filename)
