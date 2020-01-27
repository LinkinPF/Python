#!/usr/bin/python3

'''
本实验用 50 行 Python 代码完成图片转字符画小工具。
通过本实验将学习到 Linux 命令行操作，Python 基础，pillow 库的使用，argparse 库的使用。

PIL 是一个 Python 图像处理库，是本课程使用的重要工具，使用下面的命令来安装 pillow（PIL）库：
$ sudo pip3 install --upgrade pip
$ sudo pip3 install pillow


实验原理：
	字符画是一系列字符的组合，我们可以把字符看作是比较大块的像素，
	一个字符能表现一种颜色（为了简化可以这么理解），字符的种类越多，
	可以表现的颜色也越多，图片也会更有层次感。

	问题来了，我们是要转换一张彩色的图片，这么多的颜色，要怎么对应到
	单色的字符画上去？这里就要介绍灰度值的概念了。

	灰度值：指黑白图像中点的颜色深度，范围一般从0到255，白色为255，
			黑色为0，故黑白图片也称灰度图像。


	另外一个概念是 RGB 色彩：RGB色彩模式是工业界的一种颜色标准，
						是通过对红(R)、绿(G)、蓝(B)三个颜色通道的变化
						以及它们相互之间的叠加来得到各式各样的颜色的，
						RGB即是代表红、绿、蓝三个通道的颜色，
						这个标准几乎包括了人类视力所能感知的所有颜色，
						是目前运用最广的颜色系统之一。


	灰度值和RGB有换算公式，这里给出一个简单的：gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b

	我们可以创建一个不重复的字符列表，灰度值小（暗）的用列表开头的符号，灰度值大（亮）的用列表末尾的符号。

'''


from PIL import Image
import argparse

# 首先使用argparse来解析命令行参数，目标是获取输入的图片路径
# 输出字符画的宽、高，和输出文件的路径
# 关于argparse模块教程：https://blog.ixxoo.me/argparse.html
parse = argparse.ArgumentParser()

# 定义输入文件、输出文件、输出字符画的宽和高
parse.add_argument('file')			# 输入文件
parse.add_argument('-o','--output')	# 输出文件
parse.add_argument('--width',type=int,default=80)	# 输出字符画宽
parse.add_argument('--height',type=int,default=80)	# 输出字符画高

# 解析并获取参数
args = parse.parse_args()

# 输入的图片的文件路径
IMG=args.file

# 输出字符画的宽度
WIDTH=args.width

# 输出字符画的高度
HEIGHT=args.height

# 输出字符画的路径
OUTPUT=args.output

# 接下来实现将 RGB 转为灰度值，之后使用灰度值映射到字符列表中的某个字符
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 下面是RGB值转字符的函数，alpha值为0的时候表示图片中该位置为空白
def get_char(r,g,b,alpha=256):
	# 判断alpha的值
	if alpha == 0:
		return ' '

	# 获取字符集的长度,这里是70
	length = len(ascii_char)

	# 将RGB转换成灰度值，范围是0-255
	gray=(2126*r + 7125*g + 722*b) / 10000

	# 需要如下的处理才能将灰度值映射到指定的字符上
	x=int((gray / alpha) * len(ascii_char))

	# 返回灰度值对应的字符
	return ascii_char[x]

if __name__ == '__main__':
	
	# 打开并调整图片的宽和高
	im=Image.open(IMG)
	# 把输出的长和宽都设置一下，NEAREST意思是低质量打开图片
	im=im.resize((WIDTH,HEIGHT),Image.NEAREST)

	# 初始化输出的字符
	txt= ""

	# 遍历图片中的每一行
	for i in range(HEIGHT):

		# 遍历该行中的每一列
		for j in range(WIDTH):
			# 下面是一个关键点，使用im的getpixel方法，获取到(j,i)位置的RGB像素值
			# 有时候也会有alpha的值，返回的结果是一个tuple
			txt += get_char(*im.getpixel((j,i)))

		txt += '\n'
	# 输出到屏幕
	print(txt)

	# 字符画输出到文件
	# 这是python的文件IO编程的部分了
	if OUTPUT :
		with open(OUTPUT,'w') as f:
			f.write(txt)
	else:
		with open("output.txt","w") as f:
			f.write(txt)




