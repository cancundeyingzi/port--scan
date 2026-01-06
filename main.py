import socket
import sys
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from loguru import logger

logger.remove()
logger.add(sys.stderr,level="TRACE")

class ScanPort:
    def __init__(self):
        self.ip = None

    def scan_port(self, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #函数socket.socket创建一个socket套接字，该函数带有两个参数：
            # 参数⼀：family(地址簇)，可供选择的有socket.AF_INET(默认) 为IPv4，socket.AF_INET6,为IPv6但是下面的dns解析貌似不能用...
            # 参数⼆：type（socket类型），如socket.SOCK_STREAM为TCP(默认)，SOCK_DGRAM为UDP。
            res = s.connect_ex((self.ip, port))
            if res == 0:  # 端口开启
                logger.warning('Ip:{} Port:{} IS OPEN'.format(self.ip, port))
            #else:
                #print('Ip:{} Port:{}: IS NOT OPEN'.format(self.ip, port))
        except Exception as e:
            logger.error(e)
        finally:
            s.close()

    def start(self):
        remote_server = "bilibili.com"#'8.217.13.38'
        self.ip = socket.gethostbyname(remote_server)#域名转ip
        #self.ip = '[2409:8a28:cfb:e5e7:7c3f:9f53:d794:6171]'
        self.ip = '10.53.152.43'
        logger.info(socket.gethostbyname(remote_server))
        t1 = datetime.now()  # 开始时间
        每次增加=100
        x=10000  #开始端口
        while x<11000:  #结束端口,最大65535
            ports = [i for i in range(x, x+每次增加 if x+每次增加<65536 else 65536)]#包括前面不包括后面
            socket.setdefaulttimeout(9)#单个端口等待时间
            # 设置多进程
            threads = []
            pool = ThreadPool(processes=每次增加)#线程数,线程数量过高,端口等待时间又太短,就会漏掉一些
            pool.map(self.scan_port, ports)
            pool.close()
            pool.join()
            x=x+每次增加
            logger.trace('扫描进度    '+str(x))

        logger.success('端口扫描已完成，耗时：    '+ str(datetime.now() - t1))


ScanPort().start()
