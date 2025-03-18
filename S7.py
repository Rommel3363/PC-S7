import snap7
from snap7.util import *
import main
import sys

class write2PLC():
    def __init__(self,PLC_IP = '192.168.0.211', db_number = 1, start = 0, distence = 114):
        self.PLC_IP = PLC_IP
        self.db_number = db_number
        self.start = start
        self.distence = distence
    def turnToDoubleByte(self,num):
        if num<256:
            result = bytearray([0,num])
            return result
        else:
            binary = bin(num)[2:]
                # 删去低8位的0
            highEightB = binary[:-8]
            lowEightB = binary[-8:]

            highEightO = int(highEightB,2)
            lowEightO = int(lowEightB,2)
            
            result = bytearray([highEightO,lowEightO])
            return result

    def connectAndWrite(self):
        # 创建PLC客户端
        client = snap7.client.Client()
        # 连接到PLC
        client.connect(self.PLC_IP, 0, 1)  # 0和1分别是机架号和插槽号，根据你的PLC进行调整
        

        if client.get_connected():
            print("成功连接到PLC")
            data = self.turnToDoubleByte(self.distence)
            # data = bytearray([0,distence])  # 要写入的数据，示例为写入整数123

            resu = client.db_write(self.db_number, self.start, data)
            print("成功写入数据")

            # 断开连接
            client.disconnect()
        else:
            print("无法连接到PLC")


if __name__ == '__main__':
    app = main.QApplication(sys.argv)
    ex = main.ImageClassifierApp()
    ex.show()
    # distanceDataBlock = write2PLC(PLC_IP = '192.168.0.211', db_number = 1, start = 0, distence = 114)
    # distanceDataBlock.connectAndWrite()
    sys.exit(app.exec_())


        
    