"""
NapCat OneBot 11 音乐消息段模型
包含 ID 音乐和自定义音乐两种类型
"""
from typing import Optional, Union
from dataclasses import dataclass, field


@dataclass
class OB11MessageIdMusic:
    """OneBot 11 ID 音乐消息段（通过音乐 ID 点歌）"""
    type: str = field(default="music", metadata={"description": "消息类型"})
    platform_type: str = field(default="qq", metadata={
        "description": "音乐平台类型",
        "enum": ["qq", "163", "kugou", "migu", "kuwo"]
    })
    music_id: Union[int, str] = field(default=0, metadata={"description": "音乐 ID"})


@dataclass
class OB11MessageCustomMusic:
    """OneBot 11 自定义音乐消息段（自定义链接分享音乐）"""
    type: str = field(default="music", metadata={"description": "消息类型"})
    platform_type: str = field(default="custom", metadata={
        "description": "音乐平台类型，固定为 custom",
        "enum": ["custom"]
    })
    url: str = field(default="", metadata={"description": "点击后跳转 URL"})
    audio: Optional[str] = field(default=None, metadata={"description": "音频 URL"})
    title: str = field(default="", metadata={"description": "音乐标题"})
    image: str = field(default="", metadata={"description": "封面图片 URL"})
    content: Optional[str] = field(default=None, metadata={"description": "音乐简介"})
