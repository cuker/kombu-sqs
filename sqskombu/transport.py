from kombu.transport.SQS import Channel as BaseChannel, Transport as BaseTransport, CHARS_REPLACE_TABLE

class Channel(BaseChannel):
    def entity_name(self, name, table=CHARS_REPLACE_TABLE):
        name = super(Channel, self).entity_name(name, table)
        prefix = self.transport_options.get("prefix")
        if prefix:
            name = prefix + name
        return name

class SQSTransport(BaseTransport):
    Channel = Channel
    polling_interval = 30
#TODO how to make this configurable?

