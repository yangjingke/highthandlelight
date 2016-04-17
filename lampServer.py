from customProtocol import LampProtocol
from twisted.python import log
from HighHandleLightmysql import receivedata,checksum
COMMAND_TASK_TIME = 1
STATUS_TASK_TIME = 60

g_ip_socket_map = {}
g_dev_ip_map = {}


class LampServerHandle(LampProtocol):

    def getIPKey(self):
        host = self.transport.getPeer().host
        port = self.transport.getPeer().port
        return '%s:%s' % (host, port)

    def connectionMade(self):
        global g_ip_socket_map
        ip_key = self.getIPKey()
        print "recive one connection from %s" % ip_key
        g_ip_socket_map[ip_key] = self
      
        # self.sendString('00000000000000')


    def connectionLost(self, reason):
        global g_ip_socket_map
        ip_key = self.getIPKey()
        print "lose one connection from %s" % ip_key
        del g_ip_socket_map[ip_key]


    def stringReceived(self, data):
        print 'stringReceived: ' + data
        log.msg('received   '+data)
        try:
            
            if len(data)>16:
                print 'data   '+data
                print data[14:-2]
                print checksum(data[14:-2]),data[-2:]
                print checksum(data[14:-2])==data[-2:]
                if(checksum(data[14:-2])==data[-2:]):
                    fun_num = int(data[8:10],16)
                    print 'fun_num'+str(fun_num)
                    log.msg(fun_num)
                    if(07 == fun_num):                     
                        dev_num = int(data[4:8],16)
                        print "dev_num:"+str(dev_num)
                        ip = self.getIPKey()
                        global g_dev_ip_map
                        g_dev_ip_map[dev_num]=ip
                        print data
                        receivedata.ParsedateInfo(data) 
                        
                    # mysql handle
        except Exception,e:
            log.err(e)

        # self.sendString('command')


