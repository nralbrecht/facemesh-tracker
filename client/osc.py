from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_message_builder import OscMessageBuilder


class OSCServer:
    def __init__(self, host, port, client_type):
        self.client = SimpleUDPClient(host, port)
        self.client_type = client_type

    def send_update(self, position, rotation):
        if self.client_type == 'ypr': 
            # https://plugins.iem.at/docs/osc/#scenerotator
            self.client.send_message("/ypr", rotation)
        else:
            # http://facetracknoir.sourceforge.net/Trackers/OSC.htm
            # /gyrosc/gyro {yaw, pitch, roll}
            self.client.send_message("/gyrosc/gyro", rotation / 100)
            # /gyrosc/xyz {x, y, z}
            self.client.send_message("/gyrosc/xyz", position)
