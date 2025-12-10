"""
NapCat 消息相关 API - 核心同步功能模块
参考文档: https://napcat.apifox.cn/
"""
import json
import asyncio
from typing import Optional, List, Dict, Any
from ..logs import Logger


class Message:
    """消息对象包装类 - 提供便捷的属性访问"""
    def __init__(self, msg_dict: dict):
        self._msg = msg_dict
    
    @property
    def raw(self) -> str:
        """获取原始消息内容"""
        return self._msg.get("raw_message", "")
    
    @property
    def user_id(self) -> Optional[int]:
        """获取用户ID"""
        return self._msg.get("user_id")
    
    @property
    def message_id(self) -> Optional[int]:
        """获取消息ID"""
        return self._msg.get("message_id")
    
    @property
    def group_id(self) -> Optional[int]:
        """获取群ID（仅群聊消息）"""
        return self._msg.get("group_id")
    
    @property
    def message_type(self) -> str:
        """获取消息类型（group/private）"""
        return self._msg.get("message_type", "")
    
    @property
    def js(self) -> dict:
        """获取原始字典对象"""
        return self._msg
    
    @property
    def dict(self) -> dict:
        """获取原始字典对象（兼容旧方法）"""
        return self._msg
    
    def get(self, key: str, default=None):
        """获取消息字段"""
        return self._msg.get(key, default)


class MessageBuilder:
    """消息构建器 - 支持链式调用"""
    def __init__(self, websocket, target_type: str, target_id: int):
        self.websocket = websocket
        self.target_type = target_type  # 'group' or 'private'
        self.target_id = target_id
        self.message_chain: List[Dict[str, Any]] = []
    
    def text(self, content: str) -> 'MessageBuilder':
        """添加文本消息"""
        self.message_chain.append({
            "type": "text",
            "data": {"text": content}
        })
        return self
    
    def at(self, qq: int) -> 'MessageBuilder':
        """添加@某人 (仅群聊)"""
        self.message_chain.append({
            "type": "at",
            "data": {"qq": str(qq)}
        })
        return self
    
    def image(self, file: str, url: Optional[str] = None) -> 'MessageBuilder':
        """添加图片"""
        image_data = {"file": file}
        if url:
            image_data["url"] = url
        self.message_chain.append({
            "type": "image",
            "data": image_data
        })
        return self
    
    def face(self, face_id: int) -> 'MessageBuilder':
        """添加系统表情"""
        self.message_chain.append({
            "type": "face",
            "data": {"id": face_id}
        })
        return self
    
    def reply(self, message_id: int) -> 'MessageBuilder':
        """添加回复"""
        self.message_chain.append({
            "type": "reply",
            "data": {"id": message_id}
        })
        return self
    
    def voice(self, file: str, url: Optional[str] = None) -> 'MessageBuilder':
        """添加语音"""
        voice_data = {"file": file}
        if url:
            voice_data["url"] = url
        self.message_chain.append({
            "type": "record",
            "data": voice_data
        })
        return self
    
    def video(self, file: str, url: Optional[str] = None) -> 'MessageBuilder':
        """添加视频"""
        video_data = {"file": file}
        if url:
            video_data["url"] = url
        self.message_chain.append({
            "type": "video",
            "data": video_data
        })
        return self
    
    def json_msg(self, json_data: Dict[str, Any]) -> 'MessageBuilder':
        """添加JSON消息"""
        self.message_chain.append({
            "type": "json",
            "data": {"data": json.dumps(json_data)}
        })
        return self
    
    def music(self, music_type: str, music_id: str) -> 'MessageBuilder':
        """添加音乐卡片"""
        self.message_chain.append({
            "type": "music",
            "data": {
                "type": music_type,
                "id": music_id
            }
        })
        return self
    
    def custom_music(self, url: str, audio: str, title: str, 
                    singer: str, image: Optional[str] = None) -> 'MessageBuilder':
        """添加自定义音乐卡片"""
        music_data = {
            "type": "custom",
            "url": url,
            "audio": audio,
            "title": title,
            "singer": singer
        }
        if image:
            music_data["image"] = image
        self.message_chain.append({
            "type": "music",
            "data": music_data
        })
        return self
    
    def dice(self) -> 'MessageBuilder':
        """添加骰子"""
        self.message_chain.append({"type": "dice"})
        return self
    
    def rps(self) -> 'MessageBuilder':
        """添加猜拳"""
        self.message_chain.append({"type": "rps"})
        return self
    
    async def send(self) -> None:
        """发送消息"""
        if self.target_type == 'group':
            action = "send_group_msg"
            params = {
                "group_id": self.target_id,
                "message": self.message_chain
            }
            log_msg = f"发送群消息, 群号: {self.target_id}"
        else:  # private
            action = "send_private_msg"
            params = {
                "user_id": self.target_id,
                "message": self.message_chain
            }
            log_msg = f"发送私聊消息, 用户: {self.target_id}"
        
        json_msg = {
            "action": action,
            "params": params
        }
        await self.websocket.send(json.dumps(json_msg))
        Logger().info(log_msg)
        await asyncio.sleep(0.1)


