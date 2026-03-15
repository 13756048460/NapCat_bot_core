import colorlog
import logging
import sys
from datetime import datetime
from typing import Optional, Any, Dict, Union
from dataclasses import asdict, is_dataclass

# 添加 SUCCESS 日志级别
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, 'SUCCESS')


class Logger:
    """
    NapCat 机器人日志记录器
    支持 OneBot 11 协议的各种事件日志
    """
    
    def __init__(self, log_name='root', level='INFO'):
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.logger = colorlog.getLogger(log_name)
        
        if not self.logger.handlers:
            handler = colorlog.StreamHandler(sys.stdout)
            
            formatter = colorlog.ColoredFormatter(
                '%(log_color)s[%(asctime)s] [%(levelname)s] %(reset)s%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'SUCCESS': 'bold_green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                }
            )
            
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.level)
    
    def _log(self, level: int, message: str):
        """内部日志记录方法"""
        self.logger.log(level, message)
    
    def debug(self, message: str):
        """调试日志"""
        self._log(logging.DEBUG, message)
    
    def info(self, message: str):
        """信息日志"""
        self._log(logging.INFO, message)
    
    def success(self, message: str):
        """成功日志"""
        self._log(SUCCESS_LEVEL, message)
    
    def warning(self, message: str):
        """警告日志"""
        self._log(logging.WARNING, message)
    
    def error(self, message: str):
        """错误日志"""
        self._log(logging.ERROR, message)
    
    def critical(self, message: str):
        """严重错误日志"""
        self._log(logging.CRITICAL, message)
    
    def log_meta_event(self, event_data: Union[Dict[str, Any], 'OB11Notify']):
        """
        记录元事件日志
        
        Args:
            event_data: OneBot 11 元事件数据（字典或 OB11Notify 模型）
        """
        # 如果是模型对象，转换为字典
        if hasattr(event_data, '__dataclass_fields__'):
            event_dict = asdict(event_data)
        else:
            event_dict = event_data
        
        meta_event_type = event_dict.get('meta_event_type', '')
        sub_type = event_dict.get('sub_type', '')
        self_id = event_dict.get('self_id', 0)
        
        log_msg = f"[元事件] {meta_event_type}/{sub_type} | Bot:{self_id}"
        
        if sub_type == 'connect':
            self.success(log_msg)
        elif sub_type == 'disconnect':
            self.warning(log_msg)
        else:
            self.info(log_msg)
    
    def log_notice_event(self, event_data: Union[Dict[str, Any], 'OB11Notify']):
        """
        记录通知事件日志
        
        Args:
            event_data: OneBot 11 通知事件数据（字典或 OB11Notify 模型）
        """
        # 如果是模型对象，转换为字典
        if hasattr(event_data, '__dataclass_fields__'):
            event_dict = asdict(event_data)
        else:
            event_dict = event_data
        
        notice_type = event_dict.get('notice_type', '')
        user_id = event_dict.get('user_id', 0)
        group_id = event_dict.get('group_id', 0)
        self_id = event_dict.get('self_id', 0)
        
        log_msg = f"[通知事件] {notice_type}"
        
        if group_id:
            log_msg += f" | 群:{group_id}"
        if user_id:
            log_msg += f" | 用户:{user_id}"
        
        log_msg += f" | Bot:{self_id}"
        self.info(log_msg)
    
    def log_request_event(self, event_data: Union[Dict[str, Any], 'OB11Notify']):
        """
        记录请求事件日志
        
        Args:
            event_data: OneBot 11 请求事件数据（字典或 OB11Notify 模型）
        """
        # 如果是模型对象，转换为字典
        if hasattr(event_data, '__dataclass_fields__'):
            event_dict = asdict(event_data)
        else:
            event_dict = event_data
        
        request_type = event_dict.get('request_type', '')
        user_id = event_dict.get('user_id', 0)
        self_id = event_dict.get('self_id', 0)
        
        log_msg = f"[请求事件] {request_type} | 申请人:{user_id} | Bot:{self_id}"
        self.info(log_msg)
    
    def log_message(self, event_data: Union[Dict[str, Any], 'OB11Message']):
        """
        记录消息日志
        
        Args:
            event_data: OneBot 11 消息事件数据（字典或 OB11Message 模型）
        """
        # 如果是模型对象，转换为字典
        if hasattr(event_data, '__dataclass_fields__'):
            event_dict = asdict(event_data)
        else:
            event_dict = event_data
        
        message_type = event_dict.get('message_type', '')
        user_id = event_dict.get('user_id', 0)
        group_id = event_dict.get('group_id', 0)
        group_name = event_dict.get('group_name', '')
        sender = event_dict.get('sender', {})
        nickname = sender.get('nickname', '') if sender else ''
        card = sender.get('card', '') if sender else ''
        raw_message = event_dict.get('raw_message', '')
        message_seq = event_dict.get('message_seq', 0)
        
        # 构建位置信息
        if message_type == 'private':
            location = f"私聊 [{nickname}/{user_id}]"
        elif message_type == 'group':
            display_name = card if card else nickname
            location = f"群聊 [{group_name}/{group_id}] - {display_name}/{user_id}"
        else:
            location = f"{message_type} [{user_id}]"
        
        log_msg = f"[消息] {location} | 序号:{message_seq} | 内容：{raw_message}"
        self.info(log_msg)
    
    def log_plugin_error(self, plugin_name: str, error: Exception, context: str = ""):
        """
        记录插件错误日志
        
        Args:
            plugin_name: 插件名称
            error: 异常对象
            context: 错误发生的上下文
        """
        import traceback
        
        context_info = f" ({context})" if context else ""
        log_msg = f"[插件错误] {plugin_name}{context_info}\n"
        log_msg += f"\t异常类型：{type(error).__name__}\n"
        log_msg += f"\t异常信息：{str(error)}\n"
        log_msg += f"\t堆栈跟踪:\n{traceback.format_exc()}"
        
        self.error(log_msg)
    
    def log_api_response(self, response: Any, action: str = "API"):
        """
        记录 API 响应日志
        
        Args:
            response: API 响应对象（可以是 OB11BaseResponse、dataclass 或 dict）
            action: 操作描述
        """
        try:
            # 延迟导入，避免循环依赖
            from Bot_core_Client.api.model.OB11BaseResponse import OB11BaseResponse
            
            # 如果是 OB11BaseResponse 实例，直接使用
            if isinstance(response, OB11BaseResponse):
                status = response.status
                retcode = response.retcode
                wording = response.wording
                message = response.message
                stream = response.stream
            # 如果是其他 dataclass，转换为字典处理
            elif hasattr(response, '__dataclass_fields__'):
                response_dict = asdict(response)
                status = response_dict.get('status', '')
                retcode = response_dict.get('retcode', -1)
                wording = response_dict.get('wording', '')
                message = response_dict.get('message', '')
                stream = response_dict.get('stream', 'normal-action')
            # 如果是字典
            elif isinstance(response, dict):
                status = response.get('status', '')
                retcode = response.get('retcode', -1)
                wording = response.get('wording', '')
                message = response.get('message', '')
                stream = response.get('stream', 'normal-action')
            else:
                self.debug(f"[API] {action} | 未知响应类型：{type(response)}")
                return
            
            # 根据返回码判断日志级别
            if retcode == 0 and status == 'ok':
                # 成功响应
                log_msg = f"[API] {action} | 状态:OK | 返回码:{retcode} | 流:{stream}"
                if wording:
                    log_msg += f" | {wording}"
                self.success(log_msg)
            elif retcode in [1400, 1401, 1404]:
                # 常见错误码
                error_map = {
                    1400: "请求参数错误",
                    1401: "权限不足",
                    1404: "资源不存在"
                }
                error_desc = error_map.get(retcode, "业务逻辑错误")
                log_msg = f"[API] {action} | 状态:FAILED | 返回码:{retcode} | {error_desc}"
                if message:
                    log_msg += f" | {message}"
                if wording:
                    log_msg += f" | {wording}"
                self.error(log_msg)
            else:
                # 其他错误
                log_msg = f"[API] {action} | 状态:FAILED | 返回码:{retcode}"
                if message:
                    log_msg += f" | {message}"
                if wording:
                    log_msg += f" | {wording}"
                self.warning(log_msg)
                
        except Exception as e:
            self.error(f"解析 API 响应失败：{str(e)}")
