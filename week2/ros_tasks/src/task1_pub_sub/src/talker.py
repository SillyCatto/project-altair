#!/usr/bin/env python3

# 220042162 week2 ros task1

import rospy
from std_msgs.msg import String


def main():
    rospy.init_node("talker")
    rospy.loginfo("talker node started")

    pub = rospy.Publisher("chatter", String, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        msg = "Hello World %s" % rospy.get_time()
        rospy.loginfo(msg)
        pub.publish(msg)

        rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