class MessageSender:
    """消息发送器 - 用于选择发送目标"""
    def __init__(self, websocket):
        self.websocket = websocket
    
    def all(self, msg) -> MessageBuilder:
        """
        自动识别消息类型（群聊或私聊）
        :param msg: 消息对象(Message/dict)
        """
        if isinstance(msg, Message):
            msg_dict = msg.js
        else:
            msg_dict = msg
        
        message_type = msg_dict.get("message_type")
        if message_type == "group":
            group_id = msg_dict.get("group_id")
            return MessageBuilder(self.websocket, 'group', group_id)
        elif message_type == "private":
            user_id = msg_dict.get("user_id")
            return MessageBuilder(self.websocket, 'private', user_id)
        else:
            raise ValueError(f"不支持的消息类型: {message_type}")
    
    def group(self, group_id_or_msg) -> MessageBuilder:
        """
        发送群消息
        :param group_id_or_msg: 群号(int) 或 消息对象(Message/dict)
        """
        if isinstance(group_id_or_msg, Message):
            msg_dict = group_id_or_msg.js
            if msg_dict.get("message_type") != "group":
                raise ValueError("消息类型不是群消息")
            group_id = msg_dict.get("group_id")
            return MessageBuilder(self.websocket, 'group', group_id)
        elif isinstance(group_id_or_msg, dict):
            # 如果传入的是消息字典
            msg = group_id_or_msg
            if msg.get("message_type") != "group":
                raise ValueError("消息类型不是群消息")
            group_id = msg.get("group_id")
            return MessageBuilder(self.websocket, 'group', group_id)
        else:
            # 如果传入的是群号
            return MessageBuilder(self.websocket, 'group', group_id_or_msg)
    
    def private(self, user_id_or_msg) -> MessageBuilder:
        """
        发送私聊消息
        :param user_id_or_msg: 用户ID(int) 或 消息对象(Message/dict)
        """
        if isinstance(user_id_or_msg, Message):
            msg_dict = user_id_or_msg.js
            if msg_dict.get("message_type") != "private":
                raise ValueError("消息类型不是私聊消息")
            user_id = msg_dict.get("user_id")
            return MessageBuilder(self.websocket, 'private', user_id)
        elif isinstance(user_id_or_msg, dict):
            # 如果传入的是消息字典
            msg = user_id_or_msg
            if msg.get("message_type") != "private":
                raise ValueError("消息类型不是私聊消息")
            user_id = msg.get("user_id")
            return MessageBuilder(self.websocket, 'private', user_id)
        else:
            # 如果传入的是用户ID
            return MessageBuilder(self.websocket, 'private', user_id_or_msg)


class BotClient:
    """Bot客户端基础类 - 仅包含核心同步功能"""
    def __init__(self, websocket):
        self.websocket = websocket
        self.logger = Logger()
    
    def send_msg(self) -> 'MessageSender':
        """
        创建消息发送器 - 链式调用入口
        :param msg: 可选，消息对象(Message/dict)，如果传入则自动识别类型
        """
        return MessageSender(self.websocket)
