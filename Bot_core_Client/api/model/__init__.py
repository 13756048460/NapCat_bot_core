"""
NapCat OneBot 11 数据模型包
基于 NapCat OpenAPI 文档生成的纯 Python 数据模型
"""

# 基础响应模型
from .OB11BaseResponse import OB11BaseResponse
from .EmptyData import EmptyData

# 用户信息模型
from .OB11User import OB11User, OB11Sender

# 群信息模型
from .OB11Group import OB11Group, OB11GroupMember

# 文件数据模型
from .OB11FileBaseData import OB11FileBaseData

# 音乐消息段模型
from .OB11MessageMusic import OB11MessageIdMusic, OB11MessageCustomMusic

# 商城表情消息段模型
from .OB11MessageMFace import OB11MessageMFace

# 文件消息基础模型
from .OB11MessageFileBase import OB11MessageFileBase

# 消息段模型
from .OB11MessageTypes import (
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
    OB11MessageData,
    OB11MessageMixType,
)

# 完整消息模型
from .OB11Message import OB11Message, OB11LatestMessage, OB11ActionMessage

# 通知和请求模型
from .OB11Notify import OB11Notify, OB11PostSendMsg

__all__ = [
    # 基础响应
    "OB11BaseResponse",
    "EmptyData",
    
    # 用户信息
    "OB11User",
    "OB11Sender",
    
    # 群信息
    "OB11Group",
    "OB11GroupMember",
    
    # 文件数据
    "OB11FileBaseData",
    
    # 音乐消息段
    "OB11MessageIdMusic",
    "OB11MessageCustomMusic",
    
    # 商城表情
    "OB11MessageMFace",
    
    # 文件消息基础
    "OB11MessageFileBase",
    
    # 消息段
    "OB11MessageText",
    "OB11MessageImage",
    "OB11MessageRecord",
    "OB11MessageVideo",
    "OB11MessageFile",
    "OB11MessageFace",
    "OB11MessageAt",
    "OB11MessageReply",
    "OB11MessageNode",
    "OB11MessageForward",
    "OB11MessageLocation",
    "OB11MessageContact",
    "OB11MessageJson",
    "OB11MessageXml",
    "OB11MessageMarkdown",
    "OB11MessageMiniApp",
    "OB11MessagePoke",
    "OB11MessageDice",
    "OB11MessageRPS",
    "OB11MessageOnlineFile",
    "OB11MessageFlashTransfer",
    
    # 消息类型
    "OB11MessageData",
    "OB11MessageMixType",
    
    # 完整消息
    "OB11Message",
    "OB11LatestMessage",
    "OB11ActionMessage",
    
    # 通知和请求
    "OB11Notify",
    "OB11PostSendMsg",
]
