#!/usr/bin/env python3

# 220042162 week2 ros task3

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import Gst, GstRtspServer, GLib  # type: ignore


def server():
    Gst.init(None)
    server = GstRtspServer.RTSPServer()
    factory = GstRtspServer.RTSPMediaFactory()

    # we use the default port 8554 of rtsp
    # to capture webcam feed we use v4l2src with /dev/video0 as the device file for my webcam
    factory.set_launch(
        "( v4l2src device=/dev/video0 ! videoconvert ! x264enc speed-preset=ultrafast tune=zerolatency ! rtph264pay name=pay0 pt=96 )"
    )

    factory.set_shared(True)
    mount_points = server.get_mount_points()
    mount_points.add_factory("/stream", factory)
    server.attach(None)

    loop = GLib.MainLoop()
    print("\n\n server running at rtsp://127.0.0.1:8554/stream\n\n")
    loop.run()


if __name__ == "__main__":
    server()
