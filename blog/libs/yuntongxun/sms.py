
from django.conf import settings

# 注：在配置文件dev中完成四个配置信息
# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
from libs.yuntongxun.CCPRestSDK import REST

_accountSid = '8aaf07087a331dc7017a41faf58e067b'
# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = 'd1c840e76e5b4669aa86225b93af06a9'
# 说明：请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf07087a331dc7017a41faf7080681'
# 说明：请求地址，生产环境配置成app.cloopen.com，开发环境配置成sandboxapp.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"
# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'


def send_sms(mobile, code_expire_tuple, temp_id):
    # 配置
    rest = REST(_serverIP, _serverPort, _softVersion)
    rest.setAccount(_accountSid, _accountToken)
    rest.setAppId(_appId)
    # 发送
    result = rest.sendTemplateSMS(mobile, code_expire_tuple, temp_id)
    # 结果：信息成功发生，结果字典result中 statuCode 字段为 "000000"
    if result.get("statusCode") == "000000":
        print('发送成功')
        return True  # 表示发送短信成功
    else:
        print('发送失败')
        return False  # 表示发送失败


if __name__ == '__main__':
    send_sms('19934005895', ['1234', 5], 1)
