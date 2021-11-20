import struct
import socket

class OpenTrackUDPServer:
    def __init__(self, host, port):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_update(self, position, rotation):
        # struct THeadPoseData {
        #     double x, y, z, yaw, pitch, roll;
        # };
        self.sock.sendto(struct.pack("<dddddd", *position, *rotation), self.server_address)
