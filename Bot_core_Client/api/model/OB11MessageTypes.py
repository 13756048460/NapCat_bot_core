"""
NapCat OneBot 11 消息段模型
包含所有 OneBot 11 协议支持的消息类型
"""
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from .OB11FileBaseData import OB11FileBaseData


@dataclass
class OB11MessageText:
    """OneBot 11 纯文本消息段"""
    type: str = field(default="text", metadata={"description": "消息类型"})
    data: Dict[str, str] = field(default_factory=dict, metadata={"description": "文本数据"})


@dataclass
class OB11MessageImage:
    """OneBot 11 图片消息段"""
    type: str = field(default="image", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "图片数据"})


@dataclass
class OB11MessageRecord:
    """OneBot 11 语音消息段"""
    type: str = field(default="record", metadata={"description": "消息类型"})
    data: OB11FileBaseData = field(default_factory=OB11FileBaseData, metadata={"description": "语音数据"})


@dataclass
class OB11MessageVideo:
    """OneBot 11 视频消息段"""
    type: str = field(default="video", metadata={"description": "消息类型"})
    data: OB11FileBaseData = field(default_factory=OB11FileBaseData, metadata={"description": "视频数据"})


@dataclass
class OB11MessageFile:
    """OneBot 11 文件消息段"""
    type: str = field(default="file", metadata={"description": "消息类型"})
    data: OB11FileBaseData = field(default_factory=OB11FileBaseData, metadata={"description": "文件数据"})


@dataclass
class OB11MessageFace:
    """OneBot 11 QQ 表情消息段"""
    type: str = field(default="face", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "表情数据"})


@dataclass
class OB11MessageAt:
    """OneBot 11 @消息段"""
    type: str = field(default="at", metadata={"description": "消息类型"})
    data: Dict[str, str] = field(default_factory=dict, metadata={"description": "@数据"})


@dataclass
class OB11MessageReply:
    """OneBot 11 回复消息段"""
    type: str = field(default="reply", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "回复数据"})


@dataclass
class OB11MessageNode:
    """OneBot 11 合并转发消息节点"""
    type: str = field(default="node", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "节点数据"})


@dataclass
class OB11MessageForward:
    """OneBot 11 合并转发消息段"""
    type: str = field(default="forward", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "转发数据"})


@dataclass
class OB11MessageLocation:
    """OneBot 11 位置消息段"""
    type: str = field(default="location", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "位置数据"})


@dataclass
class OB11MessageContact:
    """OneBot 11 推荐好友/群消息段"""
    type: str = field(default="contact", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "推荐数据"})


@dataclass
class OB11MessageJson:
    """OneBot 11 JSON 消息段"""
    type: str = field(default="json", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "JSON 数据"})


@dataclass
class OB11MessageXml:
    """OneBot 11 XML 消息段"""
    type: str = field(default="xml", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "XML 数据"})


@dataclass
class OB11MessageMarkdown:
    """OneBot 11 Markdown 消息段"""
    type: str = field(default="markdown", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "Markdown 数据"})


@dataclass
class OB11MessageMiniApp:
    """OneBot 11 小程序消息段"""
    type: str = field(default="miniapp", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "小程序数据"})


@dataclass
class OB11MessageMusic:
    """OneBot 11 音乐消息段"""
    type: str = field(default="music", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "音乐数据"})


@dataclass
class OB11MessagePoke:
    """OneBot 11 戳一戳消息段"""
    type: str = field(default="poke", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "戳一戳数据"})


@dataclass
class OB11MessageDice:
    """OneBot 11 骰子消息段"""
    type: str = field(default="dice", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "骰子数据"})


@dataclass
class OB11MessageRPS:
    """OneBot 11 猜拳消息段"""
    type: str = field(default="rps", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "猜拳数据"})


@dataclass
class OB11MessageOnlineFile:
    """OneBot 11 在线文件消息段"""
    type: str = field(default="onlinefile", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "在线文件数据"})


@dataclass
class OB11MessageFlashTransfer:
    """OneBot 11 闪传消息段"""
    type: str = field(default="flashtransfer", metadata={"description": "消息类型"})
    data: Dict[str, Any] = field(default_factory=dict, metadata={"description": "闪传数据"})


# 消息段联合类型
OB11MessageData = Union[
    OB11MessageText,
    OB11MessageImage,
    OB11MessageRecord,
    OB11MessageVideo,
    OB11MessageFile,
    OB11MessageFace,
    OB11MessageAt,
    OB11MessageReply,
    OB11MessageNode,
    OB11MessageForward,
    OB11MessageLocation,
    OB11MessageContact,
    OB11MessageJson,
    OB11MessageXml,
    OB11MessageMarkdown,
    OB11MessageMiniApp,
    OB11MessagePoke,
    OB11MessageDice,
    OB11MessageRPS,
    OB11MessageOnlineFile,
    OB11MessageFlashTransfer,
]

# 消息混合类型（可以是字符串、消息段数组或单个消息段）
OB11MessageMixType = Union[str, List[OB11MessageData], OB11MessageData]
