# 时区助手 0.4.1

基于[ayaka](https://github.com/bridgeL/ayaka)开发的 时区助手 插件

任何问题请发issue

注意：只适用于群聊！

## 安装插件

`nb plugin install nonebot-plugin-ayaka-timezone`

# 指令
| 指令    | 参数           | 功能                                                                      |
| ------- | -------------- | ------------------------------------------------------------------------- |
| tz_add  | name, timezone | 添加一条时区转换，例如，#tz_add 北京 8，#tz_add 伦敦 0，#tz_add 洛杉矶 -8 |
| tz      | name           | 返回name对应时区的时间，例如 #tz 北京                                     |
| tz      | number         | 返回对应时区的时间，例如 #tz 8                                            |
| tz_list | 无             | 查看所有的时区转换                                                        |
