#!/usr/bin/env python3

# 220042162 week2 ros task1

import rospy
from std_msgs.msg import String


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " I heard:  %s", data.data)


def main():
    rospy.init_node("listener")
    rospy.loginfo("listener node started")
    rospy.Subscriber("chatter", String, callback)

    rospy.spin()


if __name__ == "__main__":
    main()
