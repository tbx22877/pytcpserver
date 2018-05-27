from simpletcp.clientsocket import ClientSocket
from tcp_pack import tqPack78
from crc16 import CRC_16
from cal_pack import *

#s1 = ClientSocket("localhost", 5000)
#response = s1.send("Hello, World!")

def printbytes(tips, databytes):
    aa = ' '.join(['%02X' % b for b in databytes])
    print(tips+aa) 

def socsend(queue,buf):
    r0 = queue.send(buf.data)
    buf.print('Tx:')
    printbytes('Rx:', r0)
    crc1 =   CRC_16()
    if (not crc1.chkcrc(r0)):
        print('crc err')
    else:
        print('crc ok')


def tqdataTest(cnt):
    s2 = ClientSocket("localhost", 5000, single_use=False)
    
    print('Login test')
    sn = 1
    login_p = tqLogin_pkt(
        cmd = 1,
        imei = (0x52,0x53,0x36,0x78,0x90,0x02,0x42,0x70)
    )    
    
    buf = tqPack78(login_p.to_bytes(),sn)
    socsend(s2, buf)

    print('Heat test')
    sn = 2
    buf = tqPack78(b'\x15',sn)
    socsend(s2, buf)        
  
    sn = 3
    gpsInfo_p = cmGpsInfo_pkt(
        cmd = 0x12,
        imei = (0x08,0x64,0x11,0x34,0x22,0x43,0x26,0x66),
        lat = (0x02,0x7a,0xc9,0xb0),
        lon = (0x0c,0x46,0x5a,0x92),
        flag = 0x05,
        halfCourse = 0xa1,
        speed = 0,
        csq = 0x17,
        sv_used_num = 11,
        gpsLevel = (0x21,0x22,0x22,0x22,0x25,0x1d),
        mcc = (0x01,0xcc),
        mnc = 0,
        lac = (0x28,0x7d),
        ci = (0x1f,0x40)
    )
    d = datetime.datetime.now()
    gpsInfo_p.year = d.year-2000
    gpsInfo_p.mon = d.month
    gpsInfo_p.day = d.day
    gpsInfo_p.hour = d.hour
    gpsInfo_p.min = d.minute
    gpsInfo_p.sec = d.second
    buf = tqPack78(gpsInfo_p.to_bytes(),sn)
    socsend(s2, buf)
  
    #78782D12035160808607827112030E0C142103BF84940CB4F2640509001D0400001400000001CC005390DE8900CB68E40D0A
    #78782D12035160808607827112030E0C142103BF84940CB4F2640509001D0400001400000001CC005390DE8900CB68E40D0A
    #78782D12
    #03 51 60 80 86 07 82 71 
    #12 03 0E 0C 14 21
    #03 BF 84 94 0C B4 F2 64 
    #05 09 00 1D
    #04
    #00 00 14 00 00 00 
    #01 CC 00 53 90 DE 89 
    #00 CB 68 E4 0D 0A
    sn = 0xcb
    gpsInfo_p = cmGpsInfo_pkt(
        cmd = 0x12,
        imei = (0x03 ,0x51 ,0x60 ,0x80 ,0x86 ,0x07 ,0x82 ,0x71),
        lat = (0x03 ,0xBF ,0x84 ,0x94),
        lon = (0x0C ,0xB4 ,0xF2 ,0x64),
        flag = 0x05,
        halfCourse = 0x09,
        speed = 0,
        csq = 0x1d,
        sv_used_num = 4,
        gpsLevel = (0x00,0x00,0x14,0x00,0x00,0x00),
        mcc = (0x01,0xcc),
        mnc = 0,
        lac = (0x53,0x90),
        ci = (0xde,0x89)
    )
    d = datetime.datetime.now()
    gpsInfo_p.year = d.year-2000
    gpsInfo_p.mon = d.month
    gpsInfo_p.day = 0x0e #d.day
    gpsInfo_p.hour = 0x0c #d.hour
    gpsInfo_p.min = 0x14 #d.minute
    gpsInfo_p.sec = 0x21 #d.second
    buf = tqPack78(gpsInfo_p.to_bytes(),sn)
    socsend(s2, buf)
    
    #r1 = s2.send("Hello for the first time...")
    #r2 = s2.send("...and hello for the last!")
    s2.close()

if __name__ == "__main__":
    for i in range(1):
        tqdataTest(i)
    

'''
# Display the correspondence
print("s1 sent\t\tHello, World!")
print("s1 received\t\t{}".format(response.decode("UTF-8")))
print("-------------------------------------------------")
print("s2 sent\t\tHello for the first time....")
print("s2 received\t\t{}".format(r1.decode("UTF-8")))
print("s2 sent\t\t...and hello for the last!.")
print("s2 received\t\t{}".format(r2.decode("UTF-8")))
'''