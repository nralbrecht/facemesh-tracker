from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_message_builder import OscMessageBuilder



# http://facetracknoir.sourceforge.net/Trackers/OSC.htm

class OSCServer:
    def __init__(self, host, port):
        self.client = SimpleUDPClient(host, port)

    def send_update(self, position, rotation):
        # /gyrosc/gyro {pitch, roll, yaw}
        self.client.send_message("/gyrosc/gyro", rotation / 100)

        # /gyrosc/xyz {x, y, z}
        self.client.send_message("/gyrosc/xyz", position)
