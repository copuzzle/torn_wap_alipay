# -*- coding: utf-8 -*-


class Settings:
    # 安全检验码，以数字和字母组成的32位字符
    KEY = ''

    INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    PARTNER = ''

    # 签约支付宝账号或卖家支付宝帐户
    SELLER_EMAIL = ''

    # 付完款后跳转的页面（同步通知）要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    RETURN_URL = ''

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    NOTIFY_URL = 'http://127.0.0.1/apilay_callback_url'

    MERCHANT_URL = 'http://127.0.0.1/apilay_merchant_url'

    SHOW_URL = ''

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    TRANSPORT = 'https'

    #签名方式 不需修改
    #ALIPAY_KEY_SIGN_TYPE = '0001'
    SIGN_TYPE = 'MD5'

    GATEWAY = 'https://mapi.alipay.com/gateway.do'