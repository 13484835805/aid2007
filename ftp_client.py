from socket import socket
from time import sleep
import os,sys
class FTPClient:
    def __init__(self, socket):
        self.socket = socket
    def quit(self):
        self.socket.send(b"EXIT")
        self.socket.close()
        sys.exit("谢谢使用")
    def retr(self):
        name = input("请输入文件名称:")
        self.socket.send(("RETR" + name).encode())
        result = self.socket.recv(256)
        print(result.decode())
        if result == b"OK":
            fw = open("/home/tarena/aid2007/" + name, "wb")
            while True:
                data = self.socket.recv(1024)
                if data == b"$$":
                    break
                fw.write(data)
            fw.close()
            print("下载完毕")
        else:
            print("文件不存在")
    def stor(self):
        name = input("请输入文件名称:")
        if os.path.isfile(name):
            if not os.path.exists(name):
                print("文件不存在")
                return
        else:
            return
        filename = name.split("/")[-1]
        print("旧",name,"新:",filename)
        self.socket.send(("STOR" + filename).encode())
        result = self.socket.recv(1024)
        print(result.decode())
        if result == b"YES":
            try:
                fr = open(name, "rb")
            except:
                return
            while True:
                data = fr.read(1024)
                if not data:
                    break
                self.socket.send(data)
            fr.close()
            sleep(0.1)
            self.socket.send(b"$$")
            print("上传成功")
        else:
            print("文件已存在")
    def list(self):
        self.socket.send(b"LIST")
        result = self.socket.recv(1024).decode()
        if result == "FAIL":
            print("没有文件存在")
        else:
            file_name = self.socket.recv(1024 * 10).decode()
            print(file_name)
def main():
    tcp_socket = socket()
    tcp_socket.connect(("127.0.0.1", 8888))
    fc = FTPClient(tcp_socket)
    while True:
        print("""
        =========命令选项=========
        查看文件列表:LIST
        上传文件:STOR
        下载文件:RETR
        退出:EXIT
        ========================
        """)
        commod = input("请输入命令:")
        if commod == "LIST":
            fc.list()
        elif commod == "STOR":
            fc.stor()
        elif commod == "RETR":
            fc.retr()
        elif commod == "EXIT":
            fc.quit()

if __name__ == '__main__':
    main()