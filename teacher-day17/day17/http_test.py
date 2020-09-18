"""
http请求 响应示例
"""
from socket import *

sockfd = socket()
sockfd.bind(("0.0.0.0",8000))
sockfd.listen(5)

# 浏览器输入地址后会自动链接服务端
connfd,addr = sockfd.accept()
print("Connect from ",addr)

# 接收到的是来自浏览器的 HTTP请求
data = connfd.recv(1024 * 10)
print(data.decode())

# 将数据组织为响应格式
# response = """HTTP/1.1 404 Not Found
# Content-Type:text/html;charset=UTF-8
#
# 你好,世界
# """

with open('timg.jpg','rb') as f:
    data = f.read()

response = "HTTP/1.1 200 OK\r\n"
response += "Content-Type:image/jpeg\r\n"
response += "\r\n"
response = response.encode() + data

# 向浏览器发送内容
connfd.send(response)

connfd.close()
sockfd.close()

