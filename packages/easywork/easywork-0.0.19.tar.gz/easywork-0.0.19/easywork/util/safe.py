import base64
import os
import re

import easywork.util.time as time
import requests
import win32api
import win32con
import wmi
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def get_beijing_time():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        url = 'https://www.beijing-time.org/t/time.asp'
        rtn = requests.get(url, headers=headers, timeout=3).text
        y = re.findall('nyear=(.*?);', rtn)[0]
        m = re.findall('nmonth=(.*?);', rtn)[0].zfill(2)
        d = re.findall('nday=(.*?);', rtn)[0].zfill(2)
        return time.strptime(f'{y}-{m}-{d}', time.FORMAT_DATE)
    except:
        return None


def get_mac():
    return wmi.WMI().Win32_Processor()[0].ProcessorId


def encrypt(secret, text):
    factory = AES.new(bytes(secret, encoding='utf8'), AES.MODE_ECB)
    text = factory.encrypt(pad(bytes(text, encoding='utf8'), 32))
    return str(base64.b64encode(text), encoding='utf-8')


def decrypt(secret, data):
    factory = AES.new(bytes(secret, encoding='utf8'), AES.MODE_ECB)
    data = factory.decrypt(base64.b64decode(data))
    return bytes.decode(unpad(data, 32))


def check(secret):
    try:
        with open('key', 'r') as f:
            data = f.read()
        rtn = decrypt(secret, data).split('_')
        if rtn[0] == get_mac() and time.differ_days(time.strptime(rtn[1], time.FORMAT_DATE), get_beijing_time()) >= 0:
            return
    except:
        pass
    win32api.MessageBox(0, '试用到期，请联系管理员获取激活码！', '提示', win32con.MB_OK)
    os._exit(0)
