from meutils.pipe import *
from meutils.hash_utils import *

key = '1eb25317-39a1-4af7-a6e3-63877ec2dd64'
hook_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'  # 发送消息接口地址


def wx_post(file='wechat.py'):
    id_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file'  # 上传文件接口地址
    data = {'file': open(file, 'rb')}  # post jason
    response = requests.post(url=id_url, files=data)  # post 请求上传文件
    json_res = response.json()  # 返回转为json
    print(json_res)
    media_id = json_res['media_id']  # 提取返回ID

    wx_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'  # 发送消息接口地址
    data = {"msgtype": "file", "file": {"media_id": media_id}}  # post json
    r = requests.post(url=wx_url, json=data)  # post请求消息
    return r  # 返回请求状态



if __name__ == '__main__':
    print(wx_post().text)