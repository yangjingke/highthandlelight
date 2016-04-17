from twisted.internet.protocol import Protocol

class LampProtocol(Protocol):
    _buffer = ""

    def dataReceived(self, data):
        self._buffer = self._buffer + data
        while True:
            if len(self._buffer) > 0:
                end_index = self._buffer.find('$')
                if end_index > 0:
                    begin_index = self._buffer.find('@')
                    if begin_index >= 0:
                        packet = self._buffer[begin_index+1:end_index]
                        self.stringReceived(packet)
                    self._buffer = self._buffer[end_index+1:]
                    
                else:
                    break
            else:
                break

    def stringReceived(self, data):
        raise NotImplementedError

    def sendString(self, string):
        self.transport.write('@'+string+'$')