#coding=utf-8
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet import task
from twisted.python import log
from twisted.python import logfile

from lampServer import LampServerHandle
from lampServer import g_ip_socket_map
from lampServer import g_dev_ip_map
from HighHandleLightmysql import session,checksum
import redis
import time
from db import Lightcontrollog,Light
redis_con=redis.StrictRedis(host='223.3.41.132',db=0 )
timely_task_list='gaogandeng:timelytask:list'
timer_task_list='gaogandeng:timertask:list'
timer_task_hash='gaogandeng:timertask:hash'

COMMAND_TASK_TIME = 20
STATUS_TASK_TIME = 4
TIMER_TASK_TIME=1
TIMELY_TASK_TIME=1
timer_task={}

def getStatusTask():
    
     # print "sendCommandTask"
    
    for dev, ip in g_dev_ip_map.items():
        print dev,ip
    # print "getStatusTask"
    # for key, client in g_ip_socket_map.items():
    #     print key


def sendCommandTask():  #每分钟发送一次查询命令
    # print "sendCommandTask"
    for key, client in g_ip_socket_map.items():
        print key
        # print('@00000000070000$')  
        client.transport.write('@0000000007000000$')

def sendTimelyTask(): #及时任务
    task = redis_con.lpop(timely_task_list)
    print '任务',task    
    if task:   #存在任务
        print '任务',task
        if len(task)>5: #长度大于5  
            dev=int(task[1:5],16)
            print '设备',dev

            if dev==0:
                for key, client in g_ip_socket_map.items():
                    client.transport.write(task)    
            else: 
                print '设备是否存在',dev in g_dev_ip_map
                if dev in g_dev_ip_map:  #向对应集中控制器发送
                    print 'socket是否存在',g_dev_ip_map[dev] in g_ip_socket_map
                    if g_dev_ip_map[dev] in g_ip_socket_map:
                        print '任务命令如下：',task
                        print str(task)

                        g_ip_socket_map[g_dev_ip_map[dev]].transport.write(task)

        # while task
        #     task = redis_con.rpop(task_queue)
        #     print task
    
def sendTimerTask():     
    print'当前时间',(int(time.time())) ,time.gmtime()      
    tasktime = redis_con.lindex(timer_task_list,0) #查询第一个元素时间值
    print '任务时间',tasktime
    if  tasktime:
        if int(tasktime)<=int(time.time()):  #如果已到时间
            timertask=redis_con.lpop(timer_task_list)    
            print timertask,int(time.time()),time.gmtime() 
            cmdexist=redis_con.hexists(timer_task_hash, timertask) #取出对应hash表对应的
            print cmdexist
            if cmdexist:
                cmd=redis_con.hget(timer_task_hash, timertask)
                print cmd
                if cmd:
                    cmdid=cmd.split(';')
                    for item in cmdid:
                        print item
                        lightcmd=session.query(Lightcontrollog).filter(Lightcontrollog.id==item).all() #根据任务号选取
                        if lightcmd:
                            print lightcmd[0].light_id,lightcmd[0].bright,lightcmd[0].status   #输出该任务号下的灯的编号以及状态亮度
                            if lightcmd[0].status==0:
                                light=session.query(Light).filter(Light.id==lightcmd[0].light_id).all()
                                print light
                                if light:
                                    id=int(light[0].device_id,16)
                                    print '设备是否存在',id in g_dev_ip_map
                                    if id in g_dev_ip_map:
                                        print 'socket是否存在',g_dev_ip_map[id] in g_ip_socket_map                                       
                                        if g_dev_ip_map[id] in g_ip_socket_map:
                                            if timer_task.has_key(id):
                                                timer_task[id]=timer_task[id]+str(light[0].group_id)+str(light[0].in_group_id)+'{0:x}'.format(lightcmd[0].bright).zfill(2)
                                                print timer_task[id]
                                            else:
                                                timer_task[id]=str(light[0].group_id)+str(light[0].in_group_id)+'{0:x}'.format(lightcmd[0].bright).zfill(2)
                                            # cmdword='@'+str(light[0].device_id)+'0000040005'+str(light[0].group_id)+str(light[0].in_group_id)+'{0:x}'.format(lightcmd[0].bright)+checksum(str(light[0].group_id)+str(light[0].in_group_id)+'{0:x}'.format(lightcmd[0].bright))+'$'
                                            
                                            # g_ip_socket_map[g_dev_ip_map[id]].transport.write(cmdword)
                                            # # time.sleep(2)
                                            # print checksum(str(light[0].group_id)+str(light[0].in_group_id)+'{0:x}'.format(lightcmd[0].bright))
                                            # print '控制命令',cmdword
                                            # print light[0].device_id,light[0].group_id,light[0].in_group_id    
                                session.query(Lightcontrollog).filter(Lightcontrollog.id==item).update({Lightcontrollog.status:1})
                                session.commit()
                                print 'change'
                    for devid ,task in timer_task.items():
                        if devid in g_dev_ip_map:
                            print 'socket是否存在',g_dev_ip_map[devid] in g_ip_socket_map                                       
                            if g_dev_ip_map[devid] in g_ip_socket_map:
                                for i in xrange(0,len(task),100):
                                    length='{0:x}'.format(len(task[i:i+100]))
                                    cmd='@'+str(light[0].device_id)+'000004'+length.zfill(4)+task[i:i+100]+checksum(task[i:i+100])+'$'
                                    print '控制命令',cmd
                                    g_ip_socket_map[g_dev_ip_map[devid]].transport.write(cmd)
                                    # g_ip_socket_map[g_dev_ip_map[devid]].transport.write('@00000000060023ds0f2sdsdf000000$')
                                    time.sleep(5)
                    timer_task.clear()


                                            # print 'gesdhis',light[0].device_id,light[0].group_id,light[0].in_group_id    
                                    
                                          
                                    
                                    # lightcmd[0].status=1    
                    redis_con.hdel(timer_task_hash,timertask)


    # print task
    # while task:
    #     task = redis_con.rpop(timer_task_list)
    #     print task    

def registerTimerTask():
    command_task = task.LoopingCall(sendCommandTask)
    command_task.start(COMMAND_TASK_TIME)

    status_task = task.LoopingCall(getStatusTask)
    status_task.start(STATUS_TASK_TIME)

    timer_task=task.LoopingCall(sendTimerTask)
    timer_task.start(TIMER_TASK_TIME)

    timely_task=task.LoopingCall(sendTimelyTask)
    timely_task.start(TIMELY_TASK_TIME)

def main():
    registerTimerTask()
    factory = Factory()
    factory.protocol = LampServerHandle
    f=logfile.DailyLogFile("twisted.log","log/")
    log.startLogging(f,setStdout=0)
    
    
    reactor.listenTCP(10000, factory)
    reactor.run()

if __name__ == '__main__':
    main()

        

            
         