import json
from typing import Any

from flask import Flask, request

from utils import auto_request
from ramox import respond


class WeChatMsg:
    """WeChat messages. Thanks to DaenWxHook.dll created by Daen, this program
    is able to capture messages from WeChat. Visit
    https://www.apifox.cn/apidoc/shared-af49a169-8b5c-4137-a5ea-723a10e8e794/doc-1046131
    for Details. Contact Daen by QQ: 1330166564 for any questions. Each message
    contains many attributions, and the followings are the most userful.
    fromWxid: The WeChat ID of the person who sents the message.
    msg: The text message.
    type: The type of the message. "D0003" represents text messages.
    """

    def __init__(self, req: str) -> None:
        """Initializes the WeChat message. Save the json data received from
        WeChat as a dictionary. Automatically deletes trailing spaces.

        Args:
            req (str): The json data.
        """
        self.data = eval(req)
        if self.data_type == 'D0003':
            while self.msg[-1] == ' ':
                self.msg = self.msg[:-1]

    def __getattr__(self, attr: str) -> Any:
        if attr in self.__dict__:
            return self.__dict__[attr]
        if attr in self.data:
            return self.data[attr]
        return self.data['data'][attr]

    def __str__(self) -> str:
        if self.data_type == 'D0003':
            return remarks[self.fromWxid] + ' ' + self.msg
        return self.data_type


def send_img_download_modification() -> None:
    """Change the image downloading strategy. Images received in WeChat must be
    downloaded before they can be view as files. The parameter "type"
    determines the time period that images received will be automatically be
    downloaded. "23:30-23:30" means that pictures will be automatically
    downloaded all day.
    """
    data = {'type': 'Q0002', 'data': {'type': '23:30-23:30'}}
    auto_request(URL, headers=HEADERS, data=json.dumps(data))


def send_get_personal_info(wxid: str) -> dict:
    """Check the personal information of a user. The information contains many
    attributions, and the followings are the most useful.
    remark: The remark.
    nick: The nickname.

    Args:
        wxid (str): The WeChat ID of the user.

    Returns:
        dict: The dictionary that contains personal information.
    """
    data = {'type': 'Q0004', 'data': {'wxid': wxid}}
    response = auto_request(URL, headers=HEADERS,
                            data=json.dumps(data))['result']
    return response


def send_msg(wxid: str, msg: str) -> None:
    data = {
        'type': 'Q0001',
        'data': {
            'wxid': wxid,
            'msg': msg
        }
    }
    auto_request(URL, headers=HEADERS, data=json.dumps(data))


URL = 'http://127.0.0.1:8055/DaenWxHook/client/'
HEADERS = {
    'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)',
    'Content-Type': 'application/json'
}

app = Flask(__name__)
remarks = {}


@app.route('/wechat', methods=['POST'])
def wechat() -> str:
    global img_download_strategy
    data = WeChatMsg(request.data.decode())
    if data.type == 'D0003':
        info = send_get_personal_info(data.fromWxid)
        if 'remark' in info and info['remark']:
            remarks[data.fromWxid] = info['remark']
        elif 'nick' in info and info['nick']:
            remarks[data.fromWxid] = info['nick']
        else:
            remarks[data.fromWxid] = data.fromWxid
    print(data)
    if data.type != 'D0003' or data.msg[:5] in ['<msg>', '<?xml']:
        return ''
    send_msg(data.fromWxid, respond(data.fromWxid, data.msg))


if __name__ == '__main__':
    app.run(port=8089)