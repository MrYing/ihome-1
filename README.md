# 配置
基于`flask`做的一个租房app项目

修改 `ihome/_constants.py`中的
* 云片ak
`API_KEY`
* 七牛空间域名
`QINIU_DOMIN_PREFIX`
* 七牛access_key
`ACCESS_KEY`
* 七牛secret_key
`SECRET_KEY`
* 上传的空间名
`BUCKET_NAME`

重命名为`constants.py`

修改 `_config.py`中的数据库配置信息, 并重命名为`config.py`


# 支付

[https://docs.open.alipay.com/203/107090/](https://docs.open.alipay.com/203/107090/)

运行`openssl`生成密钥,放在`ihome/api_1_0/keys`下,

密钥生成方法
[https://github.com/fzlee/alipay/blob/master/README.zh-hans.md#%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B](https://github.com/fzlee/alipay/blob/master/README.zh-hans.md#%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B)

支付结果应该是以异步通知为准的

[https://docs.open.alipay.com/203/105286/](https://docs.open.alipay.com/203/105286/)

修改`ihome/constants.py`文件中的`ALIPAY_RETURN_URL`