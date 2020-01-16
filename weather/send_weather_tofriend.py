import requests
import json
import itchat

from apscheduler.schedulers.blocking import BlockingScheduler  # 定时框架


def get_weather():
    # 成都市的天气
    url = "http://t.weather.sojson.com/api/weather/city/101270101"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        text = response.text
        print(text)
        data = json.loads(text)

        # 今日信息
        today = data['data']['forecast'][0]['ymd']  # 时间
        today_hightem = data['data']['forecast'][0]['high']  # 最高气温
        today_lowtem = data['data']['forecast'][0]['low']  # 最低气温
        today_win = data['data']['forecast'][0]['fx'] + ' ' + data['data']['forecast'][0]['fl']  # 风力
        today_wea = data['data']['forecast'][0]['type']  # 晴
        notice = data['data']['forecast'][0]['notice']  # 注意事项

        # 明日信息
        tomorrow = data['data']['forecast'][1]['ymd']
        tomorrow_hightem = data['data']['forecast'][1]['high']
        tomorrow_lowtem = data['data']['forecast'][1]['low']
        tomorrow_win = data['data']['forecast'][1]['fx'] + ' ' + data['data']['forecast'][1]['fl']
        tomorrow_wea = data['data']['forecast'][1]['type']
        # 信息整合
        today_data = '[' + today + ']' + '\n' + '温度：' + today_hightem + '/' + today_lowtem + '\n' + '天气：' + today_wea + '\n' + '风力：' + today_win + '\n\n'
        tomorrow_data = '[' + tomorrow + ']' + '\n' + '温度：' + tomorrow_hightem + '/' + tomorrow_lowtem + '\n' + '天气：' + tomorrow_wea + '\n' + '风力：' + tomorrow_win
        notice = '\n\n温馨提醒：' + notice
        info = [today_data, tomorrow_data, notice]

        return info
    except  Exception:
        print("异常")


def send_tofriend(info):
    NickName = "filehelper"
    # account = itchat.get_friends(NickName)  # 这里的NickName是你给微信好友的备注
    # for item in account:
    #     if item['RemarkName'] == NickName:  # 由于每次登录时朋友的UserName都会变，所以我们这样做
    #         user = item['UserName']  # 获取微信朋友的UserName
    itchat.send("天气预报:\n" + info[0] + info[1] + info[2], toUserName=NickName)


def method_main():
    info = get_weather()
    send_tofriend(info)


if __name__ == '__main__':
    itchat.auto_login(hotReload=False)
    # enableCmdQR=True, 可以在登陆的时候使用命令行显示二维码
    sched = BlockingScheduler()
    sched.add_job(method_main, 'interval', seconds=30)
    # sched.add_job(method_main, 'cron', month='1-12', day='1-31', hour=7, minute=30)
    sched.start()
    itchat.run()
