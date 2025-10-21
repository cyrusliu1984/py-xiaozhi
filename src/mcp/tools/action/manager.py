from signal import raise_signal
from turtle import left
from typing import Any, Dict
from src.utils.logging_config import get_logger
from .tools import left_handshake, right_handshake, left_wave, right_wave,  both_hands_wave, cheer_up, fist_greet, point_left,point_right,open_hands

logger = get_logger(__name__)


# manager.py
class ActionManager:
    def __init__(self):
        # 初始化代码（修正类名日志）
        logger.info("[ActionManager] 工具管理器初始化")
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册工具（删除重复注册的右握手方法）
        """
        try:
            self._register_action_left_handshake(add_tool, PropertyList, Property, PropertyType)
            self._register_action_right_handshake(add_tool, PropertyList, Property, PropertyType)
            self._register_action_left_wave(add_tool, PropertyList, Property, PropertyType)
            self._register_action_right_wave(add_tool, PropertyList, Property, PropertyType)
            self._register_action_both_hands_wave(add_tool, PropertyList, Property, PropertyType)
            self._register_action_cheer_up(add_tool, PropertyList, Property, PropertyType)
            self._register_action_fist_greet(add_tool, PropertyList, Property, PropertyType)
            self._register_action_point_left(add_tool, PropertyList, Property, PropertyType)
            self._register_action_point_right(add_tool, PropertyList, Property, PropertyType)
            self._register_action_open_hands(add_tool, PropertyList, Property, PropertyType)
        except Exception as e:  # 修正异常捕获变量未定义问题
            logger.error(f"[ActionManager] 工具注册失败: {e}", exc_info=True)
            raise


    def _register_action_left_handshake(self, add_tool, PropertyList, Property, PropertyType):
        """注册左握手工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误（quary → query）
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
            处理机器人左握手动作的MCP工具调用。输入触发调用的指令，返回MCP调用状态与动作执行状态。适用于：开场欢迎、接待游客、表达友好等场景。
            Handle MCP tool calls for robot's left handshake action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: opening greeting, receiving visitors, expressing friendliness, etc.
        '''

        add_tool(
            (
                "action.left_handshake",
                tool_description,
                props,
                left_handshake,
            )
        )
        logger.debug("[ActionManager] 注册action.left_handshake工具成功")  # 修正日志描述


    def _register_action_right_handshake(self, add_tool, PropertyList, Property, PropertyType):
        """注册右握手工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人右握手动作的MCP工具调用。输入触发调用的指令，返回MCP调用状态与动作执行状态。适用于：开场欢迎、接待游客、表达友好等场景。
                Handle MCP tool calls for robot's right handshake action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: opening greeting, receiving visitors, expressing friendliness, etc.
        '''

        add_tool(
            (
                "action.right_handshake",
                tool_description,
                props,
                right_handshake,
            )
        )
        logger.debug("[ActionManager] 注册action.right_handshake工具成功")  # 修正日志描述


    def _register_action_left_wave(self, add_tool, PropertyList, Property, PropertyType):
        """注册左挥手工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人左挥手动作的MCP工具调用。输入触发调用的挥手指令，返回MCP调用状态与动作执行状态。适用于：MCP调用控制挥手、获取执行反馈、调试联动问题等场景。
                Handle MCP tool calls for robot's left waving action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: MCP call to control waving, obtaining execution feedback, debugging linkage issues, etc.
        '''

        add_tool(
            (
                "action.left_wave",
                tool_description,
                props,
                left_wave,
            )
        )
        logger.debug("[ActionManager] 注册action.left_wave工具成功")  # 修正日志描述


    def _register_action_right_wave(self, add_tool, PropertyList, Property, PropertyType):
        """注册右挥手工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人右挥手动作的MCP工具调用。输入触发调用的挥手指令，返回MCP调用状态与动作执行状态。适用于：MCP调用控制挥手、获取执行反馈、调试联动问题等场景。
                Handle MCP tool calls for robot's right waving action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: MCP call to control waving, obtaining execution feedback, debugging linkage issues, etc.
        '''

        add_tool(
            (
                "action.right_wave",
                tool_description,
                props,
                right_wave,
            )
        )
        logger.debug("[ActionManager] 注册action.right_wave工具成功")  # 修正日志描述


    def _register_action_both_hands_wave(self, add_tool, PropertyList, Property, PropertyType):
        """注册双手挥手工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人双手挥手动作的MCP工具调用。输入触发调用的挥手指令，返回MCP调用状态与动作执行状态。适用于：热情欢迎、群体互动、远距离打招呼等场景。
                Handle MCP tool calls for robot's both hands waving action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: warm welcome, group interaction, greeting from a distance, etc.
        '''

        add_tool(
            (
                "action.both_hands_wave",
                tool_description,
                props,
                both_hands_wave,
            )
        )
        logger.debug("[ActionManager] 注册action.both_hands_wave工具成功")  # 修正日志描述


    def _register_action_cheer_up(self, add_tool, PropertyList, Property, PropertyType):
        """注册欢呼工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人双手向上欢呼动作的MCP工具调用。输入触发调用的指令，返回MCP调用状态与动作执行状态。适用于：庆祝胜利、节日氛围、激励情绪等场景。
                Handle MCP tool calls for robot's hands-up cheer action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: celebrating victory, festival atmosphere, boosting morale, etc.
        '''

        add_tool(
            (
                "action.cheer_up",
                tool_description,
                props,
                cheer_up,
            )
        )
        logger.debug("[ActionManager] 注册action.cheer_up工具成功")  # 修正日志描述


    def _register_action_fist_greet(self, add_tool, PropertyList, Property, PropertyType):
        """注册抱拳工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人双手抱拳动作的MCP工具调用。输入触发调用的指令，返回MCP调用状态与动作执行状态。适用于：传统礼仪、节日祝福、表达尊重等场景。
                Handle MCP tool calls for robot's fist-greeting (kungfu bow) action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: traditional etiquette, festival greetings, showing respect, etc.
        '''

        add_tool(
            (
                "action.fist_greet",
                tool_description,
                props,
                fist_greet,
            )
        )
        logger.debug("[ActionManager] 注册action.fist_greet工具成功")  # 修正日志描述


    def _register_action_point_left(self, add_tool, PropertyList, Property, PropertyType):
        """注册左指引工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人左前方指引动作的MCP工具调用。输入触发调用的指引指令，返回MCP调用状态与动作执行状态。适用于：引导参观、聚焦展品、讲解说明等场景。
                Handle MCP tool calls for robot's left forward pointing action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: guiding tours, focusing on exhibits, giving explanations, etc.
        '''

        add_tool(
            (
                "action.point_left",
                tool_description,
                props,
                point_left,
            )
        )
        logger.debug("[ActionManager] 注册action.point_left工具成功")  # 修正日志描述


    def _register_action_point_right(self, add_tool, PropertyList, Property, PropertyType):
        """注册右指引工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人右前方指引动作的MCP工具调用。输入触发调用的指引指令，返回MCP调用状态与动作执行状态。适用于：引导参观、聚焦展品、讲解说明等场景。
                Handle MCP tool calls for robot's right forward pointing action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: guiding tours, focusing on exhibits, giving explanations, etc.
        '''

        add_tool(
            (
                "action.point_right",
                tool_description,
                props,
                point_right,
            )
        )
        logger.debug("[ActionManager] 注册action.point_right工具成功")  # 修正日志描述


    def _register_action_open_hands(self, add_tool, PropertyList, Property, PropertyType):
        """注册张开双手工具"""
        props = PropertyList(
            [
                Property(
                    "query",  # 修正参数名拼写错误
                    PropertyType.STRING,
                )
            ]
        )
        
        tool_description ='''
                处理机器人张开双手动作的MCP工具调用。输入触发调用的指令，返回MCP调用状态与动作执行状态。适用于：拥抱示意、展示物品、热情欢迎等场景。
                Handle MCP tool calls for robot's open hands action. Input instructions triggering the call, return MCP call status and action execution status. Suitable for: hugging gesture, showing items, warm welcome, etc.
        '''

        add_tool(
            (
                "action.open_hands",  # 修正工具名格式（统一用下划线）
                tool_description,
                props,
                open_hands,
            )
        )
        logger.debug("[ActionManager] 注册action.open_hands工具成功")  # 修正日志描述


# 全局管理器实例
_manager = None

def get_action_manager():
    global _manager
    if _manager is None:
        _manager = ActionManager()
    return _manager
