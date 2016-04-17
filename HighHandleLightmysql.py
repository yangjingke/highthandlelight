#coding=utf-8
import re
import MySQLdb
from db import Light,Lightstatuslog,Warninglog
class DataInfo:        #整个数据的类
    dstAddress = ''
    srcAddress = ''
    nCode = ''
    nTextSize = 0
    groupNum = ''
    lpszText = ''
    phase1 = ''
    phase2 = ''
    phase3 = ''
    checkCode = ''
    singleLampInfo=[]
    def __init__(self,groupNum = '',dstAddress = '',srcAddress ='',nCode = 0,nTextSize = '',lpszText = '',phase1 = '',phase2 = '',phase3 = '',checkCode = ''): 
        self.dstAddress = dstAddress  
        self.srcAddress = srcAddress  
        self.nCode = nCode
        self.nTextSize = nTextSize
        self.groupNum = groupNum
        self.lpszText = lpszText  
        self.checkCode = checkCode  
        self.phase1 = phase1
        self.phase2 = phase2
        self.phase3 = phase3
    def ParsedateInfo(self,dateinfo):
        self.dstAddress = dateinfo[0:4]
        self.srcAddress = dateinfo[4:8]
        self.nCode = dateinfo[8:10]
        self.nTextSize = dateinfo[10:14]
        self.groupNum = dateinfo[14:16]
        self.lpszText = dateinfo[16:-2]
        self.phase1 = dateinfo[-5:-4]
        self.phase2 = dateinfo[-4:-3]
        self.phase3 = dateinfo[-3:-2]
        self.checkCode = dateinfo[-2:]
        self.singleLampInfo=[]
        mGroupInfo = multGroupInfo()
        mGroupInfo.ParsemultGroupInfo(self.lpszText,self.groupNum) #第二步分解到数组

        sGroupInfo = GroupInfo()
        NUM = int(self.groupNum, 16)
        for i in range(0,NUM):
            sGroupInfo.ParseGroupInfo(mGroupInfo.groupInfo[i])     #第三步对每个数组分解
            sLampInfo = singleLampInfo()
            for j in range(1,5):
                sLampInfo.ParseLampInfo(sGroupInfo.inGroupInfo1,self.srcAddress,sGroupInfo.groupID,j,sGroupInfo.envirbight,sGroupInfo.temperature,sGroupInfo.temperature1,sGroupInfo.temperature2)       #第四步分解4组组内信息
                self.singleLampInfo.append(sLampInfo)

        print '数量',len(self.singleLampInfo)
        print self.dstAddress
        print self.srcAddress
        print self.nCode
        print self.nTextSize
        print self.groupNum
        print self.phase1
        print self.phase2
        print self.phase3
        print self.checkCode

class multGroupInfo:         #多组单灯控制器的类
    groupInfo = []
    def ParsemultGroupInfo(self,lpszText,num):
        self.groupInfo=[]
        gNum = int(num, 16)
        print 'gNum=',gNum
        for i in range(0,gNum):
            self.groupInfo.append(lpszText[i*74+0:i*74+74])
            print(lpszText[i*74+0:i*74+74])

class GroupInfo:         #单灯控制器的类
    groupID=''
    inGroupInfo1 = ''
    inGroupInfo2 = ''
    inGroupInfo3 = ''
    inGroupInfo4 = ''
    envirbight = ''
    temperature = ''
    temperature1 = ''
    temperature2 = ''

    def __init__(self,groupID='',inGroupInfo1 = '',inGroupInfo2 = '',inGroupInfo3 = '',inGroupInfo4 = '',envirbight = '',temperature = '',temperature1 = '',temperature2 = '',phase1 = '',phase2 = '',phase3 = ''): 
        groupID=groupID
        self.inGroupInfo1 = inGroupInfo1  
        self.inGroupInfo2= inGroupInfo2  
        self.inGroupInfo3 = inGroupInfo3  
        self.inGroupInfo4 = inGroupInfo4  
        self.envirbight = envirbight  
        self.temperature = temperature
        self.temperature1 = temperature1
        self.temperature2 = temperature2  


    def ParseGroupInfo(self,lpszText):
        self.groupID=lpszText[0:2]
        self.inGroupInfo1 = lpszText[2:16]
        self.inGroupInfo2 = lpszText[16:30]
        self.inGroupInfo3 = lpszText[30:44]
        self.inGroupInfo4 = lpszText[44:58]
        self.envirbight = lpszText[58:62]
        temperature = lpszText[62:66]
        temperature1 = lpszText[66:70]
        temperature2 = lpszText[70:74]


        self.temperature = int(temperature, 16)/10.0  #数据处理16进制string转成10进制int
        self.temperature1 = int(temperature1, 16)/10.0
        self.temperature2 = int(temperature2, 16)/10.0

        # print lpszText[58:62]
        # print '亮度',self.envirbight
        # print lpszText[62:66]
        # print '温度1',self.temperature1
        # print lpszText[66:70]
        # print '温度2',self.temperature2
        # print lpszText[70:74]
        # print '温度3',self.temperature3
        
    



