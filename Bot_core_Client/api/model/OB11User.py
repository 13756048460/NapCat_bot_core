"""
NapCat OneBot 11 用户信息模型
"""
from typing import Optional, Union
from dataclasses import dataclass, field


@dataclass
class OB11User:
    """OneBot 11 用户信息"""
    user_id: int = field(default=0, metadata={"description": "QQ 号"})
    nickname: str = field(default="", metadata={"description": "昵称"})
    remark: Optional[str] = field(default=None, metadata={"description": "备注"})
    sex: Optional[str] = field(default=None, metadata={"description": "性别"})
    level: Optional[int] = field(default=None, metadata={"description": "等级"})
    age: Optional[int] = field(default=None, metadata={"description": "年龄"})
    qid: Optional[str] = field(default=None, metadata={"description": "QID"})
    login_days: Optional[int] = field(default=None, metadata={"description": "登录天数"})
    category_name: Optional[str] = field(
        default=None, 
        metadata={"description": "分组名称", "alias": "categoryName"}
    )
    category_id: Optional[int] = field(
        default=None, 
        metadata={"description": "分组 ID", "alias": "categoryId"}
    )
    
    # 生日信息
    birthday_year: Optional[int] = field(default=None, metadata={"description": "出生年份"})
    birthday_month: Optional[int] = field(default=None, metadata={"description": "出生月份"})
    birthday_day: Optional[int] = field(default=None, metadata={"description": "出生日期"})
    
    # 联系方式
    phone_num: Optional[str] = field(default=None, metadata={"description": "手机号"})
    email: Optional[str] = field(default=None, metadata={"description": "邮箱"})


@dataclass
class OB11Sender:
    """OneBot 11 发送者信息"""
    user_id: Union[int, str] = field(default=0, metadata={"description": "发送者 QQ 号"})
    nickname: str = field(default="", metadata={"description": "发送者昵称"})
    card: Optional[str] = field(default=None, metadata={"description": "群名片"})
    role: Optional[str] = field(default=None, metadata={"description": "角色"})
    sex: Optional[str] = field(default=None, metadata={"description": "性别"})
    age: Optional[int] = field(default=None, metadata={"description": "年龄"})
    area: Optional[str] = field(default=None, metadata={"description": "地区"})
    level: Optional[str] = field(default=None, metadata={"description": "等级"})
    title: Optional[str] = field(default=None, metadata={"description": "头衔"})
