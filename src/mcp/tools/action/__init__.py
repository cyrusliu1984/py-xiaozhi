"""CalculateMCP工具模块.

提供延迟执行命令的倒计时器功能，支持AI模型状态查询和反馈
"""

from .manager import get_action_manager

__all__ = ["get_action_manager"]
