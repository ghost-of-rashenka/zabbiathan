# Trapper implementation.
import json
import socket
import time

# Header configurations, per Zabbix documentation:
# https://www.zabbix.com/documentation/4.0/manual/appendix/protocols/header_datalen

# <PROTOCOL> - "ZBXD" (4 bytes).
# <FLAGS> -the protocol flags, (1 byte). 0x01 - Zabbix communications protocol, 0x02 - compression).
# <DATALEN> - data length (4 bytes). 1 will be formatted as 01/00/00/00 (four bytes, 32 bit number in little-endian
# format).
# <RESERVED> - reserved for protocol extensions (4 bytes).
#
# When compression is enabled (0x02 flag) the <RESERVED> bytes contains uncompressed data size, 32 bit number in little-
# endian format.
#
# To not exhaust memory (potentially) Zabbix protocol is limited to accept only 128MB in one connection.
ZBX_PROTOCOL = b"ZBXD"
ZBX_FLAGS = b"\1"


def datalen(trappers):
    """
    The byte length of the Trapper Metrics in a single message.

    :param trapper:
    :return:
    """
    pass


class Trapper:
    """A single Zabbix Trapper Metric for a host monitored by Zabbix."""

    def __init__(self, host=socket.gethostname(), key="", value="", clock=None):
        """
        A trapper metric to be sent to the Zabbix Server as identified by host and key:value pair.

        :param host: The host that the metric is for.
        :type host: str
        :param key: The trapper key as specified on the Zabbix server.
        :type key: str
        :param value: The trapper value.
        :param clock: The epoch time for the trapper. Current time if `True`.
        :type clock: int
        """
        self._host = host
        self._key = key
        self._value = value
        self._clock = None
        if clock is not None:
            if clock is True:
                self._clock = int(time.time())
            elif clock is False:
                self._clock = None
            else:
                try:
                    self._clock = int(clock)
                except TypeError as e:
                    raise ValueError("Unable to determine clock value from {}".format(clock)) from e

    def __repr__(self):
        return "{cls}(host={h!r}, key={k!r}, value={v!r}, clock={c!r})".format(cls=self.__class__.__name__,
                                                                               h=self._host,
                                                                               k=self._key,
                                                                               v=self._value,
                                                                               c=self._clock)

    @property
    def host(self):
        return self._host

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def clock(self):
        return self._clock

    def json(self):
        """
        The Trapper as a str of JSON.

        :return: the JSON representation of the Trapper.
        :rtype: str
        """
        trap_dict = {
            "host": self.host,
            "key": self.key,
            "value": self.value
        }
        if self.clock:
            trap_dict.update({"clock": self.clock})

        return json.dumps(trap_dict)
