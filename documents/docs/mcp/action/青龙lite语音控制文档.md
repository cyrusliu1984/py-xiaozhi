# 青龙 lite 语音控制文档

本文档详细说明如何通过 **串口指令** 和 **MCP 工具（UDP 通信）** 控制小智的表情与机械臂动作，适用于开发者调试或集成到自动化系统中。

## 一、概览



| 控制方式   | 协议   | 目标设备               | 适用场景            |
| ------ | ---- | ------------------ | --------------- |
| 串口控制   | UART | 表情主控板              | 表情切换、本地调试       |
| MCP 调用 | UDP  | 192.168.1.100:8889 | 远程动作触发、AI 自动化交互 |

## 二、串口控制：表情管理

通过串口向小智主控板发送文本指令，可切换其面部表情或执行简单动作。

### 2.1 前提条件

⚠️ 确保已连接 USB-TTL 模块，且系统已识别小智设备（通常设备路径为 `/dev/ttyACM0` 或 `/dev/ttyUSB0`）。

### 2.2 串口参数配置



| 参数     | 配置值          |
| ------ | ------------ |
| 波特率    | 115200       |
| 数据位    | 8            |
| 停止位    | 1            |
| 校验位    | 无            |
| 设备路径示例 | /dev/ttyACM0 |

### 2.3 支持的串口指令表



| 指令（字符串） | 动作描述             |
| ------- | ---------------- |
| happy   | 切换为 “开心” 表情      |
| lovely  | 切换为 “可爱” 表情      |
| smile   | 切换为 “微笑” 表情      |
| look    | 执行 “注视” 动作（眼睛聚焦） |
| shake   | 执行 “摇头” 动作       |
| close   | 关闭所有面部表情         |

### 2.4 使用方法（Linux/macOS 系统）

通过终端执行以下命令，向串口发送指令（需将设备路径 `/dev/ttyACM0` 替换为实际识别的路径）：



```
\# 1. 查看所有串口设备，找到小智对应的路径

ls /dev/tty\*

\# 2. 查看当前串口的波特率配置

sudo stty -F /dev/ttyACM0 -a

\# 3. 设置串口波特率为 115200（若当前不是）

sudo stty -F /dev/ttyACM0 115200

\# 示例 1：发送“开心”表情指令（-n 避免附加换行符，确保解析正确）

sudo bash -c 'echo -n "happy" > /dev/ttyACM0'

\# 示例 2：发送“摇头”动作指令

sudo bash -c 'echo -n "shake" > /dev/ttyACM0'

\# 示例 3：发送“关闭表情”指令

sudo bash -c 'echo -n "close" > /dev/ttyACM0'
```

✅ 说明：`-n` 参数用于避免指令后附加换行符，确保主控板能正确解析指令。

## 三、MCP 调用：机械臂动作控制（UDP 协议）

通过 MCP（Modular Control Protocol）工具系统，调用异步函数实现远程机械臂动作控制。底层采用 **UDP 文本协议** 发送整数命令至固定目标。

### 3.1 通信配置



| 参数    | 值                 |
| ----- | ----------------- |
| 目标 IP | 192.168.1.100     |
| 目标端口  | 8889              |
| 传输协议  | UDP               |
| 数据格式  | ASCII 文本（如 "201"） |
| 编码方式  | ASCII             |
| 超时时间  | 10 秒              |

### 3.2 支持的动作与对应指令码



| 函数名                     | 动作描述  | 发送整数 |
| ----------------------- | ----- | ---- |
| right\_handshake(args)  | 右手握手  | 201  |
| left\_handshake(args)   | 左手握手  | 202  |
| right\_wave(args)       | 右手挥手  | 204  |
| left\_wave(args)        | 左手挥手  | 203  |
| both\_hands\_wave(args) | 双手挥动  | 205  |
| cheer\_up(args)         | 加油鼓励  | 206  |
| fist\_greet(args)       | 抱拳打招呼 | 207  |
| point\_left(args)       | 指向左侧  | 暂无动作 |
| point\_right(args)      | 指向右侧  | 208  |
| open\_hands(args)       | 张开双手  | 210  |

### 3.3 MCP 指令发送函数（Python）



