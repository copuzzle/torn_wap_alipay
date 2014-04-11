Tornado gen 使用
----  

本次使用实例用在支付宝支付流程实例，基本手机 WAP (无线端)

根据最新官方文档   

1.先根据表单数据和收款方账户生提交到支付宝生成 token。   
2.再使用 token 生成支付链接。
3.用户支付宝完成后支付宝返回异步通知。获取通知的数据，去做签名验证和支付宝服务 ATN 验证。  

在没有使用异步实现的情况下，整个生成支付链接的过程需要花1秒左右的时间。  
当然使用无阻塞方式时间会花相差不多的时间，只是对于服务的并发能力来说，会提升很多。  
这里值得一提的是，就是对于生成支付链接这个http请求来说，如果有一个请求阻塞，会造成后面的对于这个的相同请求也阻塞，除非要等到前面的请求超时或者完成。不过这也比全部阻塞好太多了。  
当然我们一般部署方式是使用多进程（mult-process）的方式。

-------------------------------

##Tornado 基本简介

facebook 开源框架， 无阻塞实现WEB服务，支持长链接，kepp-alive

 利用其最新版本异步实现。
 gen.engine
 
 
##使用方法

from wap_alipay import submit


pay_url = yield gen.Task(submit.get_pay_ur, *("订单号"， “订单商品名称”，”“订单费用”)

在方法 get_pay_url 中使用的是基于 gen.engen 实现的 stickless 实现。

代码简释:

```
@gen.engine
def get_pay_url(tn, subject, total_fee, callback=None):
    """get token, ganerate pay_url

    """
    _GATEWAY = "http://wappaygw.alipay.com/service/rest.htm"
    .
    .
    response = yield async_http_client.fetch(request_url, body=data)
    response_params = parse_response(response.body)
    #获得token
    .
    .
    alipay_url = "%s?%s" % (_GATEWAY, alipay_query_str)
    callback(alipay_url)

```