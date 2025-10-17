from typing import Any, Dict
from src.utils.logging_config import get_logger
from .tools import CalculateSum
logger = get_logger(__name__)


# manager.py
class CalculateManager:
    def __init__(self):
        # 初始化代码
        logger.info("[CalculateManager] 工具管理器初始化")
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册工具
        """
        # 定义工具属性
        tool_props = PropertyList([
            Property("param1", PropertyType.INTEGER, default_value=0),
            Property("param2", PropertyType.INTEGER, default_value=0)
        ])
        
        # 注册工具
        add_tool((
            "self.calculate.sum",
            "Calculate the sum of two numbers.",
            tool_props,
            CalculateSum
        ))

# 全局管理器实例
_manager = None

def get_calculate_manager():
    global _manager
    if _manager is None:
        _manager = CalculateManager()
    return _manager