"""
NapCat OneBot 11 文件数据模型
"""
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class OB11FileBaseData:
    """OneBot 11 文件基础数据"""
    file: str = field(default="", metadata={"description": "文件路径/URL/file:///"})
    path: Optional[str] = field(default=None, metadata={"description": "文件路径"})
    url: Optional[str] = field(default=None, metadata={"description": "文件URL"})
    name: Optional[str] = field(default=None, metadata={"description": "文件名"})
    thumb: Optional[str] = field(default=None, metadata={"description": "缩略图"})
