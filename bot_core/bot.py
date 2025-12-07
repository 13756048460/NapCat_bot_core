import websockets
import asyncio
import json
from .logs import Logger
from .plugin_manager import PluginManager
from .api import BotClient

class Bot:
    def __init__(self, url: str, token: str = None, plugin_dir: str = "plugins"):
        self.url = url
        self.token = token
        self.plugin_manager = PluginManager(plugin_dir)
        self.logger = Logger()

    async def _connect_and_listen(self):
        """连接并持续监听消息"""
        while True:
            try:
                additional_headers = {}
                if self.token:
                    additional_headers["Authorization"] = f"Bearer {self.token}"
                
                async with websockets.connect(self.url, additional_headers=additional_headers) as ws:
                    self.logger.info("已连接至服务器")
                    client = BotClient(ws)
                    async for message in ws:
                        try:
                            self.logger.info(f"收到消息: {message}")
                            msg = json.loads(message)
                            await self.plugin_manager.process_message(msg, client)
                        except json.JSONDecodeError:
                            self.logger.warning(f"无法解析JSON消息: {message}")
                        except Exception as e:
                            self.logger.error(f"处理消息时发生错误: {e}")
            except websockets.exceptions.ConnectionClosed as e:
                self.logger.error(f"WebSocket连接已关闭，正在尝试重连... 错误: {e}")
            except websockets.exceptions.InvalidURI as e:
                self.logger.error(f"无效的URI，错误: {e}")
                break  # 不可恢复错误，退出
            except websockets.exceptions.InvalidHandshake as e:
                self.logger.error(f"握手失败: {e}")
                break  # 可能配置错误，不重试
            except asyncio.CancelledError:
                self.logger.info("异步任务被取消")
                break
            except Exception as e:
                self.logger.error(f"发生未预期错误: {e}")

            # 重连前等待几秒，避免频繁重试
            self.logger.info("将在3秒后尝试重连...")
            await asyncio.sleep(3)

    async def run(self):
        """启动机器人"""
        try:
            # 加载所有插件
            self.plugin_manager.load_plugins()
            # 开启插件热重载监听
            self.plugin_manager.start_watching()
            self.logger.info(f"已加载 {self.plugin_manager.get_plugin_count()} 个插件处理函数")
            await self._connect_and_listen()
        except KeyboardInterrupt:
            self.logger.info("程序已退出")
            self.plugin_manager.stop_watching()
        except Exception as e:
            self.logger.error(f"主循环异常: {e}")
            self.plugin_manager.stop_watching()
        finally:
            self.plugin_manager.stop_watching()
            self.logger.info("程序已退出")
