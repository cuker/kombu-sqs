from Queue import Empty
from kombu.transport import virtual

from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message
from anyjson import serialize, deserialize

import socket

class Channel(virtual.Channel):
    def normalize_queue_name(self, queue):
        """
        A queue name must conform to the following::
            
            Can only include alphanumeric characters, hyphens, or underscores. 1 to 80 in length
        
        This function aims to map a non-standard name to one that is acceptable for sqs
        """
        return queue.replace('.', '_')
    
    def get_or_create_queue(self, queue):
        return self.client.create_queue(self.normalize_queue_name(queue))

    def _new_queue(self, queue, **kwargs):
        self.get_or_create_queue(queue)

    def _put(self, queue, message, **kwargs):
        q = self.get_or_create_queue(queue)
        m = Message()
        m.set_body(serialize(message))
        q.write(m)

    def _get(self, queue):
        q = self.get_or_create_queue(queue)
        m = q.read()
        if m:
            msg = deserialize(m.get_body())
            q.delete_message(m)
            return msg
        raise Empty()

    def _size(self, queue):
        q = self.get_or_create_queue(queue)
        return q.count()

    def _purge(self, queue):
        q = self.get_or_create_queue(queue)
        count = q.count()
        q.clear()
        return count #CONSIDER this number may not be accurate
    
    def _open(self):
        conninfo = self.connection.client
        return SQSConnection(conninfo.userid, conninfo.password)
    
    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = self._open()
        return self._client


class SQSTransport(virtual.Transport):
    Channel = Channel

    connection_errors = (socket.error)
    channel_errors = ()
