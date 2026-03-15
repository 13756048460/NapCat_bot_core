"""
NapCat OneBot 11 群信息模型
"""
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class OB11Group:
    """OneBot 11 群信息"""
    group_id: int = field(default=0, metadata={"description": "群号"})
    group_name: str = field(default="", metadata={"description": "群名称"})
    group_remark: Optional[str] = field(default=None, metadata={"description": "群备注"})
    group_all_shut: int = field(default=0, metadata={"description": "是否全员禁言"})
    member_count: Optional[int] = field(default=None, metadata={"description": "成员人数"})
    max_member_count: Optional[int] = field(default=None, metadata={"description": "最大成员人数"})


@dataclass
class OB11GroupMember:
    """OneBot 11 群成员信息"""
    group_id: int = field(default=0, metadata={"description": "群号"})
    user_id: int = field(default=0, metadata={"description": "QQ 号"})
    nickname: str = field(default="", metadata={"description": "昵称"})
    card: Optional[str] = field(default=None, metadata={"description": "名片"})
    sex: Optional[str] = field(default=None, metadata={"description": "性别"})
    age: Optional[int] = field(default=None, metadata={"description": "年龄"})
    join_time: Optional[int] = field(default=None, metadata={"description": "入群时间戳"})
    last_sent_time: Optional[int] = field(default=None, metadata={"description": "最后发言时间戳"})
    level: Optional[str] = field(default=None, metadata={"description": "等级"})
    qq_level: Optional[int] = field(default=None, metadata={"description": "QQ 等级"})
    role: Optional[str] = field(default=None, metadata={"description": "角色 (owner/admin/member)"})
    title: Optional[str] = field(default=None, metadata={"description": "头衔"})
    area: Optional[str] = field(default=None, metadata={"description": "地区"})
    unfriendly: Optional[bool] = field(default=None, metadata={"description": "是否不良记录"})
    title_expire_time: Optional[int] = field(default=None, metadata={"description": "头衔过期时间"})
    card_changeable: Optional[bool] = field(default=None, metadata={"description": "是否允许修改名片"})
    shut_up_timestamp: Optional[int] = field(default=None, metadata={"description": "禁言截止时间戳"})
    is_robot: Optional[bool] = field(default=None, metadata={"description": "是否为机器人"})
    qage: Optional[int] = field(default=None, metadata={"description": "Q 龄"})
