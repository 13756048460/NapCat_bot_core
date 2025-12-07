# Bot Core

这是一个基于 NapCat_api开发的的 QQ 机器人核心python框架包。

## 功能特性

- **WebSocket 连接**: 支持与 NapCat 建立 WebSocket 连接。
- **插件系统**: 支持动态加载和热重载插件。
- **API 封装**: 提供了完整的 NapCat API 封装。
- **日志系统**: 提供了带有颜色的日志输出。
- **动态配置**: 支持通过代码动态配置 URL 和插件目录。
- **参考文档**: https://napcat.apifox.cn/

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
async def my_plugin(msg, client):
    # 处理消息逻辑
    pass
```

## 插件实例


```python
import requests

from api import BotClient
from logs import Logger

async def menu(msg:dict , client: BotClient):
    if msg.get("message_type") != "group":
        return
    if msg.get("raw_message") == "数据列表":
        group_id = msg.get("group_id")
        msg = (
            "数据列表：\n"
            "--------------------\n"
            "战网数据\n"
            "房间数据\n"
            "战网阵营胜率\n"
            "战网日冕阵营胜率\n"
            "--------------------"
        )
        await client.send_group_msg(group_id, msg)
async def menu2(msg:dict , client: BotClient):
    if msg.get("message_type") != "group":
        return
    if msg.get("raw_message") == "菜单":
        group_id = msg.get("group_id")
        await client.send_group_msg(group_id, "自动问答机")
async def ra3(msg:dict , client: BotClient):
    if msg.get("message_type") != "group":
        return
    if msg.get("raw_message") == "战网数据":
        group_id = msg.get("group_id")
        API_URL = "http://api.ra3battle.cn/api/server/status"
        try:
            getJson = requests.get(API_URL)
            getJson.raise_for_status()  # 添加异常处理
        except requests.RequestException as e:
            msg = f"API请求失败: {e}"
            await client.send_group_msg(group_id, msg)
        data = getJson.json()  # 简化变量名
        players = len(data["players"])
        if not data["players"] and not data["games"]:
            msg = f"根据api获取json为\n-------------------\n{data}\n-------------------\n获取players和games内的数据为空\n疑似战网崩溃或战网内暂无玩家\n如崩溃则联系战网管理"
            await client.send_group_msg(group_id, msg)
        Total = data["games"]
        total_players = sum(len(game["players"]) for game in Total)
        Idle_player = players - total_players
        count1v1D = data['automatching']['count1v1Details']
        count1v1 = count1v1D.get('ra3', 0)
        count1v1R = count1v1D.get('corona', 0)
        mate_room = str(len(data["automatch"]))
        closed_playing_count = sum(1 for game in Total if game["gamemode"] == 'closedplaying')
        preparing_games = len(Total) - closed_playing_count
        msg = (
            "房间详细数据请发送\"房间数据\"\n"
            "--------------------\n"
            f"当前在线人数：{players}\n"
            f"正在对局玩家：{total_players}\n"
            f"闲置玩家：{Idle_player}\n"
            "--------------------\n"
            f"自动匹配寻找对局的玩家：{count1v1}\n"
            f"日冕自动匹配寻找对局的玩家：{count1v1R}\n"
            "--------------------\n"
            f"正在进行匹配对战的房间总数：{mate_room}\n"
            f"正在进行游戏的房间个数：{closed_playing_count}\n"
            f"正在准备的房间个数：{preparing_games}\n"
            "--------------------"
        )
        await client.send_group_msg(group_id, msg)
        
