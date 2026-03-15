"""
NapCat OneBot 11 文件消息基础模型
"""
from dataclasses import dataclass, field

from .OB11FileBaseData import OB11FileBaseData


@dataclass
class OB11MessageFileBase:
    """OneBot 11 文件消息基础接口"""
    data: OB11FileBaseData = field(default_factory=OB11FileBaseData, metadata={"description": "文件数据"})
