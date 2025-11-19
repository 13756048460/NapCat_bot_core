import importlib
import sys
import inspect
from pathlib import Path
from logs import Logger

class PluginManager:
    """动态插件管理器"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []  # 存储所有加载的插件函数
        self.logger = Logger()
    
    def load_plugins(self):
        """动态加载所有插件（递归遍历子文件夹）"""
        plugin_path = Path(self.plugin_dir)
        if not plugin_path.exists():
            self.logger.warning(f"插件目录 {self.plugin_dir} 不存在")
            return
        
        # 递归获取所有 .py 文件（排除 __init__.py 和 __pycache__）
        plugin_files = [
            f for f in plugin_path.rglob("*.py")
            if f.stem != '__init__' and '__pycache__' not in f.parts
        ]
        
        if not plugin_files:
            self.logger.warning(f"在 {self.plugin_dir} 目录下未找到插件文件")
            return
        
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
                
                # 查找模块中所有的异步函数（排除私有函数和特殊方法）
                # 只获取模块中定义的函数，不包括导入的函数
                module_file = plugin_file.resolve()
                functions = []
                for name, obj in inspect.getmembers(module, inspect.isfunction):
                    # 检查是否是模块中定义的函数（不是导入的）
                    if (inspect.iscoroutinefunction(obj) and 
                        not name.startswith('_') and
                        hasattr(obj, '__module__') and
                        obj.__module__ == module_name):
                        # 进一步检查函数定义的文件
                        try:
                            func_file = inspect.getfile(obj)
                            if Path(func_file).resolve() == module_file:
                                functions.append(obj)
                        except (TypeError, OSError):
                            # 如果无法获取文件，跳过（可能是内置函数）
                            pass
                
                if functions:
                    self.plugins.extend(functions)
                    self.logger.info(f"成功加载插件 {module_name}，发现 {len(functions)} 个处理函数")
                else:
                    self.logger.warning(f"插件 {module_name} 中未找到异步处理函数")
                    
            except Exception as e:
                self.logger.error(f"加载插件 {plugin_file} 时发生错误: {e}")
    
    async def process_message(self, msg: dict, websocket):
        """处理消息，调用所有注册的插件函数"""
        for plugin_func in self.plugins:
            try:
                await plugin_func(msg, websocket)
            except Exception as e:
                self.logger.error(f"插件 {plugin_func.__name__} 处理消息时发生错误: {e}")
    
    def get_plugin_count(self):
        """获取已加载的插件函数数量"""
        return len(self.plugins)

