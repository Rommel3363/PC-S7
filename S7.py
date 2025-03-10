import snap7
from snap7.util import *

# 定义PLC的IP地址
PLC_IP = '192.168.0.211'  # 替换为你的PLC的IP地址

# 创建PLC客户端
client = snap7.client.Client()

# 连接到PLC
client.connect(PLC_IP, 0, 1)  # 0和1分别是机架号和插槽号，根据你的PLC进行调整

if client.get_connected():
    print("成功连接到PLC")

    # 写入数据到PLC DB块
    db_number = 1  # DB块号
    start = 0  # 起始地址
    data = bytearray([123])  # 要写入的数据，示例为写入整数123

    client.db_write(db_number, start, data)
    print("成功写入数据")

    # 断开连接
    client.disconnect()
else:
    print("无法连接到PLC")