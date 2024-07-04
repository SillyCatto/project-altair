#!/usr/bin/env python3

# 220042162 week2 ros task3

import rospy
from sensor_msgs.msg import Image
import cv2

# cv_bridge to convert between OpenCV image and ROS message
from cv_bridge import CvBridge


def stream_pub():
    rospy.init_node("video_publisher", anonymous=True)
    rospy.loginfo("video publisher node started")

    pub = rospy.Publisher("video_stream", Image, queue_size=10)
    rate = rospy.Rate(10)

    # set opencv to capture video stream from rtsp server
    cap = cv2.VideoCapture("rtsp://127.0.0.1:8554/stream")
    bridge = CvBridge()

    while not rospy.is_shutdown():
        # read video stream
        ret, frame = cap.read()
        # check if there is video data
        if ret is True:
            # convert cv2 image to ros message
            # we use bgr8 encoding as mentioned in ros wiki
            image_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            pub.publish(image_msg)
            rospy.loginfo("publishing video stream")
        rate.sleep()

    cap.release()


if __name__ == "__main__":
    try:
        stream_pub()
    except rospy.ROSInterruptException:
        pass
