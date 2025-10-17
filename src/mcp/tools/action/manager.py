from signal import raise_signal
from typing import Any, Dict
from src.utils.logging_config import get_logger
from .tools import action_wave
logger = get_logger(__name__)


# manager.py
class ActionManager:
    def __init__(self):
        # 初始化代码
        logger.info("[CalculateManager] 工具管理器初始化")
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册工具
        """
        try:
            self._register_action_wave_tool(add_tool, PropertyList, Property, PropertyType)
        except ImportError:
            logger.error(f"[ActionManager] 工具注册失败: {e}", exc_info=True)
            raise
    def _register_action_wave_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册wave工具.
        """
        props = PropertyList(
            [
                Property(
                    "quary",
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
            处理机器人挥手动作的MCP工具调用。输入触发调用的挥手指令，返回MCP调用状态与动作执行状态。适用于：MCP调用控制挥手、获取执行反馈、调试联动问题等场景。
            Handle MCP tool calls for robot's waving action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: MCP call to control waving, obtaining execution feedback, debugging linkage issues, etc.
        '''

        add_tool(
            (
                "action.wave",
                tool_description,
                props,
                action_wave,
            )
        )
        logger.debug("[ActionManager] 注册action.wave工具成功")  

# 全局管理器实例
_manager = None

def get_action_manager():
    global _manager
    if _manager is None:
        _manager = ActionManager()
    return _manager