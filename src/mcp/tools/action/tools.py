import struct
import socket
import threading
import asyncio
# 基础日志配置（确保调试信息可见）
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class WebUdpController:
    def __init__(self, local_bind_ip: str = "0.0.0.0", local_bind_port: int = 0):
        """初始化UDP控制器，固定目标地址为192.168.1.100:8889"""
        try:
            # 创建UDP Socket并绑定本地地址
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((local_bind_ip, local_bind_port))
            self.local_ip, self.local_port = self.sock.getsockname()
            logger.info(f"✅ UDP控制器初始化完成 | 本地绑定：{self.local_ip}:{self.local_port}")
            
            # 固定目标地址（用户需求：192.168.1.100:8889）
            self.target_ip = "192.168.1.100"
            self.target_port = 8889
            logger.info(f"🎯 目标地址已固定：{self.target_ip}:{self.target_port}")

        except Exception as e:
            logger.error(f"❌ UDP控制器初始化失败：{str(e)}", exc_info=True)
            raise

        self.lock = threading.Lock()

    def close(self):
        """关闭Socket释放资源"""
        if self.sock:
            self.sock.close()
            logger.info(f"🔌 UDP Socket已关闭 | 本地：{self.local_ip}:{self.local_port}")

    def send_int_data(self, data: int, timeout: float = 5.0, add_newline: bool = False) -> bool:
        """
        按文本发送，例如 "201"（默认不带换行）。设 add_newline=True 可发送 "201\n"。
        """
        try:
            with self.lock:
                if not isinstance(data, int):
                    logger.error(f"❌ 发送数据必须是整数，当前类型：{type(data)}")
                    return False

                # 修复 f-string 报错问题
                newline = "\n" if add_newline else ""
                payload = f"{data}{newline}"
                data_packet = payload.encode("ascii")
                packet_size = len(data_packet)

                logger.debug(f"📦 数据包 | 类型：text | 内容：{repr(payload)} | 大小：{packet_size}字节")

                self.sock.settimeout(timeout)
                logger.info(f"🚀 发送文本 {repr(payload)} -> {self.target_ip}:{self.target_port} | 超时：{timeout}秒")

                sent_bytes = self.sock.sendto(data_packet, (self.target_ip, self.target_port))

                if sent_bytes != packet_size:
                    logger.warning(f"⚠️  发送不完整！预期{packet_size}字节，实际{sent_bytes}字节")
                    return False

                logger.info(f"✅ 发送成功：{repr(payload)}")
                return True

        except socket.timeout:
            logger.error(f"⏱️  发送超时！{timeout}秒内未完成")
            return False
        except PermissionError:
            logger.error(f"🚫 无权限发送！尝试用 sudo 运行脚本")
            return False
        except OSError as e:
            logger.error(f"🌐 网络错误：{str(e)}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"❌ 发送异常：{str(e)}", exc_info=True)
            return False



async def right_handshake(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()


        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=201,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()

async def left_handshake(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=201,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()


async def left_wave(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=203,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()


async def right_wave(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=204,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()


async def both_hands_wave(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=205,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()



async def cheer_up(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=206,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()


async def fist_greet(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=207,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()

async def point_left(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=207,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()


async def point_right(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=208,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()


async def open_hands(args: dict) -> str:
    """发送整数201的异步函数"""
    controller = None
    try:
        # 初始化控制器（本地端口随机，不影响发送）
        controller = WebUdpController()

        # 发送整数201（用户需求的核心数据）
        logger.info(f"📢 开始执行发送整数201的任务")
        result = await asyncio.to_thread(
            controller.send_int_data,
            data=210,  # 固定发送201
            timeout=10.0
        )

        return f"\n【最终结果】\n整数201发送到{controller.target_ip}:{controller.target_port}：{'成功' if result else '失败'}"

    except Exception as e:
        err_msg = f"\n【最终结果】\n发送失败：{str(e)}\n建议查看上方日志排查问题！"
        logger.error(err_msg, exc_info=True)
        return err_msg
    finally:
        if controller:
            controller.close()




# 直接运行时发送整数201
if __name__ == "__main__":
    try:
        # 启动事件循环执行发送任务
        result = asyncio.run(action_wave())
        # 打印最终结果
        print("\n" + "="*50)
        print(result)
        print("="*50)
    except KeyboardInterrupt:
        print("\n\n🔌 程序被手动中断（Ctrl+C）")
    except Exception as e:
        print(f"\n\n❌ 执行异常：{str(e)}", exc_info=True)
