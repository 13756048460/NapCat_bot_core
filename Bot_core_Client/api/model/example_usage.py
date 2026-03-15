"""
NapCat OneBot 11 数据模型使用示例
"""

# 导入所有模型
from .OB11BaseResponse import OB11BaseResponse
from .OB11User import OB11User, OB11Sender
from .OB11Group import OB11Group, OB11GroupMember
from .OB11FileBaseData import OB11FileBaseData
from .OB11MessageTypes import (
    OB11MessageText,
    OB11MessageImage,
    OB11MessageAt,
    OB11MessageReply,
    OB11MessageData,
    OB11MessageMixType,
)
from .OB11Message import OB11Message
from .OB11Notify import OB11Notify, OB11PostSendMsg


__all__ = [
    # 基础响应
    "OB11BaseResponse",
    
    # 用户信息
    "OB11User",
    "OB11Sender",
    
    # 群信息
    "OB11Group",
    "OB11GroupMember",
    
    # 文件数据
    "OB11FileBaseData",
    
    # 消息段
    "OB11MessageText",
    "OB11MessageImage",
    "OB11MessageAt",
    "OB11MessageReply",
    
    # 消息类型
    "OB11MessageData",
    "OB11MessageMixType",
    
    # 完整消息
    "OB11Message",
    
    # 通知和请求
    "OB11Notify",
    "OB11PostSendMsg",
]
