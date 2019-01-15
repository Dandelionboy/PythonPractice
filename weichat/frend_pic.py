import itchat
# 生成图云
from random import random
from scipy.misc import imread  # 获取颜色
import matplotlib.pyplot as plt
import jieba  # 辅助库，把不必要的词语剔除
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from pyecharts import Bar


# 'NickName'好友昵称 
# 'RemarkName':备注
# 'Signature':签名
# 'Province':省
# 'City':市
# 'SEX':性别，1男 2女 0其他


# 返回所有的朋友，每个朋友信息在字典中，放在1个列表里
def my_friend():
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)
    return friends


# 好友性别比例
def my_friends_sex(friends):
    print("好友性别分析中")
    friends_sex = dict()
    male = "男性"
    female = "女性"
    other = '其他'
    # 第一个是自己，不取
    for i in friends[1:]:
        sex = i['Sex']
        # 记录性别的数量
        if sex == 1:
            friends_sex[male] = friends_sex.get(male, 0) + 1
        if sex == 2:
            friends_sex[female] = friends_sex.get(female, 0) + 1
        if sex == 0:
            friends_sex[other] = friends_sex.get(other, 0) + 1
    # 好友总数
    totle = len(friends[1:])
    friend_pencet = [float(friends_sex[male]) / totle * 100, float(friends_sex[female]) / totle * 100,
                     float(friends_sex[other]) / totle * 100]
    # 百分比  %.2f保留两位小数， %%表示百分号
    print("男性好友:%.2f%%" % friend_pencet[0])
    print("女性好友:%.2f%%" % friend_pencet[1])
    print("其他好友:%.2f%%" % friend_pencet[2])
    return friends_sex


# 获取好友的个性签名
def my_friend_sign(friends):
    signs = []
    for friend in friends[1:]:
        signature = friend['Signature'].strip()
        signs.append(signature)
    text = "".join(signs)
    with open(r"D:\Python_project\PythonPractice\weichat\friend_sign.txt", 'a', encoding='utf8') as f:
        f.write(text)


def show_pic():
    # read  word.txt
    text = ''
    with open(r"D:\Python_project\PythonPractice\weichat\friend_sign.txt", 'r', encoding='UTF-8') as f:
        text = f.read()
    text = text.replace(u"^_^", u"")
    text = text.replace(u"span", u"")
    text = text.replace(u"class", u"")
    text = text.replace(u"emoji", u"")
    # 结巴分词，默认精确模式，
    cut_text = jieba.cut(text)
    reslt = '/'.join(cut_text)  # 必须用符号分开
    # 初始化背景图
    # image = Image.open("D:\Python_project\PythonPractice\mask.jpg")
    # graph = np.array(image)
    graph = imread(r"D:\Python_project\PythonPractice\ciyun\mask.jpg")
    # 获取图片的颜色作为文字颜色
    image_colors = ImageColorGenerator(graph)
    # 生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
    wc = WordCloud(font_path=r"D:\Python_project\PythonPractice\ciyun\msyh.ttf", width=600, height=600, margin=10,
                   max_font_size=64
                   , max_words=300, color_func=image_colors, min_font_size=18, background_color='white', mask=graph,
                   mode='RGBA')
    wc.generate(reslt)

    wc.to_file("D:\Python_project\PythonPractice\weichat\wordcloud.png")

    # 显示图片
    plt.figure()
    plt.title("词云图")  # 指定名称
    plt.imshow(wc)  # 指定图片形式展示词云
    plt.axis("off")  # 关闭图像坐标系
    plt.show()

    # 设置颜色的话，可以用背景图的颜色里


def show_sex(friend_sex):
    bar = Bar("朋友圈性别图表")
    bar.add("性别", ["男性", '女性', "其他"], [friend_sex['男性'], friend_sex['女性'], friend_sex['其他']])
    bar.render()


if __name__ == '__main__':
    friends = my_friend()
    sexs=my_friends_sex(friends)
    show_sex(sexs)


    # show_pic()
    # my_friend_sign(friends)