class singleLampInfo:     #小灯的类
    deviceID=''
    groupID = ''
    ingroupID=''
    wRateVoltage = ''
    wRateCurrent = ''
    wRatePowWatt = ''
    Luminance = ''
    envirbight=''
    temperature=''
    temperature1=''
    temperature2=''
    light_id=''

    def __init__(self,deviceID='',groupID = '',ingroupID='',wRateVoltage = '',wRateCurrent = '',wRatePowWatt = '',Luminance = '',envirbight='',temperature='',temperature1='',temperature2=''): 
        self.deviceID=deviceID
        self.groupID = groupID
        self.ingroupID=ingroupID  
        self.wRateVoltage = wRateVoltage  
        self.wRateCurrent = wRateCurrent
        self.wRatePowWatt = wRatePowWatt
        self.Luminance = Luminance 
        self.envirbight = envirbight
        self.temperature = temperature
        self.temperature1 = temperature1
        self.temperature2 = temperature2  

    def ParseLampInfo(self,lpszText,deviceID,groupID,ingroupID,groupenvirbight,grouptemperature,grouptemperature1,grouptemperature2):
        self.deviceID=deviceID
        self.groupID = groupID
        self.ingroupID=ingroupID
        self.wRateVoltage = lpszText[0:4]
        self.wRateCurrent = lpszText[4:8]
        self.wRatePowWatt = lpszText[8:12]
        self.Luminance = lpszText[12:14]
        self.envirbight = groupenvirbight
        self.temperature = grouptemperature
        self.temperature1 = grouptemperature1
        self.temperature2 = grouptemperature2

        # self.temperature1 = int(self.temperature1, 16)/10.0  #数据处理16进制string转成10进制int
        # self.temperature2 = int(self.temperature2, 16)/10.0
        # self.temperature3 = int(self.temperature3, 16)/10.0

        self.wRateVoltage = int(self.wRateVoltage, 16)/10.0   #数据处理16进制string转成10进制int
        self.wRateCurrent = int(self.wRateCurrent, 16)/100.0
        self.wRatePowWatt = int(self.wRatePowWatt, 16)/10.0
        self.Luminance = int(self.Luminance, 16)
        self.WriteInDb()
        self.CheckWarn()
        print "编号",self.deviceID,self.groupID,self.ingroupID
        print "电压",self.wRateVoltage
        print "电流",self.wRateCurrent
        print "功率",self.wRatePowWatt
        print "亮度",self.Luminance
        print '温度1',self.temperature
        print '温度2',self.temperature1
        print '温度3',self.temperature2
    def WriteInDb(self): 
        lightstatuslogs = session.query(Light).filter(Light.device_id==self.deviceID,Light.group_id==self.groupID,Light.in_group_id==self.ingroupID).all()
        # session.commit()
        # lightstatuslogs = session.query(Light).all()
        print lightstatuslogs
        if  lightstatuslogs:  
            self.light_id= lightstatuslogs[0].id
            lightstatuslog = Lightstatuslog(light_id=self.light_id, light_vol=self.wRateVoltage, light_cur=self.wRateCurrent, light_pow=self.wRatePowWatt, light_bright=self.Luminance, envi_bright=self.envirbight, temperature=self.temperature,temperature1=self.temperature1,temperature2=self.temperature2) 
            session.add(lightstatuslog)
            session.commit()

        else:    
            print None
            newlight=Light(device_id=self.deviceID,group_id=self.groupID,in_group_id=self.ingroupID)
            print newlight.id,newlight.device_id
            session.add(newlight)
            session.commit()
            print newlight.id,newlight.device_id    
            self.light_id= newlight.id 
            lightstatuslog = Lightstatuslog(light_id=self.light_id, light_vol=self.wRateVoltage, light_cur=self.wRateCurrent, light_pow=self.wRatePowWatt, light_bright=self.Luminance, envi_bright=self.envirbight, temperature=self.temperature,temperature1=self.temperature1,temperature2=self.temperature2) 
            session.add(lightstatuslog)
            session.commit()
    def CheckWarn(self):
        if(self.wRateVoltage>280):
            warninfo=Warninglog(light_id=self.light_id,status=0,info='电压过大')
            session.add(warninfo)
            session.commit()
        if(self.wRateVoltage<150):
            warninfo=Warninglog(light_id=self.light_id,status=0,info='电压过小') 
            session.add(warninfo)
            session.commit()
        if(self.wRateCurrent>15):
            warninfo=Warninglog(light_id=self.light_id,status=0,info='电流过大')
            session.add(warninfo)
            session.commit()
        if(self.wRateCurrent<1):
            warninfo=Warninglog(light_id=self.light_id,status=0,info="电流过小") 
            session.add(warninfo)
            session.commit() 
        if(self.wRatePowWatt>700):
            warninfo=Warninglog(light_id=self.light_id,status=0,info="功率过大")
            session.add(warninfo)
            session.commit()
        if(self.wRatePowWatt<50):
            warninfo=Warninglog(light_id=self.light_id,status=0,info="功率过小") 
            session.add(warninfo)
            session.commit()  
        if(self.temperature>100 or self.temperature1>100 or self.temperature2>100):
            warninfo=Warninglog(light_id=self.light_id,status=0,info="温度过高")
            session.add(warninfo)
            session.commit()
        if(self.temperature<0 or self.temperature1<0 or self.temperature2<0):
            warninfo=Warninglog(light_id=self.light_id,status=0,info="温度过低") 
            session.add(warninfo)
            session.commit()                   
