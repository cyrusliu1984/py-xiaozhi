# -*- coding: utf-8 -*-
import json
import requests
import sh
import os
import socket
import hashlib
import random
import asyncio  # 导入asyncio模块，用于运行异步函数
from typing import Any, Dict, Optional
from src.utils.logging_config import get_logger

logger = get_logger(__name__)

SERVER_IP = "172.16.128.20"  # 服务器IP地址
SERVER_PORT = 2631           # 服务器端口号，需与服务器一致

# 百度翻译API配置
APPID = '20220227001100072'
SECRET_KEY = 'qhNBPsvQvKsHyfR190ce'


def start_navila():
    """启动导航服务"""
    try:
        result = sh.sh('/home/ubuntu/navila/start_navila.sh')
        print("tmux attach -t navila")
        logger.info(f"导航服务启动结果: {result}")
        return True
    except sh.ErrorReturnCode as e:
        logger.error(f"导航服务启动失败: {e}")
        return False


def stop_navila():
    """停止导航服务"""
    try:
        result = sh.sh('/home/ubuntu/navila/stop_navila.sh')
        logger.info(f"导航服务停止结果: {result}")
        return True
    except sh.ErrorReturnCode as e:
        logger.error(f"导航服务停止失败: {e}")
        return False


def make_md5(s, encoding='utf-8'):
    """生成MD5签名"""
    return hashlib.md5(s.encode(encoding)).hexdigest()


def baidu_translate(chinese_text, appid, secret_key):
    """使用百度翻译API将中文翻译为英文"""
    if not chinese_text or not appid or not secret_key:
        logger.error("翻译参数不完整：文本、appid或secret_key为空")
        return None

    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    
    # 生成随机数和签名
    salt = random.randint(32768, 65536)
    sign_str = f"{appid}{chinese_text}{salt}{secret_key}"
    sign = make_md5(sign_str)
    
    params = {
        "q": chinese_text,
        "from": "zh",  # 源语言：中文
        "to": "en",    # 目标语言：英文
        "appid": appid,
        "salt": salt,
        "sign": sign
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 检查HTTP请求是否成功
        result = response.json()
        
        # 处理API返回的错误
        if "error_code" in result:
            error_code = result["error_code"]
            error_msg = result.get("error_msg", "未知错误")
            logger.error(f"百度翻译API错误: {error_code} - {error_msg}")
            return None
            
        if "trans_result" in result and len(result["trans_result"]) > 0:
            return result["trans_result"][0]["dst"]
        else:
            logger.error("翻译结果解析失败，未找到trans_result")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"翻译请求失败: {str(e)}")
        return None
    except json.JSONDecodeError:
        logger.error("翻译响应不是有效的JSON格式")
        return None
    except Exception as e:
        logger.error(f"翻译过程发生未知错误: {str(e)}")
        return None


def send_to_server(message: str) -> Optional[str]:
    """发送消息到服务器并获取响应"""
    client_socket = None
    try:
        # 创建TCP套接字并连接服务器
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        logger.info(f"已成功连接到服务器 {SERVER_IP}:{SERVER_PORT}")
        
        # 发送数据（确保编码为bytes）
        client_socket.sendall(message.encode('utf-8'))
        
        # 接收响应
        response = client_socket.recv(1024).decode("utf-8")
        logger.info(f"收到服务器响应: {response}")
        return response
        
    except ConnectionRefusedError:
        logger.error(f"无法连接到服务器 {SERVER_IP}:{SERVER_PORT}，请检查服务器是否启动")
        return None
    except socket.timeout:
        logger.error("与服务器通信超时")
        return None
    except Exception as e:
        logger.error(f"与服务器通信发生错误: {str(e)}")
        return None
    finally:
        # 确保套接字关闭
        if client_socket:
            client_socket.close()
            logger.info("客户端套接字已关闭")


def operation(args: dict) -> str:
    """处理导航指令翻译和服务器交互"""
    # 启动导航服务
    if not start_navila():
        return "错误：无法启动导航服务"
    
    # 获取导航指令
    instruction = args.get("param1")
    if not instruction:
        logger.warning("未获取到导航指令参数param1")
        stop_navila()
        return "错误：缺少导航指令参数"
    
    # 翻译指令为英文
    logger.info(f"待翻译的导航指令: {instruction}")
    translated = baidu_translate(instruction, APPID, SECRET_KEY)
    
    if not translated:
        logger.error("翻译指令失败")
        stop_navila()
        return "错误：翻译导航指令失败"
    
    logger.info(f"翻译后的指令: {translated}")
    
    # 发送到服务器并获取结果
    result = send_to_server(translated)
    
    # 停止导航服务
    stop_navila()
    
    if result:
        return f"导航结果: {result}"
    else:
        return "错误：与服务器通信失败"


async def VLNavigation(args: dict) -> str:
    """VL导航工具主函数"""
    try:
        return operation(args)
    except Exception as e:
        logger.error(f"VLNavigation工具执行失败: {e}", exc_info=True)
        # 发生错误时确保导航服务已停止
        stop_navila()
        return f"错误: {str(e)}"


if __name__ == "__main__":
    # 定义测试参数
    args = {
        "param1": "移动到门前然后停下",  # 导航指令参数
    }
    
    # 正确运行异步函数：使用asyncio.run()来执行并等待异步函数完成
    try:
        # 运行异步函数并获取结果
        result = asyncio.run(VLNavigation(args))
        # 打印执行结果
        print("导航操作结果：", result)
    except Exception as e:
        print("执行出错：", str(e))
    