```
import socket

import threading

import logging

import asyncio

\# 初始化日志（可根据需求调整日志级别）

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(\_\_name\_\_)

class WebUdpController:

&#x20;   def \_\_init\_\_(self, local\_bind\_ip: str = "0.0.0.0", local\_bind\_port: int = 0):

&#x20;       """初始化UDP控制器，固定目标地址为192.168.1.100:8889"""

&#x20;       try:

&#x20;           # 创建UDP Socket并绑定本地地址

&#x20;           self.sock = socket.socket(socket.AF\_INET, socket.SOCK\_DGRAM)

&#x20;           self.sock.setsockopt(socket.SOL\_SOCKET, socket.SO\_REUSEADDR, 1)

&#x20;           self.sock.bind((local\_bind\_ip, local\_bind\_port))

&#x20;           self.local\_ip, self.local\_port = self.sock.getsockname()

&#x20;           logger.info(f"✅ UDP控制器初始化完成 | 本地绑定：{self.local\_ip}:{self.local\_port}")

&#x20;          &#x20;

&#x20;           # 固定目标地址（用户需求：192.168.1.100:8889）

&#x20;           self.target\_ip = "192.168.1.100"

&#x20;           self.target\_port = 8889

&#x20;           logger.info(f"🎯 目标地址已固定：{self.target\_ip}:{self.target\_port}")

&#x20;       except Exception as e:

&#x20;           logger.error(f"❌ UDP控制器初始化失败：{str(e)}", exc\_info=True)

&#x20;           raise

&#x20;       self.lock = threading.Lock()

&#x20;   def close(self):

&#x20;       """关闭Socket释放资源"""

&#x20;       if self.sock:

&#x20;           self.sock.close()

&#x20;           logger.info(f"🔌 UDP Socket已关闭 | 本地：{self.local\_ip}:{self.local\_port}")

&#x20;   def send\_int\_data(self, data: int, timeout: float = 5.0, add\_newline: bool = False) -> bool:

&#x20;       """

&#x20;       按文本发送，例如 "201"（默认不带换行）。设 add\_newline=True 可发送 "201\n"。

&#x20;       """

&#x20;       try:

&#x20;           with self.lock:

&#x20;               if not isinstance(data, int):

&#x20;                   logger.error(f"❌ 发送数据必须是整数，当前类型：{type(data)}")

&#x20;                   return False

&#x20;               # 修复 f-string 报错问题

&#x20;               newline = "\n" if add\_newline else ""

&#x20;               payload = f"{data}{newline}"

&#x20;               data\_packet = payload.encode("ascii")

&#x20;               packet\_size = len(data\_packet)

&#x20;               logger.debug(f"📦 数据包 | 类型：text | 内容：{repr(payload)} | 大小：{packet\_size}字节")

&#x20;               self.sock.settimeout(timeout)

&#x20;               logger.info(f"🚀 发送文本 {repr(payload)} -> {self.target\_ip}:{self.target\_port} | 超时：{timeout}秒")

&#x20;               sent\_bytes = self.sock.sendto(data\_packet, (self.target\_ip, self.target\_port))

&#x20;               if sent\_bytes != packet\_size:

&#x20;                   logger.warning(f"⚠️  发送不完整！预期{packet\_size}字节，实际{sent\_bytes}字节")

&#x20;                   return False

&#x20;               logger.info(f"✅ 发送成功：{repr(payload)}")

&#x20;               return True

&#x20;       except socket.timeout:

&#x20;           logger.error(f"⏱️  发送超时！{timeout}秒内未完成")

&#x20;           return False

&#x20;       except PermissionError:

&#x20;           logger.error(f"🚫 无权限发送！尝试用 sudo 运行脚本")

&#x20;           return False

&#x20;       except OSError as e:

&#x20;           logger.error(f"🌐 网络错误：{str(e)}", exc\_info=True)

&#x20;           return False

&#x20;       except Exception as e:

&#x20;           logger.error(f"❌ 发送异常：{str(e)}", exc\_info=True)

&#x20;           return False

async def right\_handshake(args: dict) -> str:

&#x20;   """发送整数201的异步函数（右手握手动作）"""

&#x20;   controller = None

&#x20;   try:

&#x20;       # 初始化控制器（本地端口随机，不影响发送）

&#x20;       controller = WebUdpController()

&#x20;       # 发送整数201（对应右手握手动作）

&#x20;       logger.info(f"📢 开始执行发送整数201的任务（右手握手）")

&#x20;       result = await asyncio.to\_thread(

&#x20;           controller.send\_int\_data,

&#x20;           data=201,  # 固定发送201

&#x20;           timeout=10.0

&#x20;       )

&#x20;       return f"\n【最终结果】\n整数201发送到{controller.target\_ip}:{controller.target\_port}：{'成功' if result else '失败'}"

&#x20;   except Exception as e:

&#x20;       err\_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"

&#x20;       logger.error(err\_msg, exc\_info=True)

&#x20;       return err\_msg

&#x20;   finally:

&#x20;       if controller:

&#x20;           controller.close()
```

### 3.4 MCP 工具调用示例（Python）



```
def \_register\_action\_cheer\_up(self, add\_tool, PropertyList, Property, PropertyType):

&#x20;   """注册“加油鼓励”动作的MCP工具"""

&#x20;   props = PropertyList(

&#x20;       \[

&#x20;           Property(

&#x20;               "query",  # 触发调用的指令参数（修正原参数名拼写错误）

&#x20;               PropertyType.STRING,

&#x20;           )

&#x20;       ]

&#x20;   )

&#x20;  &#x20;

&#x20;   tool\_description ='''

&#x20;           处理机器人双手向上欢呼动作的MCP工具调用。输入触发调用的指令，返回MCP调用状态与动作执行状态。

&#x20;           适用于：庆祝胜利、节日氛围、激励情绪等场景。

&#x20;           Handle MCP tool calls for robot's hands-up cheer action. Input instructions triggering the call,&#x20;

&#x20;           return MCP call status and action execution status. Suitable for: celebrating victory, festival atmosphere, boosting morale, etc.

&#x20;   '''

&#x20;   add\_tool(

&#x20;       (

&#x20;           "action.cheer\_up",

&#x20;           tool\_description,

&#x20;           props,

&#x20;           cheer\_up,  # 关联“加油鼓励”动作的执行函数（对应指令码206）

&#x20;       )

&#x20;   )

&#x20;   logger.debug("\[ActionManager] 注册action.cheer\_up工具成功")
```

### 3.5 输出示例



```
\==================================================

【最终结果】

整数204发送到192.168.1.100:8889：成功

\==================================================
```

<video 
  src="demo.mp4"  
  controls                              
  width="100%"                                 
>
  您的设备不支持视频播放
</video>