# 云账户 SDK for Python

欢迎使用云账户 SDK for Python。  
云账户是一家专注为平台企业和新就业形态劳动者提供高质量灵活就业服务的新时代企业。云账户 SDK 对云账户综合服务平台 API 接口进行封装，让您不必关心过多参数请求，帮助您快速接入到云账户综合服务平台。云账户 SDK for Python 为您提供签约、下单、回调、数据查询等功能，帮助您完成与云账户综合服务平台的接口对接及业务开发。  
如果您在使用过程中遇到任何问题，欢迎在当前 GitHub 提交 Issues，或发送邮件至技术支持组 [techsupport@yunzhanghu.com](mailto:techsupport@yunzhanghu.com)。

### 环境要求

云账户 SDK for Python 支持 Python3 及其以上版本。

### 配置密钥

#### 1、获取配置

使用云账户 SDK for Python 前，您需先获取 dealer_id、broker_id、3DES Key、App Key 信息。    
获取方式：使用开户邮件中的账号登录【[云账户综合服务平台](https://service.yunzhanghu.com/user/login)】，选择“业务中心 > 业务管理 > 对接信息”，查看并获取以上配置信息。  
![获取配置信息](https://infra-engineering-yos-prod.obs.cn-north-1.myhuaweicloud.com/3edacfcb8f2f689d3ee6e9e7aba983139a8ec869-duijiexinxi.png)

#### 2、生成密钥

- 方式一：使用 OpenSSL 生成 RSA 公私钥

```
① ⽣成私钥 private_key.pem

Openssl-> genrsa -out private_key.pem 2048 位  // 建议密钥⻓度⾄少为 2048 位

OpenSSL-> pkcs8 -topk8 -inform PEM -in private_key.pem -outform PEM -nocrypt -out private_key_pkcs8.pem  // 将私钥转为 PKCS8 格式 

② ⽣成公钥⽂件 pubkey.pem

Openssl-> rsa -in private_key.pem -pubout -out pubkey.pem

```

- 方式二：使用工具生成

请联系云账户技术支持获取 RSA 密钥生成工具

#### 3、配置密钥

登录【[云账户综合服务平台](https://service.yunzhanghu.com/user/login)】，选择“业务中心 > 业务管理 > 对接信息”，单击页面右上角的“编辑”，配置平台企业公钥。
![配置平台企业公钥信息](https://infra-engineering-yos-prod.obs.cn-north-1.myhuaweicloud.com/6cfd4c1c6560b7ae99d5c3cb358aea23b9433c58-dujiexinxi-2.png)

### 安装Python SDK

1、pip install yzh_py 

如有特殊需求需要源码，请联系云账户技术支持。

### 快速使用

#### 示例

```

from yzh_py.client.api.model.payment import GetOrderRequest
from yzh_py.client.api.payment_client import PaymentClient
from yzh_py.config import *

if __name__ == "__main__":
    config = Config(
        host="https://api-service.yunzhanghu.com",
        dealer_id="", 
        sign_type="",
        app_key="",
        des3key="",
        private_key="",
        public_key="",
    )
    # 获取订单详情
    request = GetOrderRequest(
        order_id="",
        channel="微信",
        data_type="encryption"
    )
    client = PaymentClient(config)
    resp = client.get_order(request)

    print(resp.code, resp.message, resp.data)

```
