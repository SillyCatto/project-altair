#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

# 220042162 week2 ros task3


def callback(data):
    bridge = CvBridge()
    rospy.loginfo("receiving video stream")

    # convert ros message to cv2
    frame = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("video feed from rtsp", frame)

    cv2.waitKey(1)


def stream_sub():
    rospy.init_node("video_subscriber")
    rospy.loginfo("video subscriber node started")
    rospy.Subscriber("video_stream", Image, callback)
    rospy.spin()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    stream_sub()
