import itchat
from itchat.content import TEXT


##回复给自己发送的文本,一样的返回回去
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    if msg['Type'] == TEXT:
        return "你好，我现在不在，您发送的消息【{}】,我已经收到。" .format(msg.text)


itchat.auto_login(hotReload=True)
# //发送给文本助手
itchat.run()
# itchat.send("你好,filehelper",toUserName='filehelper')
