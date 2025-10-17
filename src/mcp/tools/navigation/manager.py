from typing import Any, Dict
from src.utils.logging_config import get_logger
from .tools import VLNavigation
logger = get_logger(__name__)


# manager.py
class NavigationManager:
    def __init__(self):
        # 初始化代码
        logger.info("[Navigation Manager] 工具管理器初始化")
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册工具
        """
        # 定义工具属性
        tool_props = PropertyList([
            Property("param1", PropertyType.STRING)
        ])

        # 注册工具时的description参数
        tool_description = """
        VLN（Visual-Linguistic Navigation，视觉语言导航）工具：基于实时摄像头画面和自然语言指令，实现物理空间内的自主导航。
        核心能力：
        1. 视觉感知：实时采集摄像头图像，识别环境中的物体（如桌子、门、走廊）、障碍物和路径；
        2. 语言理解：解析自然语言导航指令（如“向前直行2米后左转”“走到红色椅子旁边停下”）；
        3. 路径规划：结合视觉信息和指令，生成 step-by-step 导航路径，并实时调整（如避开突然出现的障碍物）；
        4. 状态反馈：导航过程中返回实时状态（如“已前进1米，距离目标还有1米”“即将左转”）。

        适用场景：
        - 室内短距离导航：如家庭、办公室场景中“到书桌前拿文件”“走到厨房冰箱旁”；
        - 辅助移动：如“向前走3步后停下”“绕过前方椅子”；
        - 目标定位导航：基于物体描述的导航（如“找到白色柜子并停在前方”）。

        参数说明：
        - param1（必需，字符串）：导航指令文本，需包含“动作+目标/距离”（示例：“向前直行2米后左转到桌子前”“走到蓝色沙发旁边”）；
        注意：指令需明确动作（直行/左转/右转/停下），避免模糊表述（如“去那边”“靠近那个东西”会导致解析失败）。

        返回结果：
        - 成功：返回导航启动状态（如“VLN导航已启动，正在执行指令：向前直行2米后左转”）及实时进度更新；
        - 失败：返回错误原因（如“指令解析失败：未包含明确动作”“摄像头未启动，无法采集环境画面”）。

        English Description:
        Visual-Linguistic Navigation (VLN) Tool: Enables autonomous navigation in physical spaces using real-time camera feed and natural language commands.
        Core Capabilities:
        1. Visual Perception: Capture real-time camera images to recognize objects (tables, doors, corridors), obstacles, and paths in the environment;
        2. Language Understanding: Parse natural language navigation commands (e.g., "Go straight 2 meters then turn left", "Walk to the red chair and stop");
        3. Path Planning: Generate step-by-step navigation paths based on visual information and commands, with real-time adjustments (e.g., avoiding sudden obstacles);
        4. Status Feedback: Return real-time navigation status (e.g., "Moved 1 meter, 1 meter left to target", "About to turn left").

        Application Scenarios:
        - Indoor short-distance navigation (e.g., "Get documents from the desk" "Walk to the kitchen fridge" in home/office);
        - Assisted movement (e.g., "Walk 3 steps forward then stop" "Go around the chair ahead");
        - Object-based navigation (e.g., "Find the white cabinet and stop in front of it").

        Parameter Description:
        - param1 (Required, String): Natural language navigation command, must include "action + target/distance" (Examples: "Go straight 2 meters then turn left to the table", "Walk to the blue sofa");
        Note: Commands must include clear actions (go straight/turn left/turn right/stop); vague phrases (e.g., "Go over there" "Get close to that thing") will cause parsing failure.

        Return Result:
        - Success: Returns navigation startup status (e.g., "VLN navigation started, executing command: Go straight 2 meters then turn left") and real-time progress updates;
        - Failure: Returns error reason (e.g., "Command parsing failed: No clear action included" "Camera not activated, cannot capture environment images").
        """
        
        # 注册工具
        add_tool((
            "self.navigation.navigation",
            tool_description,
            tool_props,
            VLNavigation
        ))

# 全局管理器实例
_manager = None

def get_navigation_manager():
    global _manager
    if _manager is None:
        _manager = NavigationManager()
    return _manager