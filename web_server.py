"""
web server

完成一个类,提供给别人
让他能够使用这个类快速的搭建后端web服务

IO多路复用和http训练
"""
from socket import socket
from select import select
import re
# 实现具体功能的类
class WebServer:
    def __init__(self,host = "0.0.0.0", port = 8000, html = None):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 创建套接字
        self.sock = socket()
        self.sock.setblocking(False)
        self.sock.bind((host,port))
    # 处理客户端请求
    def parse(self, data, connfd):
        print("data:",data)
        # 解析请求(请求内容)
        path = re.findall(r'[A-Z]\s(/.*?)\s', data)
        print("请求内容:",path)
        # 没有匹配到内容
        if not path:
            self.rlist.remove(connfd)
            connfd.close()
            print("请求内容不存在")
            return
        # 提取请求内容
        filename = path[0]
        print("访问路径:",self.html,"文件名:",filename)
        self.send_response(connfd, filename)
    # 组织发送响应
    def send_response(self, connfd, filename):
        # 组织文件路径
        if filename == "/":
            filename = "/index.html"
        # 打开失败说明文件不存在
        try:
            fr = open(self.html + filename, "rb")
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "Sorry"
            response = response.encode()
        else:
            file = fr.read()
            response = "HTTP/1.1 200 OK\R\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n" % len(file)
            response += "\r\n"
            response = response.encode() + file
        # if path == "/" or path == "/index.html":
        #     with open(self.html + "/index.html") as i:
        #         index = i.read()
        #     self.sock.send((response + index).encode())
        print("响应:",response)
        # 发送响应给客户端
        # connfd.send(response.encode())
        connfd.send(response)
    # 启动服务
    def start(self):
        self.sock.listen(5)
        print("listen the port %d" % self.port)
        # 首先加入监听套接字
        self.rlist.append(self.sock)
        # 循环监控IO发生
        while True:
            rs,ws,xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock:
                    # 浏览器连接
                    connfd,addr = r.accept()
                    print("已连接:",addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    # 处理客户端http请求
                    # 浏览器发过来请求
                    data = r.recv(1024).decode()
                    print("收到:",data)
                    # if not data:
                    #     continue
                    self.parse(data, r)
            for w in ws:
                pass

if __name__ == '__main__':
    # 1.使用者咋么利用这个类
    # 2.实现类的功能需要使用者提供什么(传参)
    #       地址       网页
    ws = WebServer(host = "0.0.0.0",port = 8000, html = "./static")
    ws.start()