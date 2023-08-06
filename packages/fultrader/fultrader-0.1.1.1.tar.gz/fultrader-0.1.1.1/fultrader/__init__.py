# -*- coding: utf-8 -*-
import requests

# version_url = 'https://ultronsandbox.oss-cn-hangzhou.aliyuncs.com/version/ultron.json'

__all__ = ['__version__']

__version__ = "0.1.0"


# def get_version():
#     res = requests.get(version_url).json()
#     if res.get('code') != 200:
#         return '', ''

#     remote_version = res['data']['version']
#     content = res['data']['content']

#     return remote_version, content


# def check_version():
#     remote_version, content = get_version()
#     if not remote_version or remote_version <= __version__:
#         return
#     print('Ultron 版本由%s升级到%s,升级内容%s,执行 pip install --uprgrade Finance-Ultron' %
#           (__version__, remote_version, content))


def get_version():

    return print(f'当前软件版本为：{__version__}, trader for commodity fulture')


get_version()