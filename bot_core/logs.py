import colorlog
import logging
import sys
import traceback
from datetime import datetime
from typing import Optional, Any

# 添加 SUCCESS 日志级别
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, 'SUCCESS')

# 添加 CRITICAL 级别（如果不存在）
if not hasattr(logging, 'CRITICAL'):
    logging.CRITICAL = 50

class Logger:
    """
    增强的日志记录器，支持多种颜色和日志级别
    """
    def __init__(self, log_name='root', level='INFO'):
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.logger = colorlog.getLogger(log_name)
        
        # 如果处理器已存在，不重复添加
        if not self.logger.handlers:
            handler = colorlog.StreamHandler(sys.stdout)
            
            # 配置颜色方案 - 支持更多颜色
            color_scheme = {
                'DEBUG': 'cyan',           # 青色 - 调试信息
                'INFO': 'green',           # 绿色 - 信息
                'SUCCESS': 'bold_green',   # 粗体绿色 - 成功
                'WARNING': 'yellow',       # 黄色 - 警告
                'ERROR': 'red',            # 红色 - 错误
                'CRITICAL': 'bold_red',    # 粗体红色 - 严重错误
            }
            
            # 创建彩色格式化器
            formatter = colorlog.ColoredFormatter(
                '%(log_color)s[%(asctime)s]%(reset)s '
                '%(log_color)s[%(name)s]%(reset)s '
                '%(log_color)s[%(levelname)s]%(reset)s '
                '%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': color_scheme['DEBUG'],
                    'INFO': color_scheme['INFO'],
                    'SUCCESS': color_scheme['SUCCESS'],
                    'WARNING': color_scheme['WARNING'],
                    'ERROR': color_scheme['ERROR'],
                    'CRITICAL': color_scheme['CRITICAL'],
                },
                secondary_log_colors={},
                style='%',
                reset=True
            )
            
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.level)
        
        self.tz = "Asia/Shanghai"
    
    def _get_time(self):
        """获取当前时区时间"""
        import pytz
        tz = pytz.timezone(self.tz)
        return datetime.now(tz)
    
    def _log(self, level: int, message: Any, exc_info: bool = False):
        """内部日志记录方法"""
        if message is not None:
            if exc_info:
                # 记录异常堆栈信息
                self.logger.log(level, str(message), exc_info=True)
            else:
                self.logger.log(level, str(message))
    
    def debug(self, message: Any, exc_info: bool = False):
        """调试信息 - 青色"""
        self._log(logging.DEBUG, message, exc_info)
    
    def info(self, message: Any, exc_info: bool = False):
        """一般信息 - 绿色"""
        self._log(logging.INFO, message, exc_info)
    
    def success(self, message: Any, exc_info: bool = False):
        """成功信息 - 粗体绿色"""
        self._log(SUCCESS_LEVEL, message, exc_info)
    
    def warning(self, message: Any, exc_info: bool = False):
        """警告信息 - 黄色"""
        self._log(logging.WARNING, message, exc_info)
    
    def error(self, message: Any, exc_info: bool = False):
        """错误信息 - 红色"""
        self._log(logging.ERROR, message, exc_info)
    
    def critical(self, message: Any, exc_info: bool = False):
        """严重错误 - 粗体红色"""
        self._log(logging.CRITICAL, message, exc_info)
    
    def exception(self, message: Any):
        """记录异常信息（自动包含堆栈跟踪）"""
        if message is not None:
            self.logger.exception(str(message))
    
    def error_with_traceback(self, message: Any, exception: Optional[Exception] = None):
        """记录错误并包含完整的堆栈跟踪"""
        if message is not None:
            error_msg = str(message)
            if exception:
                error_msg += f"\n异常类型: {type(exception).__name__}"
                error_msg += f"\n异常信息: {str(exception)}"
                error_msg += f"\n堆栈跟踪:\n{''.join(traceback.format_tb(exception.__traceback__))}"
            self.logger.error(error_msg, exc_info=exception is not None)
    
    def log_exception(self, exception: Exception, context: Optional[str] = None):
        """专门用于记录异常的方法"""
        context_msg = f"{context}: " if context else ""
        self.logger.error(
            f"{context_msg}{type(exception).__name__}: {str(exception)}",
            exc_info=True
        )
