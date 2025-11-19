import websockets
import asyncio
from dotenv import load_dotenv
import os
import json
from logs import Logger
from plugin_manager import PluginManager

load_dotenv()
URL = os.getenv('URL')
# URL=ws://172.16.0.2:3001
# 初始化插件管理器
plugin_manager = PluginManager()

async def connect_and_listen():
    """连接并持续监听消息"""
    while True:
        try:
            async with websockets.connect(URL) as ws:
                Logger().info("已连接至服务器")
                async for message in ws:
                    try:
                        Logger().info(f"收到消息: {message}")
                        msg = json.loads(message)
                        await plugin_manager.process_message(msg, ws)
                    except json.JSONDecodeError:
                        Logger().warning(f"无法解析JSON消息: {message}")
                    except Exception as e:
                        Logger().error(f"处理消息时发生错误: {e}")
        except websockets.exceptions.ConnectionClosed as e:
            Logger().error(f"WebSocket连接已关闭，正在尝试重连... 错误: {e}")
        except websockets.exceptions.InvalidURI as e:
            Logger().error(f"无效的URI，错误: {e}")
            break  # 不可恢复错误，退出
        except websockets.exceptions.InvalidHandshake as e:
            Logger().error(f"握手失败: {e}")
            break  # 可能配置错误，不重试
        except asyncio.CancelledError:
            Logger().info("异步任务被取消")
            break
        except KeyboardInterrupt:
            Logger().info("程序被用户中断")
            break
        except Exception as e:
            Logger().error(f"发生未预期错误: {e}")

        # 重连前等待几秒，避免频繁重试
        Logger().info("将在3秒后尝试重连...")
        await asyncio.sleep(3)

async def main():
    """主函数"""
    try:
        # 加载所有插件
        plugin_manager.load_plugins()
        Logger().info(f"已加载 {plugin_manager.get_plugin_count()} 个插件处理函数")
        await connect_and_listen()
    except KeyboardInterrupt:
        Logger().info("程序已退出")
    except Exception as e:
        Logger().error(f"主循环异常: {e}")
    finally:
        Logger().info("程序已退出")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序已退出")
