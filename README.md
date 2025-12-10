# Bot Core

这是一个基于 NapCat 的 QQ 机器人核心框架。

## 功能特性

- **WebSocket 连接**: 支持与 NapCat 建立 WebSocket 连接。
- **插件系统**: 支持动态加载和热重载插件。
- **API 封装**: 提供了完整的 NapCat API 封装。
- **日志系统**: 提供了带有颜色的日志输出。
- **动态配置**: 支持通过代码动态配置 URL 和插件目录。
- **参考文档**: https://napcat.apifox.cn/
## 感谢
感谢 gemini chatGPT 通义 
## 目录结构

```
bot_core/
├── api/            # API 封装
├── bot.py          # 机器人核心类
├── main.py         # 示例入口文件
├── plugin_manager.py # 插件管理器
├── logs.py         # 日志模块
└── __init__.py
```

## 初始化

```python
import asyncio
from bot_core import Bot

async def main():
    # 初始化机器人，指定 WebSocket URL 和插件目录 TOKEN可以为空
    bot = Bot(url=URL, token=TOKEN, plugin_dir="plugins")
    # 启动机器人
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
```

## 插件开发

在 `plugins` 目录（或你指定的目录）下创建 `.py` 文件，定义异步函数即可作为插件加载。

```python
async def my_plugin(msg:Message, client: BotClient):
    # 处理消息逻辑
    pass
```

如果使用原封装api则为

```python
async def my_plugin(msg:dict , client: BotClient):
    # 处理消息逻辑
    pass
```



## 插件开发

### 构造消息链

通过导入类

```python
from api.client import Message
```

~~~python
await client.send_msg()
~~~

#### 发送前缀：

.all(msg)，传入包装后的消息对象，自动识别是否是群或者私聊

.group(group_id||msg)，传入群号或消息对象，发送群消息

.private(user_id||msg)，传入用户id或消息对象，发送私聊消息

#### 其中消息链为：

.text(string)，添加文本消息

.at(int)，传入qq号（仅群聊）

.image(str||url)，传入file://链接以及url

.face(int)，传入face_id

.reply(int)，传入回复的msg_id

**以下方未经测试**

.voice()，添加语音

.video()，添加视频

.json_msg()，json消息

.music()，音乐卡片

.custom_music()，自定义音乐卡片

.dice()，添加骰子

.rps()，猜拳

#### 发送消息缀：

.send()，构造后的结尾缀，发送消息

#### 造消息实例

```python
await client.send_msg().all(msg).reply(msg.message_id).at(msg.user_id).text("你好").image("file:///").send()
```

其含义为，回复消息，群私聊都可以，at用户，发送文字你好，并附带图片

### 注

注：其原封装api都能继续使用

使用需导入

```python
from api.BotClient import BotClient
```


#### 发送群聊消息

| API名称 | 使用方法 |
|---------|----------|
| send_group_msg | `group_id: int, message: str` - 发送群文本消息 |
| send_group_at | `group_id: int, user_id: int, message: str` - 发送群艾特消息 |
| send_group_image | `group_id: int, file: str, url: Optional[str]` - 发送群图片 |
| send_group_face | `group_id: int, face_id: int` - 发送群系统表情 |
| send_group_json | `group_id: int, json_data: Dict[str, Any]` - 发送群JSON消息 |
| send_group_voice | `group_id: int, file: str, url: Optional[str]` - 发送群语音 |
| send_group_video | `group_id: int, file: str, url: Optional[str]` - 发送群视频 |
| send_group_reply | `group_id: int, message_id: int, message: str` - 发送群回复消息 |
| send_group_music_card | `group_id: int, music_type: str, id: str` - 发送群聊音乐卡片 |
| send_group_custom_music_card | `group_id: int, url: str, audio: str, title: str, singer: str, image: Optional[str]` - 发送群聊自定义音乐卡片 |
| send_group_dice | `group_id: int` - 发送群聊超级表情-骰子 |
| send_group_rps | `group_id: int` - 发送群聊超级表情-猜拳 |
| send_group_forward_msg | `group_id: int, messages: List[Dict], source: str, news, prompt: str, summary: str` - 发送群合并转发消息 |
| send_group_file | `group_id: int, file: str, name: str` - 发送群文件 |
| forward_msg_to_group | `group_id: int, message_id: int` - 消息转发到群 |
| send_group_poke | `group_id: int, user_id: int` - 发送群聊戳一戳 |
| send_group_ai_voice | `group_id: int, text: str, voice_id: Optional[int]` - 发送群AI语音 |

#### 发送私聊消息

