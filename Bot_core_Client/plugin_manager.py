import importlib
import sys
import inspect
import os
from pathlib import Path
from .logs import Logger
from .api.client import Message, _plugin_registry

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PluginFileHandler(FileSystemEventHandler):
    """监听插件文件变化的处理器"""
    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager
        self.logger = Logger()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            self.logger.info(f"检测到新文件: {event.src_path}")
            self.plugin_manager.load_plugins()

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py"):
            self.logger.info(f"检测到文件修改: {event.src_path}")
            self.plugin_manager.load_plugins()

class PluginManager:
    """动态插件管理器"""

    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []  # 存储所有加载的插件函数
        self.logger = Logger()
        self.observer = None

    def load_plugins(self):
        """动态加载所有插件（递归遍历子文件夹）"""
        # 检查插件目录是否为空或不存在
        plugin_path = Path(self.plugin_dir)
        if not self.plugin_dir or not plugin_path.exists():
            # 如果插件目录为空或不存在，则在当前项目根目录下查找包含装饰器的类
            self.logger.info("插件目录为空或不存在，开始在项目中查找包含装饰器的类...")
            self._load_plugins_from_project()
            return

        # 递归获取所有 .py 文件（排除 __init__.py 和 __pycache__）
        plugin_files = [
            f for f in plugin_path.rglob("*.py")
            if f.stem != '__init__' and '__pycache__' not in f.parts
        ]

        if not plugin_files:
            self.logger.warning(f"在 {self.plugin_dir} 目录下未找到插件文件")
            # 尝试在项目中查找包含装饰器的类
            self._load_plugins_from_project()
            return

        # 清空现有插件列表，重新加载
        self.plugins = []
        self.logger.info("开始重新加载插件...")

        # 清空插件注册表
        _plugin_registry.clear()
        
        for plugin_file in plugin_files:
            try:
                # 计算相对于插件目录的路径
                relative_path = plugin_file.relative_to(plugin_path)
                # 构建模块路径，将路径分隔符替换为点号
                # 例如: plugins/src/hello.py -> plugins.src.hello
                module_parts = [self.plugin_dir] + list(relative_path.parts[:-1]) + [relative_path.stem]
                module_name = '.'.join(module_parts)

                # 如果模块已加载，先重新加载
                if module_name in sys.modules:
                    module = importlib.reload(sys.modules[module_name])
                else:
                    module = importlib.import_module(module_name)

                # 检查模块是否包含任何插件装饰的函数
                # 从插件注册表中获取当前模块的插件函数
                module_plugins = []
                for name, func in _plugin_registry.items():
                    # 检查函数是否属于当前模块
                    if (hasattr(func, '__module__') and
                        func.__module__ == module_name):
                        module_plugins.append((name, func))

                if module_plugins:
                    for plugin_name, plugin_func in module_plugins:
                        self.plugins.append(plugin_func)
                        self.logger.info(f"成功加载插件 [{plugin_name}] 从模块 {module_name}")
                # 如果没有使用@plugin装饰器的函数，静默处理，不显示任何信息

            except Exception as e:
                self.logger.error(f"加载插件 {plugin_file} 时发生错误: {e}")

        self.logger.info(f"插件加载完成，共 {len(self.plugins)} 个处理函数")

    def _load_plugins_from_project(self):
        """从整个项目中加载包含装饰器的类"""
        # 获取项目根目录
        project_root = Path('.').resolve()
        
        # 递归查找所有.py文件
        all_py_files = [
            f for f in project_root.rglob("*.py")
            if f.stem != '__init__' and '__pycache__' not in f.parts and 'venv' not in f.parts and '.venv' not in f.parts
        ]
        
        # 清空现有插件列表，重新加载
        self.plugins = []
        self.logger.info("开始从项目中加载插件...")
        
        # 清空插件注册表
        _plugin_registry.clear()
        
        # 临时保存已导入的模块，避免重复导入
        imported_modules = set()
        
        for py_file in all_py_files:
            try:
                # 将文件路径转换为模块名
                relative_path = py_file.relative_to(project_root)
                module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
                if module_parts[0] == '':  # 处理根目录文件
                    module_parts = [relative_path.stem]
                module_name = '.'.join(module_parts)
                
                # 避免重复导入
                if module_name in imported_modules:
                    continue
                
                # 尝试导入模块
                if module_name in sys.modules:
                    module = importlib.reload(sys.modules[module_name])
                else:
                    module = importlib.import_module(module_name)
                
                imported_modules.add(module_name)
                
                # 检查模块是否包含任何插件装饰的函数
                module_plugins = []
                for name, func in _plugin_registry.items():
                    # 检查函数是否属于当前模块
                    if (hasattr(func, '__module__') and
                        func.__module__ == module_name):
                        module_plugins.append((name, func))

                if module_plugins:
                    for plugin_name, plugin_func in module_plugins:
                        self.plugins.append(plugin_func)
                        self.logger.info(f"成功加载插件 [{plugin_name}] 从模块 {module_name}")
                        
            except Exception as e:
                # 忽略导入失败的模块，继续处理其他文件
                self.logger.debug(f"尝试导入模块 {py_file} 时发生错误，已跳过: {e}")
                continue
        
        self.logger.info(f"项目插件加载完成，共 {len(self.plugins)} 个处理函数")

    def start_watching(self):
        """开始监听插件目录变化"""
        if self.observer:
            return

        event_handler = PluginFileHandler(self)
        self.observer = Observer()
        
        # 如果插件目录为空，则监听整个项目目录
        watch_dir = self.plugin_dir if self.plugin_dir else "."
        
        # 检查目录是否存在，如果不存在则不启动监听
        import os
        if not os.path.exists(watch_dir):
            self.logger.warning(f"监听目录 {watch_dir} 不存在，跳过启动监听器")
            return
            
        self.observer.schedule(event_handler, watch_dir, recursive=True)
        self.observer.start()
        self.logger.info(f"开始监听插件目录: {watch_dir}")

    def stop_watching(self):
        """停止监听"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

    async def process_message(self, msg: dict, client):
        """处理消息，调用所有注册的插件函数"""
        # 将字典消息包装成 Message 对象
        message_obj = Message(msg)
        for plugin_func in self.plugins:
            try:
                # 检查函数签名以确定传递哪种类型的参数
                sig = inspect.signature(plugin_func)
                params = list(sig.parameters.values())

                # 如果第一个参数期望 Message 类型，则传递包装后的对象
                if (len(params) >= 1 and
                    params[0].annotation == Message):
                    await plugin_func(message_obj, client)
                else:
                    # 否则传递原始字典
                    await plugin_func(msg, client)
            except Exception as e:
                self.logger.error(f"插件 {plugin_func.__name__} 处理消息时发生错误: {e}")

    def get_plugin_count(self):
        """获取已加载的插件函数数量"""
        return len(self.plugins)
