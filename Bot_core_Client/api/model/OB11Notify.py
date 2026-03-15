"""
NapCat OneBot 11 通知和请求模型
"""
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from .OB11MessageTypes import OB11MessageData


@dataclass
class OB11Notify:
    """OneBot 11 通知信息"""
    request_id: int = field(default=0, metadata={"description": "请求 ID"})
    invitor_uin: int = field(default=0, metadata={"description": "邀请者 QQ"})
    invitor_nick: str = field(default="", metadata={"description": "邀请者昵称"})
    group_id: int = field(default=0, metadata={"description": "群号"})
    group_name: str = field(default="", metadata={"description": "群名称"})
    message: str = field(default="", metadata={"description": "附言"})
    checked: bool = field(default=False, metadata={"description": "是否已处理"})
    actor: int = field(default=0, metadata={"description": "操作者 QQ"})
    requester_nick: str = field(default="", metadata={"description": "申请者昵称"})


@dataclass
class OB11PostSendMsg:
    """OneBot 11 发送消息请求"""
    message: Union[str, List[OB11MessageData], OB11MessageData] = field(
        default_factory=list, 
        metadata={"description": "消息内容"}
    )
    message_type: Optional[str] = field(default=None, metadata={"description": "消息类型"})
    user_id: Optional[str] = field(default=None, metadata={"description": "用户 QQ 号"})
    group_id: Optional[str] = field(default=None, metadata={"description": "群号"})
    auto_escape: Optional[Union[bool, str]] = field(default=None, metadata={"description": "是否作为纯文本发送"})
    source: Optional[str] = field(default=None, metadata={"description": "消息来源"})
    news: Optional[List[Dict[str, str]]] = field(default=None, metadata={"description": "新闻列表"})
    summary: Optional[str] = field(default=None, metadata={"description": "摘要"})
    prompt: Optional[str] = field(default=None, metadata={"description": "提示"})
    time: Optional[str] = field(default=None, metadata={"description": "时间"})
