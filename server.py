import queue
from simpletcp.tcpserver import TCPServer
from tcp_pack import tqPack78
from tcp_pack import tqTools
from crc16 import CRC_16


def printbytes(tips, databytes):
    aa = ' '.join(['%02X' % b for b in databytes])
    print(tips+aa) 
    
    
#data is bytes TYPE
def echo(ip, queue, data):
    print(ip);
    printbytes('-----Rx------:\r', data)  
    
    crc1 =   CRC_16()
    if (not crc1.chkcrc(data)):
        print('crc err')
        s="teststr\r\n"
        bufBytes=bytes(s, encoding = "utf8")
        queue.put(bufBytes)
    else:
        print('crc ok')
        d = data
        
        if (d[0] == 0x78 and d[1] == 0x78):
            tq = tqTools(data,queue)
            tq.tqDataHdl()
    


    
print("Server in port:5000")
server = TCPServer("localhost", 5000, echo)
server.run()
