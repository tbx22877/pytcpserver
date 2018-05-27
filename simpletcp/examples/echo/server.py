import queue
from simpletcp.tcpserver import TCPServer


#data is bytes TYPE
def echo(ip, queue, data):
    #print(ip);
    aa = ' '.join(['%02X' % b for b in data])
    print("RX:"+aa)
    #s="teststr\r\n"
    #bufBytes=bytes(s, encoding = "utf8")
    #queue.put(bufBytes)
    queue.put(data)   



server = TCPServer("localhost", 5000, echo)
server.run()
