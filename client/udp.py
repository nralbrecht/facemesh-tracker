import struct
import socket


# http://facetracknoir.sourceforge.net/Trackers/UDP.htm

class UDPServer:
    def __init__(self, host, port, client_type):
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.frame_number = 0

    def send_update(self, position, rotation):
        # struct THeadPoseData {
        #     double x, y, z, yaw, pitch, roll;
        #     long frame_number;
        # };
        self.sock.sendto(struct.pack("<ddddddl", *position, *rotation, self.frame_number), self.server_address)
        self.frame_number += 1
