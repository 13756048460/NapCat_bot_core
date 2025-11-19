"""
NapCat 消息相关 API
参考文档: https://napcat.apifox.cn/
"""
import json
import asyncio
from typing import Optional, List, Dict, Any
from logs import Logger


# ==================== 发送群聊消息 ====================

async def send_group_msg(websocket, group_id: int, message: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群文本消息: {message[:50]}..., 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_at(websocket, group_id: int, user_id: int, message: str = ""):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群@消息: @{user_id}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_image(websocket, group_id: int, file: str, url: Optional[str] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群图片, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_face(websocket, group_id: int, face_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群表情: {face_id}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_json(websocket, group_id: int, json_data: Dict[str, Any]):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群JSON消息, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_voice(websocket, group_id: int, file: str, url: Optional[str] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群语音, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_video(websocket, group_id: int, file: str, url: Optional[str] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群视频, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_reply(websocket, group_id: int, message_id: int, message: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群回复消息: {message_id}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_music_card(websocket, group_id: int, music_type: str, id: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群音乐卡片: {music_type}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_custom_music_card(websocket, group_id: int, url: str, audio: str, title: str,
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群自定义音乐卡片: {title}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_dice(websocket, group_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群骰子, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_rps(websocket, group_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群猜拳, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_forward_msg(websocket, group_id: int, messages: List[Dict],
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群合并转发消息, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_file(websocket, group_id: int, file: str, name: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群文件: {name}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def forward_msg_to_group(websocket, group_id: int, message_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"转发消息到群: {message_id}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_poke(websocket, group_id: int, user_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群戳一戳: {user_id}, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_group_ai_voice(websocket, group_id: int, text: str, voice_id: Optional[int] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送群AI语音: {text[:50]}..., 群号: {group_id}")
    await asyncio.sleep(0.1)


# ==================== 发送私聊消息 ====================

async def send_private_msg(websocket, user_id: int, message: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊文本: {message[:50]}..., 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_image(websocket, user_id: int, file: str, url: Optional[str] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊图片, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_face(websocket, user_id: int, face_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊表情: {face_id}, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_json(websocket, user_id: int, json_data: Dict[str, Any]):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊JSON消息, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_voice(websocket, user_id: int, file: str, url: Optional[str] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊语音, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_video(websocket, user_id: int, file: str, url: Optional[str] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊视频, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_reply(websocket, user_id: int, message_id: int, message: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊回复消息: {message_id}, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_music_card(websocket, user_id: int, music_type: str, id: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊音乐卡片: {music_type}, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_custom_music_card(websocket, user_id: int, url: str, audio: str,
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊自定义音乐卡片: {title}, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_dice(websocket, user_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊骰子, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_rps(websocket, user_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊猜拳, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_forward_msg(websocket, user_id: int, messages: List[Dict]):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊合并转发消息, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def forward_msg_to_private(websocket, user_id: int, message_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"转发消息到私聊: {message_id}, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_file(websocket, user_id: int, file: str, name: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊文件: {name}, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def send_private_poke(websocket, user_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送私聊戳一戳, 用户: {user_id}")
    await asyncio.sleep(0.1)


# ==================== 其他消息操作 ====================

async def send_poke(websocket, user_id: int, group_id: Optional[int] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"发送戳一戳: {user_id}, 群号: {group_id or '私聊'}")
    await asyncio.sleep(0.1)


async def delete_msg(websocket, message_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"撤回消息: {message_id}")
    await asyncio.sleep(0.1)


async def get_group_history_msg(websocket, group_id: int, message_seq: Optional[int] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取群历史消息, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def get_msg(websocket, message_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取消息详情: {message_id}")
    await asyncio.sleep(0.1)


async def get_forward_msg(websocket, message_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取合并转发消息: {message_id}")
    await asyncio.sleep(0.1)


async def set_essence_msg(websocket, message_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"贴表情: {message_id}")
    await asyncio.sleep(0.1)


async def get_friend_history_msg(websocket, user_id: int, message_seq: Optional[int] = None):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取好友历史消息, 用户: {user_id}")
    await asyncio.sleep(0.1)


async def get_essence_msg_list(websocket, group_id: int):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取贴表情详情, 群号: {group_id}")
    await asyncio.sleep(0.1)


async def send_forward_msg(websocket, messages: List[Dict]):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info("发送合并转发消息")
    await asyncio.sleep(0.1)


async def get_record(websocket, file: str, out_format: str = "mp3"):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取语音消息详情: {file}")
    await asyncio.sleep(0.1)


async def get_image(websocket, file: str):
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
    await websocket.send(json.dumps(json_msg))
    Logger().info(f"获取图片消息详情: {file}")
    await asyncio.sleep(0.1)


# ==================== 兼容旧版本 ====================

# 保留旧版本的函数名以保持兼容性
async def send_group_msg_at(websocket, group_id: int, user_id: int, message: str = ""):
    """
    发送群消息at（兼容旧版本）
    :param websocket: WebSocket 连接
    :param group_id: 群号
    :param user_id: 被@的用户ID
    :param message: 附加消息内容（可选）
    """
    await send_group_at(websocket, group_id, user_id, message)
