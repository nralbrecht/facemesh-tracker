import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, default="localhost",
    help="udp server hostname")
parser.add_argument("-p", "--port", type=int, default=4242,
    help="udp server port")
parser.add_argument("--preview", action="store_true",
    help="show a preview of the tracking points")
parser.add_argument("-v", "--verbose", action="store_true",
    help="enable verbose ouput")
parser.add_argument("-s", "--server", choices=["opentrack_udp", "tracknoir_udp"], required=True,
    help="choose server implementation")

args = parser.parse_args()

from facemesh_tracker import FaceMeshTracker
from facemesh_preview import FaceMeshPreview

if args.server == "opentrack_udp":
    from server.opentrack_udp import OpenTrackUDPServer
    Server = OpenTrackUDPServer
elif args.server == "tracknoir_udp":
    from server.tracknoir_udp import TrackNoIRUDPServer
    Server = TrackNoIRUDPServer

server = Server(args.host, args.port)
print("INFO: Sending tracking data to {}:{}".format(args.host, args.port))

if args.preview:
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
