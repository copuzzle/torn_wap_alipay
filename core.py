# -*- coding: utf-8 -*-
from urllib import urlencode
import xml.etree.ElementTree as Etree
from tornado.escape import utf8
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from config import Settings
from hashcompat import md5_constructor


def build_request_params(params):
    params, prestr = params_filter(params)
    mysign = build_mysign(prestr, Settings.KEY)
    params.update({"sign": mysign})
    if params["service"] not in ("alipay.wap.trade.create.direct",
                                 "alipay.wap.auth.authAndExecute"):
        params.update({"sign_type": Settings.SIGN_TYPE})
    return params


def params_filter(params):
    """sort the params dict and exclude "sign, sign_type", and enmpty keys
    """

    ks = params.keys()
    ks.sort()
    new_params = {}
    prestr = ""
    for k in ks:
        v = params[k]
        if k not in ("sign", "sign_type") and v != '':
            new_params[k] = utf8(v)
            prestr += "%s=%s&" % (k, new_params[k])
    prestr = prestr[:-1]
    return new_params, prestr


def fixed_params_filter(params):
    """sort the params dict and exclude "sign, sign_type", and enmpty keys
    """
    ks = params.keys()
    new_params = {}
    for k in ks:
        v = params[k]
        if k not in ("sign", "sign_type") and v != '':
            new_params[k] = utf8(v)
    prestr = "service=%s&v=%s&sec_id=%s&notify_data=%s" % (
        new_params["service"],
        new_params["v"],
        new_params["sec_id"],
        new_params["notify_data"])
    return new_params, prestr


def build_mysign(prestr, key):
    """hash value + key by md5

    """
    sign_type = Settings.SIGN_TYPE
    if sign_type == "MD5":
        return md5_constructor(prestr+key).hexdigest()
    return ""


@gen.engine
def notify_verify(post, callback=None):
    """验证---签名&&数据是否支付宝发送

    """
    #初级验证---签名
    order_params = {}
    params = {}
    _, prestr = fixed_params_filter(post)
    mysign = build_mysign(prestr, Settings.KEY)
    if mysign != post.get('sign'):
        callback(False)
        return
    tree = Etree.fromstring(post["notify_data"])
    notify_id = tree.find("notify_id").text
    order_params["trade_no"] = tree.find("trade_no").text
    order_params["out_trade_no"] = tree.find("out_trade_no").text
    order_params["trade_status"] = tree.find("trade_status").text
    order_params["total_fee"] = float(tree.find("total_fee").text)

    #二级验证---数据是否支付宝发送
    if notify_id:
        params['partner'] = Settings.PARTNER
        params['notify_id'] = notify_id
        if Settings.TRANSPORT == 'https':
            params['service'] = 'notify_verify'
            gateway = 'https://mapi.alipay.com/gateway.do'
        else:
            gateway = 'http://notify.alipay.com/trade/notify_query.do'
        verify_url = "%s?%s" % (gateway, urlencode(params))
        async_client = AsyncHTTPClient()
        response = yield async_client.fetch(verify_url)
        if response.body.lower().strip() == 'true':
            callback(order_params)
            return
    callback(False)


def return_verify(query_params):
    """同步通知验证

    """
    _, prestr = params_filter(query_params)
    mysign = build_mysign(prestr, Settings.KEY)
    if mysign != query_params.get('sign'):
        return False
    return True
