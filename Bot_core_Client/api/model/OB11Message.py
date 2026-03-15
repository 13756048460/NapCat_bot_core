"""
NapCat OneBot 11 完整消息和消息相关模型
"""
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from .OB11User import OB11Sender
from .OB11MessageTypes import (
    OB11MessageData,
    OB11MessageMixType,
)


@dataclass
class OB11Message:
    """OneBot 11 完整消息对象"""
    time: int = field(default=0, metadata={"description": "消息时间戳"})
    message_id: int = field(default=0, metadata={"description": "消息 ID"})
    message_seq: int = field(default=0, metadata={"description": "消息序列号"})
    real_id: int = field(default=0, metadata={"description": "真实 ID"})
    user_id: Union[int, str] = field(default=0, metadata={"description": "发送者 QQ 号"})
    message_type: str = field(default="", metadata={"description": "消息类型"})
    sender: OB11Sender = field(default_factory=OB11Sender, metadata={"description": "发送者信息"})
    message: Union[str, List[OB11MessageData]] = field(
        default_factory=list, 
        metadata={"description": "消息内容"}
    )
    message_format: str = field(default="", metadata={"description": "消息格式"})
    raw_message: str = field(default="", metadata={"description": "原始消息"})
    font: int = field(default=0, metadata={"description": "字体"})
    
    # 可选字段
    post_type: Optional[str] = field(default=None, metadata={"description": "上报类型"})
    self_id: Optional[int] = field(default=None, metadata={"description": "机器人 QQ 号"})
    group_id: Optional[Union[int, str]] = field(default=None, metadata={"description": "群号"})
    group_name: Optional[str] = field(default=None, metadata={"description": "群名称"})
    sub_type: Optional[str] = field(default=None, metadata={"description": "消息子类型"})
    target_id: Optional[int] = field(default=None, metadata={"description": "目标 ID"})
    temp_source: Optional[int] = field(default=None, metadata={"description": "临时会话来源"})
    message_sent_type: Optional[str] = field(default=None, metadata={"description": "消息发送类型"})
    real_seq: Optional[str] = field(default=None, metadata={"description": "真实序列号"})
    raw: Optional[Dict[str, Any]] = field(default=None, metadata={"description": "原始消息对象"})
    emoji_likes_list: Optional[List[Dict[str, str]]] = field(
        default=None, 
        metadata={"description": "表情点赞列表"}
    )


@dataclass
class OB11LatestMessage:
    """OneBot 11 最后一条消息"""
    self_id: int = field(default=0, metadata={"description": "发送者 QQ 号"})
    user_id: int = field(default=0, metadata={"description": "接收者 QQ 号"})
    time: int = field(default=0, metadata={"description": "时间戳"})
    real_seq: str = field(default="", metadata={"description": "消息序号"})
    message_type: str = field(default="", metadata={"description": "消息类型"})
    sender: Dict[str, Any] = field(default_factory=dict, metadata={"description": "发送者信息"})
    raw_message: str = field(default="", metadata={"description": "原始消息"})
    font: int = field(default=0, metadata={"description": "字体大小"})
    sub_type: str = field(default="", metadata={"description": "子类型"})
    message: Dict[str, Any] = field(default_factory=dict, metadata={"description": "消息内容"})
    message_format: str = field(default="", metadata={"description": "消息格式"})
    post_type: str = field(default="", metadata={"description": "发布类型"})
    group_id: int = field(default=0, metadata={"description": "群号"})
    group_name: str = field(default="", metadata={"description": "群名称"})


@dataclass
class OB11ActionMessage:
    """OneBot 11 消息信息"""
    self_id: int = field(default=0, metadata={"description": "发送者 QQ 号"})
    user_id: int = field(default=0, metadata={"description": "接收者 QQ 号"})
    time: int = field(default=0, metadata={"description": "时间戳"})
    real_seq: str = field(default="", metadata={"description": "消息序号"})
    message_type: str = field(default="", metadata={"description": "消息类型"})
    sender: Dict[str, Any] = field(default_factory=dict, metadata={"description": "发送者信息"})
    raw_message: str = field(default="", metadata={"description": "原始消息"})
    font: int = field(default=0, metadata={"description": "字体大小"})
    sub_type: str = field(default="", metadata={"description": "子类型"})
    message: Dict[str, Any] = field(default_factory=dict, metadata={"description": "消息内容"})
    message_format: str = field(default="", metadata={"description": "消息格式"})
    post_type: str = field(default="", metadata={"description": "发布类型"})
    group_id: int = field(default=0, metadata={"description": "群号"})
    group_name: str = field(default="", metadata={"description": "群名称"})
    message_id: int = field(default=0, metadata={"description": "消息 ID"})
    message_seq: int = field(default=0, metadata={"description": "消息序列号"})
    emoji_likes_list: Optional[List[Dict[str, str]]] = field(
        default=None, 
        metadata={"description": "表情点赞列表"}
    )
