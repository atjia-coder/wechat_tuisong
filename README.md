# wechat_tuisong
微信测试公众号推送每日天气，建议，每日句子
1：需要配置申请注册一个微信测试公众号 https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login 
2：其中有一项是URL配置Token - 我是通过本地JavaWeb服务器用控制器返回的TOKEN完成验证 
3：配置域名 - NATAPP 3元一个二级域名 
4：扫描二维码 - 获取微信号 
5：设置模板 - 获取模板ID
6：文件下载到本地修改相应的配置文件（默认两个人config/config1 :添加删除后人数变更） 
7：需要定时启动：放在github或aliyun服务器开启定时启动 
    #2 public String getWxUserInfo(HttpServletRequest request, @RequestParam(required = true) String echostr ) { return echostr; }

tips：可联系我的邮箱，扫描我的测试号二维码，放在我的服务器上定时运行 email: 1642879784@qq.com
