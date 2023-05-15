import sys
import socket
import concurrent.futures
from datetime import datetime

# 获取命令行参数
if len(sys.argv) == 2:
    target = sys.argv[1]
    start_port = 1
    end_port = 65535
elif len(sys.argv) == 4:
    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])
else:
    print("用法: python3 portscanner.py <目标IP> [<起始端口> <结束端口>]")
    sys.exit()

# 获取当前时间
time_start = datetime.now()

# 打印扫描开始信息
print("-" * 50)
print("开始扫描: " + target)
print("扫描时间: " + str(time_start))
print("-" * 50)

# 获取目标主机的IP地址
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("无法解析主机名")
    sys.exit()

# 定义扫描函数
def scan_port(port):
    try:
        # 创建TCP连接
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                # 获取端口支持的协议
                protocol = socket.getservbyport(port)
                print("端口 {}: 开放 ({})".format(port, protocol))
    except Exception:
        pass

# 创建线程池并发扫描
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for port in range(start_port, end_port+1):
        futures.append(executor.submit(scan_port, port))
    concurrent.futures.wait(futures)

# 获取扫描结束时间
time_end = datetime.now()

# 打印扫描结束信息
print("-" * 50)
print("扫描完成: " + target)
print("总耗时: " + str(time_end - time_start))
print("-" * 50)
