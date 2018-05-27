from calpack import models
import datetime
import pickle

def printbytes(tips, databytes):
    aa = ' '.join(['%02X' % b for b in databytes])
    print(tips+aa) 

def json_int(tips,data):
    aa = ('"%s":%d' % (tips,data))    
    return aa

'''    
class my_pkt(models.Packet):
    # Note: `IntField` bit lengths are configurable!  (See docs for more details)
    field1 = models.IntField()
    field2 = models.IntField(signed=True)


    class multi_int_field_packet(models.Packet):
        arr_int_field = models.ArrayField(models.IntField(), 10)

    expected_vals = tuple(range(10))
    p = multi_int_field_packet()
    p.arr_int_field = expected_vals
'''
        


#登陆包   
class tqLogin_pkt(models.Packet):
    cmd = models.IntField8()
    imei = models.ArrayField(models.IntField8(),8)  

#宠米定位包
#78 78 2d 12 08 64 11 34 22 43 26 66 12 02 09 10 3a 17 02 7a c9 b0 0c 46 5a 92 05 a1 00 17 0b 21 22 22 22 25 1d 01 cc 00 28 7d 1f 40 00 03 19 61 0d 0a
'''	
     VMUINT8 imei[8];		//终端id
	VMUINT8 datetime[6];	//日期时间
	VMUINT8 lat[4];			//纬度
	VMUINT8 lon[4];			//经度
	VMUINT8 flag;
	VMUINT8 halfCourse;     // 角度的一半
	VMUINT8 speed;
	VMUINT8 csq;
	VMUINT8 sv_used_num;
	VMUINT8 gpsLevel[6];
	VMUINT8 mcc[2];
	VMUINT8 mnc;
	VMUINT8 lac[2];
	VMUINT8 ci[2];
 '''
 
class cmGpsInfo_pkt(models.Packet):
    cmd = models.IntField8()
    imei = models.ArrayField(models.IntField8(),8)
    year = models.IntField8()
    mon = models.IntField8()
    day = models.IntField8()
    hour = models.IntField8()
    min = models.IntField8()
    sec = models.IntField8()
    lat = models.ArrayField(models.IntField8(),4)
    lon = models.ArrayField(models.IntField8(),4)
    flag = models.IntField8()
    halfCourse = models.IntField8()
    speed = models.IntField8()
    csq = models.IntField8()
    sv_used_num = models.IntField8()
    gpsLevel = models.ArrayField(models.IntField8(),6)
    mcc = models.ArrayField(models.IntField8(),2)
    mnc = models.IntField8()
    lac = models.ArrayField(models.IntField8(),2)
    ci = models.ArrayField(models.IntField8(),2)
    
    def json(self):
        return(json_int('cmd',self.cmd))
        
if __name__ == "__main__":   
    ##x01\x52\x53\x36\x78\x90\x02\x42\x70
    login_p = tqLogin_pkt(
        cmd = 1,
        imei = (0x52,0x53,0x36,0x78,0x90,0x02,0x42,0x70)
    )
    printbytes("Login:",login_p.to_bytes())
    
    ##定位包
    #78 78 2d 12 
    #08 64 11 34 22 43 26 66 
    #12 02 09 10 3a 17 
    #02 7a c9 b0 0c 46 5a 92 
    #05 a1 00 17 0b 21 22 22 22 25 1d 01 cc 00 28 7d 1f 40 00 03 19 61 0d 0a
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
    
    printbytes("CM Gps Info:",gpsInfo_p.to_bytes())
    print(gpsInfo_p.json())
    #print(pickle.dumps(gpsInfo_p))