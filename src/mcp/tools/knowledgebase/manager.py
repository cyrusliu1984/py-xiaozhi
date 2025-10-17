from typing import Any, Dict
from src.utils.logging_config import get_logger
from .tools import KnowledgeBase
logger = get_logger(__name__)


# manager.py
class KnowledgeBaseManager:
    def __init__(self):
        # 初始化代码
        logger.info("[KnowledgeBaseManager] 工具管理器初始化")
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册工具
        """
        # 定义工具属性
        tool_props = PropertyList([
            Property("param1", PropertyType.STRING),
        ])
        
        tool_description ='''
            本工具为青龙机器人知识库的MCP调用工具，可提供全面的青龙机器人相关知识查询、操作指导及问题解决方案。涵盖范围包括：硬件详细参数（如传感器型号、处理器性能）、自由度设计（关节数量及运动范围）、设备选型依据、技术架构（软件分层、通信协议）等核心知识；同时支持基础功能说明（安装部署、初始化配置）、故障排查（如运动卡顿、传感器数据异常、程序运行失败）及进阶操作指导（自定义运动轨迹、扩展硬件模块、优化控制算法）。

            使用场景：
            1. 初次接触青龙机器人，需了解硬件组成、安装流程及基础配置方法；
            2. 遇到机器人运动故障、传感器数据异常、程序脚本执行失败等问题时，需获取排查步骤；
            3. 需进行进阶操作（如调整自由度参数、更换核心部件、二次开发接口调用）时，需详细操作指南。

            参数：
            question: 青龙机器人相关问题描述（必需），示例：“青龙机器人的自由度设计有什么特点？”

            返回格式：
            {
            "core_answer": "核心问题解答（直接回应用户疑问）"
            }


            English Description：
            This tool is an MCP calling tool for the Qinglong Robot knowledge base, providing comprehensive knowledge queries, operation guidance, and problem-solving solutions related to Qinglong Robot. Its coverage includes: core knowledge such as detailed hardware parameters (e.g., sensor models, processor performance), degree of freedom design (number of joints and motion range), equipment selection basis, and technical architecture (software layering, communication protocols); it also supports basic function explanations (installation and deployment, initial configuration), troubleshooting (e.g., motion stuttering, abnormal sensor data, program execution failures), and advanced operation guidance (custom motion trajectories, expanding hardware modules, optimizing control algorithms).

            Usage scenarios:
            1. First-time users of Qinglong Robot who need to understand hardware composition, installation processes, and basic configuration methods;
            2. Users who encounter issues such as robot motion failures, abnormal sensor data, or program script execution failures and need troubleshooting steps;
            3. Users who need to perform advanced operations (e.g., adjusting degree of freedom parameters, replacing core components, calling secondary development interfaces) and require detailed operation guides.

            Parameters:
            question: Description of the question related to Qinglong Robot (required), example: "What are the characteristics of the degree of freedom design of Qinglong Robot?"

            Return format:
            {
            "core_answer": "Core answer to the question (directly responds to the user's inquiry)"
            }
        '''
        # 注册工具
        add_tool((
            "self.KnowledgeBase.qinglong",
            tool_description,
            tool_props,
            KnowledgeBase
        ))

# 全局管理器实例
_manager = None

def get_knowledgebase_manager():
    global _manager
    if _manager is None:
        _manager = KnowledgeBaseManager()
    return _manager