def checksum(lpBuffer):
    nlen = len(lpBuffer)
    
    uChecktemp = 0
    
    for i in range(0,nlen):
        uChecktemp = uChecktemp^ord(lpBuffer[i])
        
    uCheckVal = (uChecktemp/16)*10 + uChecktemp%16
    if(len(str(uCheckVal))==2):
        return str(uCheckVal)
    else :
        return('0'+str(uCheckVal))
receivedata = DataInfo()        
#数据提取存储


                  #|                                                                     |               | |
# def WriteInDb() :
#         lightstatuslogs = session.query(Light).filter(Light.device_id=="1001",Light.group_id=="2000",Light.in_group_id=="2").all()
#         # session.commit()
#         # lightstatuslogs = session.query(Light).all()
#         print lightstatuslogs
#         if  lightstatuslogs:  
#             print '编号',lightstatuslogs[0].id

#         else:    
#             print None

#             newlight=Light(device_id="1235",group_id="12316",in_group_id="12316516")
#             print '编号',newlight.id,newlight.device_id
#             session.add(newlight)
#             session.commit()
#             print '编号',newlight.id,newlight.device_id

from sqlalchemy import create_engine
engine = create_engine('mysql://gaogandeng:123456@223.3.41.132:3306/gaogandeng', echo=False,connect_args={'charset':'utf8'})
        
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# warninfo=Warninglog(light_id=100,status=0,info='我wo') 
# session.add(warninfo)
# session.commit()    
# WriteInDb()
# dateContent = '0001000007120201089808AB01E16402000200030004640300020003000464040002000364000000010002000301089808AB01E1640200020003000464030002000300046404000200030004640000000111132'
# date = DateInfo()
# date.ParsedateInfo(dateContent)                            #第一步整体分解

# mGroupInfo = multGroupInfo()
# mGroupInfo.ParsemultGroupInfo(date.lpszText,date.groupNum) #第二步分解到数组

# sGroupInfo = GroupInfo()
# NUM = int(date.groupNum, 16)
# for i in range(0,NUM):
#     sGroupInfo.ParseGroupInfo(mGroupInfo.groupInfo[i])     #第三步对每个数组分解
#     sLampInfo = singleLampInfo()
#     sLampInfo.ParseLampInfo(sGroupInfo.inGroupInfo1,date.srcAddress,sGroupInfo.groupID,1,sGroupInfo.envirbight,sGroupInfo.temperature1,sGroupInfo.temperature2,sGroupInfo.temperature3)       #第四步分解4组组内信息
#     sLampInfo.ParseLampInfo(sGroupInfo.inGroupInfo2,date.srcAddress,sGroupInfo.groupID,2,sGroupInfo.envirbight,sGroupInfo.temperature1,sGroupInfo.temperature2,sGroupInfo.temperature3)
#     sLampInfo.ParseLampInfo(sGroupInfo.inGroupInfo3,date.srcAddress,sGroupInfo.groupID,3,sGroupInfo.envirbight,sGroupInfo.temperature1,sGroupInfo.temperature2,sGroupInfo.temperature3)
#     sLampInfo.ParseLampInfo(sGroupInfo.inGroupInfo4,date.srcAddress,sGroupInfo.groupID,4,sGroupInfo.envirbight,sGroupInfo.temperature1,sGroupInfo.temperature2,sGroupInfo.temperature3)

# print test2.inGroupInfo1
# print test2.inGroupInfo2
# print test2.inGroupInfo3
# print test2.inGroupInfo4

# test3 = singleLampInfo()
# test3.ParseLampInfo(test2.inGroupInfo1)
# print test3.groupID
# print test3.wRateVoltage
# print test3.wRateCurrent
# print test3.wRatePowWatt
# print test3.Luminance

# test.dstAddress
# test.srcAddress
# test.nCode
# test.nTextSize
# test.lpszText
# test.checkCode


# test2.envirbight
# test2.temperature1
# test2.temperature2
# test2.temperature3
# test2.phase1
# test2.phase2
# test2.phase3



# try:
#     conn=MySQLdb.connect(host='223.3.33.247',user='lilei',passwd='123456',port=3306)
#     cur=conn.cursor()
     
#     conn.select_db('highhandlelight')

#     count=cur.execute('select * from lampInfo1')
#     print 'there has %s rows record' % count
    

#     # results=cur.fetchmany(100)
#     # for r in results:
#     #     print r


#     sql = "insert into lampInfo1(DeviceID, GroupID, InGrpID) values(%s, %s, %s)"
#     tmp = (('111', 222, '333'),)
#     cur.executemany(sql, tmp)

#     conn.commit()
#     cur.close()
#     conn.close()
 
# except MySQLdb.Error,e:
#      print "Mysql Error %d: %s" % (e.args[0], e.args[1])


