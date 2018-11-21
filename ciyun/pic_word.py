# 生成图云
from random import random
from scipy.misc import imread  # 获取颜色
import matplotlib.pyplot as plt
import jieba  # 辅助库，把不必要的词语剔除
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np

# read  word.txt
text = ''
with open('D:\Python_project\PythonPractice\ciyun\word.txt', 'r', encoding='UTF-8') as f:
    text = f.read()
text = text.replace(u"汪淼说", u"汪淼")
text = text.replace(u"汪淼问", u"汪淼")
text = text.replace(u"叶文洁说", u"叶文洁")
text = text.replace(u"元首说", u"元首")
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

wc.to_file("D:\Python_project\PythonPractice\ciyun\wordcloud.png")

# 显示图片
plt.figure()
plt.title("词云图")  # 指定名称
plt.imshow(wc)  # 指定图片形式展示词云
plt.axis("off")  # 关闭图像坐标系
plt.show()

# 设置颜色的话，可以用背景图的颜色里
