import argparse

PORT = 4242
YPR_PORT = 9000

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="localhost",
    help="udp server hostname")
parser.add_argument("-p", "--port", type=int, default=4242,
    help="udp server port")
parser.add_argument("-v", "--video", action="store_true",
    help="show a live video preview of the tracking results")
parser.add_argument("--verbose", action="store_true",
    help="enable verbose ouput")
parser.add_argument("-c", "--client", choices=["udp", "osc", "ypr"], required=True,
    help="choose client implementation")

args = parser.parse_args()

from facemesh_tracker import FaceMeshTracker
from facemesh_preview import FaceMeshPreview

if args.client == "udp":
    from client.udp import UDPServer
    ClientImplementation = UDPServer
elif args.client in ["osc", "ypr"]:
    from client.osc import OSCServer
    ClientImplementation = OSCServer

# set default YPR port
if args.client == "ypr" and args.port == PORT:
    args.port = YPR_PORT

server = ClientImplementation(args.host, args.port, args.client)
print("INFO: Sending tracking data to {}:{} via {}".format(args.host, args.port, args.client))

if args.video:
    preview = FaceMeshPreview()
else:
    preview = None

with FaceMeshTracker(server, preview) as tracker:
    try:
        print("INFO: Tracker is starting")
        tracker.start()
    except KeyboardInterrupt:
        pass
    print("INFO: Closing tracker.")
