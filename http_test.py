"""
http请求 响应示例
"""
from socket import *

sockfd = socket()
sockfd.bind(("0.0.0.0", 8000))
sockfd.listen(5)
# 浏览器输入地址后会自动链接服务端
connfd, addr = sockfd.accept()
print("connect from :",addr)
# 接收到的是来自浏览器的HTTP请求
data = connfd.recv(1024)
print(data.decode())

# 将数据组织为响应格式
# response = """HTTP/1.1 200 OK
# Content-Type:text/html;charset=UTF-8
#
# This is a test,你好!
# """
response = """HTTP/1.1 200 OK
Content-Type:image/jpeg

"""
with open('timg.jpg', "rb") as f:
    data = f.read()
response = response.encode() + data
print(response)

# 想浏览器发送内容
# connfd.send(response.encode())
connfd.send(response)

connfd.close()
sockfd.close()
