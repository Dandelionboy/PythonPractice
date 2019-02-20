import os
images_psth=os.path.join(os.path.dirname(os.path.dirname(__file__)),"images")
#D:/Python_project/SpiderDemo/bmw\images
if not os.path.exists(images_psth):
    print("不存在")
    os.mkdir(images_psth)
else:
    print("存在")
