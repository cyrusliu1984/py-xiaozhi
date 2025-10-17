import json
import os
import requests
import uuid
import json
from typing import Any, Dict
from src.utils.logging_config import get_logger
logger = get_logger(__name__)

BASE_URL = os.getenv("KNOWLEDGE_BASE_URL", "http://localhost:8080/api/v1")
API_KEY = os.getenv("KNOWLEDGE_API_KEY", "sk-W1BUWaIuoac11EGT6eO-6mwihz_q9QK_Eokrh-fHK-mSeJ6T")
def knowledge_chat(kb_chat_id: str, query: str) -> dict:
    """
    调用知识库对话接口，获取流式回答及引用来源
    
    参数:
        kb_chat_id: 知识库对话ID（用于上下文关联）
        query: 用户的查询问题（需要向知识库提问的内容）
    
    返回:
        包含回答内容和知识引用的字典，格式为:
        {
            "success": bool,  # 调用是否成功
            "answer": str,    # 拼接后的完整回答
            "knowledge_references": list  # 引用的知识库条目列表
        }
    """
    url = f"{BASE_URL}/knowledge-chat/{kb_chat_id}"
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "X-Request-ID": str(uuid.uuid4())
    }
    
    data = {"query": query}
    
    try:
        with requests.post(
            url,
            json=data,
            headers=headers,
            stream=True,  # 启用流式响应处理
            timeout=30
        ) as response:
            response.raise_for_status()  # 检查HTTP错误
            
            full_answer = ""
            references = []
            
            # 解析SSE流式响应
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data:"):
                        try:
                            event_data = json.loads(line[5:].strip())
                            if event_data.get("response_type") == "references":
                                references = event_data.get("knowledge_references", [])
                            elif event_data.get("response_type") == "answer":
                                full_answer += event_data.get("content", "")
                                if event_data.get("done") is True:
                                    break
                        except json.JSONDecodeError:
                            return {"success": False, "error": {"message": "响应格式解析失败"}}
            
            return {
                "success": True,
                "answer": full_answer,
                "knowledge_references": references
            }
    
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": {"message": f"请求失败: {str(e)}"}}
    except Exception as e:
        return {"success": False, "error": {"message": f"处理失败: {str(e)}"}}
async def KnowledgeBase(args: dict) -> str:
    kb_chat_id = "a54ec473-478a-4358-b2fa-0c19337abc60"
    try:
        # 业务逻辑
        param1 = args.get("param1", 0)
        result = knowledge_chat(kb_chat_id,param1)
        return f"成功: {result['answer']}"
    except Exception as e:
        logger.error(f"工具执行失败: {e}")
        return f"错误: {str(e)}"