from pythonosc.udp_client import SimpleUDPClient


# http://facetracknoir.sourceforge.net/Trackers/OSC.htm

class OSCServer:
    def __init__(self, host, port):
        self.client = SimpleUDPClient(host, port)

    def send_update(self, position, rotation):
        # /gyrosc/gyro {pitch, roll, yaw}
        client.send_message("/gyrosc/gyro", rotation.astype(float))

        # /gyrosc/xyz {x, y, z}
        client.send_message("/gyrosc/xyz", position.astype(float))
