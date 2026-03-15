"""
NapCat OneBot 11 基础响应模型
"""
from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class OB11BaseResponse:
    """OneBot 11 基础响应模型"""
    status: str = field(default="", metadata={"description": "状态 (ok/failed)"})
    retcode: int = field(default=0, metadata={"description": "返回码"})
    data: Optional[Any] = field(default=None, metadata={"description": "业务数据（具体结构由各接口定义）"})
    message: Optional[str] = field(default="", metadata={"description": "消息"})
    wording: Optional[str] = field(default="", metadata={"description": "提示"})
    stream: Optional[str] = field(
        default="normal-action", 
        metadata={"description": "流式响应"}
    )