async def room_data(msg:dict , client: BotClient):
    if msg.get("message_type") == "group":
        Logger().debug("非群消息")
    if msg.get("raw_message") == "房间数据":
        group_id = msg.get("group_id")
        url = "https://api.ra3battle.cn/api/server/status"
        req = requests.get(url)
        games = req.json()["games"]
        data = []
        homeSum = 0
        for game in games:
            if game["gamemode"] == "openstaging":
                homeSum += 1
                if not game["players"]:
                    names = "NUll"
                else :
                    names = game["players"][0]["name"]
                homeName = game["hostname"].split()[1]
                modName = game["mod"]
                if modName == "RA3":
                    modName = "原版"
                if modName == "corona":
                    modName = "日冕"
                mapName = game["mapname"].replace("\\", "/").split("/")
                mapName = mapName.pop().split(".")[0]
                data.append(
                    "房间名：" + homeName + "\n" + "地图名：" + mapName + "\n" + "房主名：" + names + "\n" + "MOD名：" + modName + "\n" + "房间内人数：" + str(len(
                        game["players"])) +"\n"+"------------------------------"+"\n")
        out = ''.join(data)
        textT = "正在准备的房间数：" + str(homeSum) + "\n" + "------------------------------" + "\n"
        message = textT + out
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

async def hello_reply(msg: dict, client: BotClient):
    """当收到'你好'时回复这条消息并@发送者加你好"""
    if msg.get("message_type") != "group":
        return
    if msg.get("raw_message") == "你好":
        group_id = msg.get("group_id")
        user_id = msg.get("user_id")
        message_id = msg.get("message_id")
        
        # 使用send_group_msg直接发送包含回复、@和文本的消息
        import json
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "reply",
                        "data": {
                            "id": message_id
                        }
                    },
                    {
                        "type": "at",
                        "data": {
                            "qq": str(user_id)
                        }
                    },
                    {
                        "type": "text",
                        "data": {
                            "text": " 你好"
                        }
                    }
                ]
            }
        }
        await client.websocket.send(json.dumps(json_msg))

```


## 已实现api

```python
"""
NapCat 消息相关 API
参考文档: https://napcat.apifox.cn/
"""
import json
import asyncio
from typing import Optional, List, Dict, Any
from logs import Logger