| API名称 | 使用方法 |
|---------|----------|
| send_private_msg | `user_id: int, message: str` - 发送私聊文本消息 |
| send_private_image | `user_id: int, file: str, url: Optional[str]` - 发送私聊图片 |
| send_private_face | `user_id: int, face_id: int` - 发送私聊系统表情 |
| send_private_json | `user_id: int, json_data: Dict[str, Any]` - 发送私聊JSON消息 |
| send_private_voice | `user_id: int, file: str, url: Optional[str]` - 发送私聊语音 |
| send_private_video | `user_id: int, file: str, url: Optional[str]` - 发送私聊视频 |
| send_private_reply | `user_id: int, message_id: int, message: str` - 发送私聊回复消息 |
| send_private_music_card | `user_id: int, music_type: str, id: str` - 发送私聊音乐卡片 |
| send_private_custom_music_card | `user_id: int, url: str, audio: str, title: str, singer: str, image: Optional[str]` - 发送私聊自定义音乐卡片 |
| send_private_dice | `user_id: int` - 发送私聊超级表情-骰子 |
| send_private_rps | `user_id: int` - 发送私聊超级表情-猜拳 |
| send_private_forward_msg | `user_id: int, messages: List[Dict]` - 发送私聊合并转发消息 |
| forward_msg_to_private | `user_id: int, message_id: int` - 消息转发到私聊 |
| send_private_file | `user_id: int, file: str, name: str` - 发送私聊文件 |
| send_private_poke | `user_id: int` - 发送私聊戳一戳 |

#### 其他消息操作

| API名称 | 使用方法 |
|---------|----------|
| send_poke | `user_id: int, group_id: Optional[int]` - 发送戳一戳 |
| delete_msg | `message_id: int` - 撤回消息 |
| get_group_history_msg | `group_id: int, message_seq: Optional[int]` - 获取群历史消息 |
| get_msg | `message_id: int` - 获取消息详情 |
| get_forward_msg | `message_id: int` - 获取合并转发消息 |
| set_essence_msg | `message_id: int` - 贴表情（设置精华消息） |
| get_friend_history_msg | `user_id: int, message_seq: Optional[int]` - 获取好友历史消息 |
| get_essence_msg_list | `group_id: int` - 获取贴表情详情（获取精华消息列表） |
| send_forward_msg | `messages: List[Dict]` - 发送合并转发消息 |
| get_record | `file: str, out_format: str` - 获取语音消息详情 |
| get_image | `file: str` - 获取图片消息详情 |

#### 群管理相关

| API名称 | 使用方法 |
|---------|----------|
| set_group_kick | `group_id: int, user_id: int, reject_add_request: bool` - 群组踢人 |
| set_group_ban | `group_id: int, user_id: int, duration: int` - 群组单人禁言 |
| set_group_whole_ban | `group_id: int, enable: bool` - 群组全员禁言 |
| set_group_admin | `group_id: int, user_id: int, enable: bool` - 群组设置管理员 |
| set_group_card | `group_id: int, user_id: int, card: str` - 设置群名片（群备注） |
| set_group_name | `group_id: int, group_name: str` - 设置群名 |
| set_group_leave | `group_id: int, is_dismiss: bool` - 退出群组 |
| set_group_special_title | `group_id: int, user_id: int, special_title: str, duration: int` - 设置群组专属头衔 |

#### 信息查询相关

| API名称 | 使用方法 |
|---------|----------|
| get_login_info | 无参数 - 获取登录号信息 |
| get_friend_list | 无参数 - 获取好友列表 |
| get_group_info | `group_id: int, no_cache: bool` - 获取群信息 |
| get_group_list | 无参数 - 获取群列表 |
| get_group_member_info | `group_id: int, user_id: int, no_cache: bool` - 获取群成员信息 |
| get_group_member_list | `group_id: int` - 获取群成员列表 |

#### 请求处理相关

| API名称 | 使用方法 |
|---------|----------|
| set_friend_add_request | `flag: str, approve: bool, remark: str` - 处理加好友请求 |
| set_group_add_request | `flag: str, sub_type: str, approve: bool, reason: str` - 处理加群请求／邀请 |

#### 系统操作相关

| API名称 | 使用方法 |
|---------|----------|
| get_version_info | 无参数 - 获取版本信息 |
| get_status | 无参数 - 获取运行状态 |
| clean_cache | 无参数 - 清理缓存 |

示例：构造转发消息使用方法

```python
messages = [
            {
                "type": "node",
                "data": {
                    "user_id": "1549184870",
                    "nickname": "qwq",
                    "content": [
                        {
                            "type": "text",
                            "data": {
                                "text": message
                            }
                        }
                    ]
                }
            }
        ]
await client.send_group_forward_msg(group_id,messages,"房间数据","点击查看","房间数据")
```

