from kombu.transport import virtual
from kombu.transport.SQS import Channel as BaseChannel, Transport as BaseTransport, CHARS_REPLACE_TABLE

class Channel(BaseChannel):
    def entity_name(self, name, table=CHARS_REPLACE_TABLE):
        try:
            name = super(Channel, self).entity_name(name, table)
        except TypeError:
            name = name.translate(table)
        prefix = self.transport_options.get("prefix")
        if prefix:
            name = prefix + name
        return name
    
    def _delete(self, queue, *args):
        """delete queue by name."""
        self._queue_cache.pop(queue, None)
        #self.table.queue_delete(queue)
        virtual.Channel._delete(self, queue)
    
    def _get(self, queue):
        super(Channel, self)._get(queue)
    
    def close(self):
        virtual.Channel.close(self)
        for conn in (self._sqs, self._sdb):
            if conn:
                try:
                    conn.close()
                except AttributeError, exc:  # FIXME ???
                    pass
                    #if "can't set attribute" not in str(exc):
                    #    raise

class SQSTransport(BaseTransport):
    Channel = Channel
    polling_interval = 30
#TODO how to make this configurable?

