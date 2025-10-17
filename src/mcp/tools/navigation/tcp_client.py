import socket

# 关键修改：填写服务器的真实IP（不是127.0.0.1！）
# 示例1：若服务器在同一局域网，填服务器的局域网IP（如192.168.1.100）
# 示例2：若服务器有公网IP，填公网IP（如203.xx.xx.xx）
SERVER_IP = "172.16.128.20"  # 必须替换为你的服务器IP！
SERVER_PORT = 2631           # 必须和服务器端口一致！

# 创建TCP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 连接服务器（跨设备核心：目标地址是服务器的真实IP+端口）
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"已成功连接到服务器 {SERVER_IP}:{SERVER_PORT}")
    
    # 发送自定义字符串（可修改为任意内容）
    send_msg = "客户端（跨设备）发送的消息：Hello from another PC！"
    client_socket.sendall(send_msg.encode("utf-8"))
    print(f"已发送消息：{send_msg}")
    
    # 接收服务器的响应
    response = client_socket.recv(1024).decode("utf-8")
    print(f"服务器响应：{response}")
except Exception as e:
    print(f"连接失败！原因：{e}")
finally:
    # 关闭客户端连接
    client_socket.close()