#!/usr/bin/env python3

# 220042162 week2 ros task2

import rospy
from geometry_msgs.msg import Twist


def move(cmd):
    rospy.loginfo("turtle controller started")
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(1)

    if cmd not in ["A", "B", "C"]:
        rospy.logerr(
            "Invalid input\n  'A' : circle\n  'B' : square\n  'C' : outward spiral\n\n"
        )
        return

    if cmd == "A":
        print("\n moving in circle")
    elif cmd == "B":
        print("\n moving in square")
    elif cmd == "C":
        print("\n moving in outward spiral")

    vel = Twist()
    count = 0

    while not rospy.is_shutdown():
        # process the command
        # circle
        if cmd == "A":
            vel.linear.x = 2.0
            vel.angular.z = 1.0
        # square
        elif cmd == "B":
            # go forward
            if count % 4 == 0:
                vel.linear.x = 2.0
                vel.angular.z = 0.0
            # turn 90 degree (90 degree = 1.57 radian)
            elif count % 4 == 1:
                vel.linear.x = 0.0
                vel.angular.z = 1.57
            # go forward
            elif count % 4 == 2:
                vel.linear.x = 2.0
                vel.angular.z = 0.0
            # turn 90 degree (90 degree = 1.57 radian)
            elif count % 4 == 3:
                vel.linear.x = 0.0
                vel.angular.z = 1.57
        # outward spiral
        elif cmd == "C":
            # the idea is to slowly increase the radius while keeping
            # while keeping angular velocity same, so it will move outward
            # while moving in a circle creating an outward spiral
            vel.linear.x = 1.0 + count * 0.07
            vel.angular.z = 1.0

            if count == 100:
                count = 0

        # publish it
        pub.publish(vel)
        count = count + 1
        rate.sleep()


if __name__ == "__main__":
    try:
        # initialize the node before fetching the parameter
        # otherwise it will only fetch the default value
        rospy.init_node("turtle_controller")
        cmd = str(rospy.get_param("~cmd", "A")).upper()
        move(cmd)
    except rospy.ROSInterruptException:
        pass
