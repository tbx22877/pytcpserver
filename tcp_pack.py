# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 15:20:45 2018

@author: tbx
TCP数据包封装

"""

import queue
from crc16 import CRC_16
from cal_pack import *


PACKTYPE7878 = 0
PACKTYPE7979 = 1
PACKTYPEERR = -1

CMDLOGIN =1
CMDHEAT =0x15
CMDGPSINFO = 0X12

def printbytes(tips, databytes):
    aa = ' '.join(['%02X' % b for b in databytes])
    print(tips+aa) 

class tqTools():
    def __init__(self,databytes,queue):
        self.buf=databytes
        self.queue = queue
        
        d = self.buf
        if (d[0] == 0x78 and d[1] == 0x78):
            self.pType = PACKTYPE7878
            self.cmd = d[3]
        elif (d[0] == 0x79 and d[1] == 0x79):
            self.pType = PACKTYPE7979
            self.cmd = d[4]
        else:
            self.pType = PACKTYPEERR
            self.cmd = 0
            
    def getsn(self):
        if (self.pType == PACKTYPE7878):
            vlen = self.buf[2]
            sn = (self.buf[vlen-1]<<8)+self.buf[vlen]
            return sn
            
    def print(self, tips):
        aa = ' '.join(['%02X' % b for b in self.buf])
        print(tips+aa)   
    
    def socPut(self,buf):
        printbytes('Tx:', buf)
        if (self.queue != 0):
            self.queue.put(buf)
            
    def tqDataHdl(self):
        d = self.buf
        cmd = d[3]
        #print(cmd)
        if (cmd == CMDLOGIN):
            self.tqcmdLogin()
        elif (cmd == CMDHEAT):
            self.tqcmdHeat()
        elif (cmd == CMDGPSINFO):
            self.cmcmdGpsInfo()
        else:
            self.socPut(self.buf)
    
    def tqLoginDataHdl(self):
        if (self.cmd != CMDLOGIN):
            return "imei err"
        else:
            tqlogin = tqLogin_pkt.from_bytes(self.buf[3:12])
            print("cmd:%d" % tqlogin.cmd)
            printbytes("imei:",tqlogin.imei)
            
    def cmGpsInfoDataHdl(self):
        tqlogin = cmGpsInfo_pkt.from_bytes(self.buf[3:])
        print("cmd:%d" % tqlogin.cmd)
        printbytes("imei:",tqlogin.imei)
        print("flag:",tqlogin.flag)
        print("speed:",tqlogin.speed)
        print("csq:",tqlogin.csq)
            
    #登陆包
    def tqcmdLogin(self):
        print('Login')
        sn = self.getsn();
        self.tqLoginDataHdl()
        
        buf = tqPack78(b'\x01',sn)
        self.socPut(buf.data)

    #心跳包    
    def tqcmdHeat(self):
        print('Heat')
        sn = self.getsn();
        buf = tqPack78(b'\x15',sn)
        self.socPut(buf.data)
          
    #宠米定位包
    def cmcmdGpsInfo(self):
        print('Gpsinfo')
        self.cmGpsInfoDataHdl()
        sn = self.getsn();
        buf = tqPack78(b'\x12',sn)
        self.socPut(buf.data)
            
#对7878包的封装
class tqPack78():
    def __init__(self, data, sn):
        self.data = self.pack(data,sn)
        
    def byteH(self,sn):
        return (sn>>8) & 0xff
        
    def byteL(self,sn):
        return (sn) & 0xff
        
    def pack(self,data,sn):
        buf = bytearray()
        buf.append(0x78)
        buf.append(0x78)
        buf.append(0x00)
        packSize = 4
        
        for b1 in data:
            buf.append(b1)
            packSize = packSize+1
        buf[2] = packSize  #包长度
        
        #流水号
        buf.append(self.byteH(sn))
        buf.append(self.byteL(sn))
       
        CRC =   CRC_16()
        crc = CRC.addbytes(bytes(buf)[2:])
        #print('{:X}'.format(crc))
        buf.append(self.byteH(crc))
        buf.append(self.byteL(crc))
        
        buf.append(0x0d)
        buf.append(0x0a)
        
        return bytes(buf)
        
    def print(self,tips):
        printbytes(tips,self.data)



#对7979包的封装
class tqPack79():
    def __init__(self, data, sn):
        self.data = self.pack(data,sn)
        
    def byteH(self,sn):
        return (sn>>8) & 0xff
        
    def byteL(self,sn):
        return (sn) & 0xff
        
    def pack(self,data,sn):
        buf = bytearray()
        buf.append(0x79)
        buf.append(0x79)
        buf.append(0x00)
        buf.append(0x00)
        packSize = 5
        
        for b1 in data:
            buf.append(b1)
            packSize = packSize+1
        buf[2] = self.byteH(packSize)  #包长度
        buf[3] = self.byteL(packSize)  #包长度
        
        #流水号
        buf.append(self.byteH(sn))
        buf.append(self.byteL(sn))
       
        
        buf.append(0x0d)
        buf.append(0x0a)
        
        return bytes(buf)
        
    def print(self,tips):
        printbytes(tips,self.data)


if __name__ == "__main__":
    #78 78 0D 01 52 53 36 78 90 02 42 70 00 01 7B 84 0D 0A
    loginPack = tqPack78(b'\x01\x52\x53\x36\x78\x90\x02\x42\x70',1)
    loginPack.print('login:')


    Pack79 = tqPack79(b'\x31\x32',257)
    Pack79.print('test:')   

    logindata = tqTools(b'\x78\x78\x0D\x01\x52\x53\x36\x78\x90\x02\x42\x70\x00\x02\x49\x1F\x0D\x0A',0)  
    logindata.tqDataHdl()
    
    heatPack = tqTools(b'\x78\x78\x05\x15\x00\x00\x2E\xA1\x0D\x0A',0)
    heatPack.tqDataHdl()
    
'''
TrackerProGetLat--lat:41601456
TrackerProGetLon--lon:205937298
78 78 2d 12 
08 64 11 34 22 43 26 66 -imei
12 02 09 10 3b 03  :年月日时分秒
02 7a c9 b0 0c 46 5a 92 :经纬度
05 a1 00 17 0b 21 1a 1b 1d 1d 18 01 cc 00 28 7d 1f 40 00 05 15 c0 0d 0a
'''