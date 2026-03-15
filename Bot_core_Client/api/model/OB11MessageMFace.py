"""
NapCat OneBot 11 商城表情消息段模型
"""
from dataclasses import dataclass, field


@dataclass
class OB11MessageMFace:
    """OneBot 11 商城表情消息段"""
    type: str = field(default="mface", metadata={"description": "消息类型"})
    emoji_package_id: int = field(default=0, metadata={"description": "表情包 ID"})
    emoji_id: str = field(default="", metadata={"description": "表情 ID"})
    key: str = field(default="", metadata={"description": "表情 key"})
    summary: str = field(default="", metadata={"description": "表情摘要"})