class BotClient:
    def __init__(self, websocket):
        self.websocket = websocket
        self.logger = Logger()

    # ==================== 发送群聊消息 ====================

    async def send_group_msg(self, group_id: int, message: str):
        """
        发送群文本消息
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param message: 消息内容
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群文本消息: {message[:50]}..., 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_at(self, group_id: int, user_id: int, message: str = ""):
        """
        发送群艾特消息
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param user_id: 被@的用户ID
        :param message: 附加消息内容（可选）
        """
        msg_list = [
            {
                "type": "at",
                "data": {
                    "qq": str(user_id)
                }
            }
        ]
        if message:
            msg_list.append({
                "type": "text",
                "data": {
                    "text": message
                }
            })

        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": msg_list
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群@消息: @{user_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_image(self, group_id: int, file: str, url: Optional[str] = None):
        """
        发送群图片
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param file: 图片文件路径或 base64
        :param url: 图片URL（可选）
        """
        image_data = {"file": file}
        if url:
            image_data["url"] = url

        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "image",
                        "data": image_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群图片, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_face(self, group_id: int, face_id: int):
        """
        发送群系统表情
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param face_id: 表情ID
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "face",
                        "data": {
                            "id": face_id
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群表情: {face_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_json(self, group_id: int, json_data: Dict[str, Any]):
        """
        发送群JSON消息
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param json_data: JSON数据
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "json",
                        "data": {
                            "data": json.dumps(json_data)
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群JSON消息, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_voice(self, group_id: int, file: str, url: Optional[str] = None):
        """
        发送群语音
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param file: 语音文件路径或 base64
        :param url: 语音URL（可选）
        """
        voice_data = {"file": file}
        if url:
            voice_data["url"] = url

        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "record",
                        "data": voice_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群语音, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_video(self, group_id: int, file: str, url: Optional[str] = None):
        """
        发送群视频
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param file: 视频文件路径或 base64
        :param url: 视频URL（可选）
        """
        video_data = {"file": file}
        if url:
            video_data["url"] = url

        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "video",
                        "data": video_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群视频, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_reply(self, group_id: int, message_id: int, message: str):
        """
        发送群回复消息
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param message_id: 要回复的消息ID
        :param message: 回复内容
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "reply",
                        "data": {
                            "id": message_id
                        }
                    },
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群回复消息: {message_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_music_card(self, group_id: int, music_type: str, id: str):
        """
        发送群聊音乐卡片
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param music_type: 音乐类型 (qq/163/xm/自定义)
        :param id: 音乐ID
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "music",
                        "data": {
                            "type": music_type,
                            "id": id
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群音乐卡片: {music_type}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_custom_music_card(self, group_id: int, url: str, audio: str, title: str,
                                           singer: str, image: Optional[str] = None):
        """
        发送群聊自定义音乐卡片
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param url: 跳转链接
        :param audio: 音频链接
        :param title: 标题
        :param singer: 歌手
        :param image: 封面图片（可选）
        """
        music_data = {
            "type": "custom",
            "url": url,
            "audio": audio,
            "title": title,
            "singer": singer
        }
        if image:
            music_data["image"] = image

        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "music",
                        "data": music_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群自定义音乐卡片: {title}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_dice(self, group_id: int):
        """
        发送群聊超级表情 - 骰子
        :param websocket: WebSocket 连接
        :param group_id: 群号
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "dice"
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群骰子, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_rps(self, group_id: int):
        """
        发送群聊超级表情 - 猜拳
        :param websocket: WebSocket 连接
        :param group_id: 群号
        """
        json_msg = {
            "action": "send_group_msg",
            "params": {
                "group_id": group_id,
                "message": [
                    {
                        "type": "rps"
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群猜拳, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_forward_msg(self, group_id: int, messages: List[Dict],
                                     source: str = "", news=None,
                                     prompt: str = "", summary: str = ""):
        """
        发送群合并转发消息
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param messages: 消息列表
        :param source: 标题信息
        :param news: 下方小标题信息（可以是字符串或字符串列表，兼容旧版本）
        :param prompt: 主页面信息
        :param summary: 摘要
        """
        params = {
            "group_id": group_id,
            "messages": messages
        }
        if source:
            params["source"] = source
        if news:
            # 兼容旧版本：如果 news 是字符串，转换为列表
            if isinstance(news, str):
                params["news"] = [{"text": news}]
            elif isinstance(news, list):
                # 如果已经是列表，检查元素格式
                if news and isinstance(news[0], str):
                    params["news"] = [{"text": n} for n in news]
                else:
                    params["news"] = news
        if prompt:
            params["prompt"] = prompt
        if summary:
            params["summary"] = summary

        json_msg = {
            "action": "send_group_forward_msg",
            "params": params
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群合并转发消息, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_file(self, group_id: int, file: str, name: str):
        """
        发送群文件
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param file: 文件路径或 base64
        :param name: 文件名
        """
        json_msg = {
            "action": "send_group_file",
            "params": {
                "group_id": group_id,
                "file": file,
                "name": name
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群文件: {name}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def forward_msg_to_group(self, group_id: int, message_id: int):
        """
        消息转发到群
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param message_id: 要转发的消息ID
        """
        json_msg = {
            "action": "forward_msg_to_group",
            "params": {
                "group_id": group_id,
                "message_id": message_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"转发消息到群: {message_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_poke(self, group_id: int, user_id: int):
        """
        发送群聊戳一戳
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param user_id: 被戳的用户ID
        """
        json_msg = {
            "action": "send_group_poke",
            "params": {
                "group_id": group_id,
                "user_id": user_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群戳一戳: {user_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_group_ai_voice(self, group_id: int, text: str, voice_id: Optional[int] = None):
        """
        发送群AI语音
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param text: 要转换的文本
        :param voice_id: 语音人物ID（可选）
        """
        params = {
            "group_id": group_id,
            "text": text
        }
        if voice_id:
            params["voice_id"] = voice_id

        json_msg = {
            "action": "send_group_ai_voice",
            "params": params
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送群AI语音: {text[:50]}..., 群号: {group_id}")
        await asyncio.sleep(0.1)


    # ==================== 发送私聊消息 ====================

    async def send_private_msg(self, user_id: int, message: str):
        """
        发送私聊文本消息
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param message: 消息内容
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊文本: {message[:50]}..., 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_image(self, user_id: int, file: str, url: Optional[str] = None):
        """
        发送私聊图片
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param file: 图片文件路径或 base64
        :param url: 图片URL（可选）
        """
        image_data = {"file": file}
        if url:
            image_data["url"] = url

        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "image",
                        "data": image_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊图片, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_face(self, user_id: int, face_id: int):
        """
        发送私聊系统表情
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param face_id: 表情ID
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "face",
                        "data": {
                            "id": face_id
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊表情: {face_id}, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_json(self, user_id: int, json_data: Dict[str, Any]):
        """
        发送私聊JSON消息
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param json_data: JSON数据
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "json",
                        "data": {
                            "data": json.dumps(json_data)
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊JSON消息, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_voice(self, user_id: int, file: str, url: Optional[str] = None):
        """
        发送私聊语音
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param file: 语音文件路径或 base64
        :param url: 语音URL（可选）
        """
        voice_data = {"file": file}
        if url:
            voice_data["url"] = url

        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "record",
                        "data": voice_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊语音, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_video(self, user_id: int, file: str, url: Optional[str] = None):
        """
        发送私聊视频
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param file: 视频文件路径或 base64
        :param url: 视频URL（可选）
        """
        video_data = {"file": file}
        if url:
            video_data["url"] = url

        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "video",
                        "data": video_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊视频, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_reply(self, user_id: int, message_id: int, message: str):
        """
        发送私聊回复消息
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param message_id: 要回复的消息ID
        :param message: 回复内容
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "reply",
                        "data": {
                            "id": message_id
                        }
                    },
                    {
                        "type": "text",
                        "data": {
                            "text": message
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊回复消息: {message_id}, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_music_card(self, user_id: int, music_type: str, id: str):
        """
        发送私聊音乐卡片
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param music_type: 音乐类型 (qq/163/xm/自定义)
        :param id: 音乐ID
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "music",
                        "data": {
                            "type": music_type,
                            "id": id
                        }
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊音乐卡片: {music_type}, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_custom_music_card(self, user_id: int, url: str, audio: str,
                                             title: str, singer: str, image: Optional[str] = None):
        """
        发送私聊自定义音乐卡片
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param url: 跳转链接
        :param audio: 音频链接
        :param title: 标题
        :param singer: 歌手
        :param image: 封面图片（可选）
        """
        music_data = {
            "type": "custom",
            "url": url,
            "audio": audio,
            "title": title,
            "singer": singer
        }
        if image:
            music_data["image"] = image

        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "music",
                        "data": music_data
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊自定义音乐卡片: {title}, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_dice(self, user_id: int):
        """
        发送私聊超级表情 - 骰子
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "dice"
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊骰子, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_rps(self, user_id: int):
        """
        发送私聊超级表情 - 猜拳
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        """
        json_msg = {
            "action": "send_private_msg",
            "params": {
                "user_id": user_id,
                "message": [
                    {
                        "type": "rps"
                    }
                ]
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊猜拳, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_forward_msg(self, user_id: int, messages: List[Dict]):
        """
        发送私聊合并转发消息
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param messages: 消息列表
        """
        json_msg = {
            "action": "send_private_forward_msg",
            "params": {
                "user_id": user_id,
                "messages": messages
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊合并转发消息, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def forward_msg_to_private(self, user_id: int, message_id: int):
        """
        消息转发到私聊
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param message_id: 要转发的消息ID
        """
        json_msg = {
            "action": "forward_msg_to_private",
            "params": {
                "user_id": user_id,
                "message_id": message_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"转发消息到私聊: {message_id}, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_file(self, user_id: int, file: str, name: str):
        """
        发送私聊文件
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param file: 文件路径或 base64
        :param name: 文件名
        """
        json_msg = {
            "action": "send_private_file",
            "params": {
                "user_id": user_id,
                "file": file,
                "name": name
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊文件: {name}, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def send_private_poke(self, user_id: int):
        """
        发送私聊戳一戳
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        """
        json_msg = {
            "action": "send_private_poke",
            "params": {
                "user_id": user_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送私聊戳一戳, 用户: {user_id}")
        await asyncio.sleep(0.1)


    # ==================== 其他消息操作 ====================

    async def send_poke(self, user_id: int, group_id: Optional[int] = None):
        """
        发送戳一戳
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param group_id: 群号（可选，如果是在群内）
        """
        params = {"user_id": user_id}
        if group_id:
            params["group_id"] = group_id

        json_msg = {
            "action": "send_poke",
            "params": params
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"发送戳一戳: {user_id}, 群号: {group_id or '私聊'}")
        await asyncio.sleep(0.1)


    async def delete_msg(self, message_id: int):
        """
        撤回消息
        :param websocket: WebSocket 连接
        :param message_id: 消息ID
        """
        json_msg = {
            "action": "delete_msg",
            "params": {
                "message_id": message_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"撤回消息: {message_id}")
        await asyncio.sleep(0.1)


    async def get_group_history_msg(self, group_id: int, message_seq: Optional[int] = None):
        """
        获取群历史消息
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :param message_seq: 消息序号（可选）
        :return: 返回的消息数据（需要通过响应处理）
        """
        params = {"group_id": group_id}
        if message_seq:
            params["message_seq"] = message_seq

        json_msg = {
            "action": "get_group_history_msg",
            "params": params
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取群历史消息, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def get_msg(self, message_id: int):
        """
        获取消息详情
        :param websocket: WebSocket 连接
        :param message_id: 消息ID
        :return: 返回的消息详情（需要通过响应处理）
        """
        json_msg = {
            "action": "get_msg",
            "params": {
                "message_id": message_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取消息详情: {message_id}")
        await asyncio.sleep(0.1)


    async def get_forward_msg(self, message_id: int):
        """
        获取合并转发消息
        :param websocket: WebSocket 连接
        :param message_id: 消息ID
        :return: 返回的合并转发消息（需要通过响应处理）
        """
        json_msg = {
            "action": "get_forward_msg",
            "params": {
                "message_id": message_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取合并转发消息: {message_id}")
        await asyncio.sleep(0.1)


    async def set_essence_msg(self, message_id: int):
        """
        贴表情（设置精华消息）
        :param websocket: WebSocket 连接
        :param message_id: 消息ID
        """
        json_msg = {
            "action": "set_essence_msg",
            "params": {
                "message_id": message_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"贴表情: {message_id}")
        await asyncio.sleep(0.1)


    async def get_friend_history_msg(self, user_id: int, message_seq: Optional[int] = None):
        """
        获取好友历史消息
        :param websocket: WebSocket 连接
        :param user_id: 用户ID
        :param message_seq: 消息序号（可选）
        :return: 返回的消息数据（需要通过响应处理）
        """
        params = {"user_id": user_id}
        if message_seq:
            params["message_seq"] = message_seq

        json_msg = {
            "action": "get_friend_history_msg",
            "params": params
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取好友历史消息, 用户: {user_id}")
        await asyncio.sleep(0.1)


    async def get_essence_msg_list(self, group_id: int):
        """
        获取贴表情详情（获取精华消息列表）
        :param websocket: WebSocket 连接
        :param group_id: 群号
        :return: 返回的精华消息列表（需要通过响应处理）
        """
        json_msg = {
            "action": "get_essence_msg_list",
            "params": {
                "group_id": group_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取贴表情详情, 群号: {group_id}")
        await asyncio.sleep(0.1)


    async def send_forward_msg(self, messages: List[Dict]):
        """
        发送合并转发消息
        :param websocket: WebSocket 连接
        :param messages: 消息列表
        """
        json_msg = {
            "action": "send_forward_msg",
            "params": {
                "messages": messages
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("发送合并转发消息")
        await asyncio.sleep(0.1)


    async def get_record(self, file: str, out_format: str = "mp3"):
        """
        获取语音消息详情
        :param websocket: WebSocket 连接
        :param file: 语音文件标识
        :param out_format: 输出格式（默认mp3）
        :return: 返回的语音文件信息（需要通过响应处理）
        """
        json_msg = {
            "action": "get_record",
            "params": {
                "file": file,
                "out_format": out_format
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取语音消息详情: {file}")
        await asyncio.sleep(0.1)


    async def get_image(self, file: str):
        """
        获取图片消息详情
        :param websocket: WebSocket 连接
        :param file: 图片文件标识
        :return: 返回的图片文件信息（需要通过响应处理）
        """
        json_msg = {
            "action": "get_image",
            "params": {
                "file": file
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取图片消息详情: {file}")
        await asyncio.sleep(0.1)

    # ==================== 群管理相关 ====================

    async def set_group_kick(self, group_id: int, user_id: int, reject_add_request: bool = False):
        """
        群组踢人
        :param group_id: 群号
        :param user_id: 要踢的成员QQ号
        :param reject_add_request: 拒绝此人的加群请求
        """
        json_msg = {
            "action": "set_group_kick",
            "params": {
                "group_id": group_id,
                "user_id": user_id,
                "reject_add_request": reject_add_request
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"群踢人: {user_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def set_group_ban(self, group_id: int, user_id: int, duration: int = 30 * 60):
        """
        群组单人禁言
        :param group_id: 群号
        :param user_id: 要禁言的成员QQ号
        :param duration: 禁言时长(单位秒), 0表示解除禁言
        """
        json_msg = {
            "action": "set_group_ban",
            "params": {
                "group_id": group_id,
                "user_id": user_id,
                "duration": duration
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"群禁言: {user_id}, 时长: {duration}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def set_group_whole_ban(self, group_id: int, enable: bool = True):
        """
        群组全员禁言
        :param group_id: 群号
        :param enable: 是否开启
        """
        json_msg = {
            "action": "set_group_whole_ban",
            "params": {
                "group_id": group_id,
                "enable": enable
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"群全员禁言: {enable}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def set_group_admin(self, group_id: int, user_id: int, enable: bool = True):
        """
        群组设置管理员
        :param group_id: 群号
        :param user_id: 要设置的成员QQ号
        :param enable: True为设置, False为取消
        """
        json_msg = {
            "action": "set_group_admin",
            "params": {
                "group_id": group_id,
                "user_id": user_id,
                "enable": enable
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"设置群管理员: {user_id}, 状态: {enable}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def set_group_card(self, group_id: int, user_id: int, card: str = ""):
        """
        设置群名片（群备注）
        :param group_id: 群号
        :param user_id: 要设置的成员QQ号
        :param card: 群名片内容, 不填或空字符串表示删除群名片
        """
        json_msg = {
            "action": "set_group_card",
            "params": {
                "group_id": group_id,
                "user_id": user_id,
                "card": card
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"设置群名片: {user_id}, 内容: {card}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def set_group_name(self, group_id: int, group_name: str):
        """
        设置群名
        :param group_id: 群号
        :param group_name: 新群名
        """
        json_msg = {
            "action": "set_group_name",
            "params": {
                "group_id": group_id,
                "group_name": group_name
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"设置群名: {group_name}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def set_group_leave(self, group_id: int, is_dismiss: bool = False):
        """
        退出群组
        :param group_id: 群号
        :param is_dismiss: 是否解散, 如果登录号是群主, 则仅在此项为True时能够解散
        """
        json_msg = {
            "action": "set_group_leave",
            "params": {
                "group_id": group_id,
                "is_dismiss": is_dismiss
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"退出群组: {group_id}, 解散: {is_dismiss}")
        await asyncio.sleep(0.1)

    async def set_group_special_title(self, group_id: int, user_id: int, special_title: str = "", duration: int = -1):
        """
        设置群组专属头衔
        :param group_id: 群号
        :param user_id: 要设置的成员QQ号
        :param special_title: 头衔, 空字符串表示删除
        :param duration: 有效时长(单位秒), -1表示永久
        """
        json_msg = {
            "action": "set_group_special_title",
            "params": {
                "group_id": group_id,
                "user_id": user_id,
                "special_title": special_title,
                "duration": duration
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"设置群头衔: {user_id}, 头衔: {special_title}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    # ==================== 信息查询相关 ====================

    async def get_login_info(self):
        """
        获取登录号信息
        :return: 登录号信息
        """
        json_msg = {
            "action": "get_login_info",
            "params": {}
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("获取登录号信息")
        await asyncio.sleep(0.1)

    async def get_friend_list(self):
        """
        获取好友列表
        :return: 好友列表
        """
        json_msg = {
            "action": "get_friend_list",
            "params": {}
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("获取好友列表")
        await asyncio.sleep(0.1)

    async def get_group_info(self, group_id: int, no_cache: bool = False):
        """
        获取群信息
        :param group_id: 群号
        :param no_cache: 是否不使用缓存
        :return: 群信息
        """
        json_msg = {
            "action": "get_group_info",
            "params": {
                "group_id": group_id,
                "no_cache": no_cache
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取群信息: {group_id}")
        await asyncio.sleep(0.1)

    async def get_group_list(self):
        """
        获取群列表
        :return: 群列表
        """
        json_msg = {
            "action": "get_group_list",
            "params": {}
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("获取群列表")
        await asyncio.sleep(0.1)

    async def get_group_member_info(self, group_id: int, user_id: int, no_cache: bool = False):
        """
        获取群成员信息
        :param group_id: 群号
        :param user_id: 成员QQ号
        :param no_cache: 是否不使用缓存
        :return: 群成员信息
        """
        json_msg = {
            "action": "get_group_member_info",
            "params": {
                "group_id": group_id,
                "user_id": user_id,
                "no_cache": no_cache
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取群成员信息: {user_id}, 群号: {group_id}")
        await asyncio.sleep(0.1)

    async def get_group_member_list(self, group_id: int):
        """
        获取群成员列表
        :param group_id: 群号
        :return: 群成员列表
        """
        json_msg = {
            "action": "get_group_member_list",
            "params": {
                "group_id": group_id
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"获取群成员列表: {group_id}")
        await asyncio.sleep(0.1)

    # ==================== 请求处理相关 ====================

    async def set_friend_add_request(self, flag: str, approve: bool = True, remark: str = ""):
        """
        处理加好友请求
        :param flag: 加好友请求的flag（从上报数据中获取）
        :param approve: 是否同意
        :param remark: 添加后的好友备注（仅在同意时有效）
        """
        json_msg = {
            "action": "set_friend_add_request",
            "params": {
                "flag": flag,
                "approve": approve,
                "remark": remark
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"处理加好友请求: {flag}, 同意: {approve}")
        await asyncio.sleep(0.1)

    async def set_group_add_request(self, flag: str, sub_type: str, approve: bool = True, reason: str = ""):
        """
        处理加群请求／邀请
        :param flag: 加群请求的flag（从上报数据中获取）
        :param sub_type: 子类型，add 或 invite_request（从上报数据中获取）
        :param approve: 是否同意
        :param reason: 拒绝理由（仅在拒绝时有效）
        """
        json_msg = {
            "action": "set_group_add_request",
            "params": {
                "flag": flag,
                "sub_type": sub_type,
                "approve": approve,
                "reason": reason
            }
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(f"处理加群请求: {flag}, 类型: {sub_type}, 同意: {approve}")
        await asyncio.sleep(0.1)

    # ==================== 系统操作相关 ====================

    async def get_version_info(self):
        """
        获取版本信息
        :return: 版本信息
        """
        json_msg = {
            "action": "get_version_info",
            "params": {}
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("获取版本信息")
        await asyncio.sleep(0.1)

    async def get_status(self):
        """
        获取运行状态
        :return: 运行状态
        """
        json_msg = {
            "action": "get_status",
            "params": {}
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("获取运行状态")
        await asyncio.sleep(0.1)

    async def clean_cache(self):
        """
        清理缓存
        """
        json_msg = {
            "action": "clean_cache",
            "params": {}
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info("清理缓存")
        await asyncio.sleep(0.1)

```


