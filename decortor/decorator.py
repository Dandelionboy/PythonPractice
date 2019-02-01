'''
#在没学函数，之前，在函数中直接print
x学了函数，就封装一个函数，然后，在另外一个中调用
但是  装饰器的原则
1.不能修改被装饰的函数的源代码
2.不能修改被装饰的函数的调用方式。
==========
.实现装饰器的知识储备
1。函数就是变量
2.高阶函数（满足其中一个）
    a:把一个函数名当做实参传递给另外一个函数
    b.返回值中包含函数名
3.嵌套函数
'''
# 模拟web端界面验证登录，1个函数相当于一个web界面，3个界面有2个登录验证
import time

usename, pw = "ph", "123"


def auth(auth_type):
    # print("auth_func",auth_type)
    def out_wrapper(func):
        def wapper(*args, **kwargs):  # 此处使用为函数可能带参数如
            if auth_type == "qq":
                username = input("请输入用户名：").strip()
                password = input("输入密码").strip()
                if usename == username and password == pw:
                    print("欢迎", username)
                    s = func(*args, **kwargs)
                    return s  # 函数能返回home中的返回值
                else:
                    exit("\033输入错误无法登录")
            else:
                print("暂时不支持微信登录")

        return wapper  # 作为变量是不能加括号的

    return out_wrapper


def index():
    print("welcome，首页")  # 不需要登录


@auth(auth_type="qq")
def home(star=32):
    print("welcome，个人中心,默认指数", star)  # 需要登录
    return "from home"  # 为什么没有执行的结果？在wapper中要return才有


@auth(auth_type="weixin")  # 高潮，对home.bbs进行不同的认证
def bbs():
    print("welcome，论坛")  # 需要登录


index()
choose = input("请选择登录方式:qq or weixin:")
if choose == "qq":
    home()
elif choose == "weixin":
    bbs()
# print(home())#没有返回值，因为warpper()也没返回值，需要加return
