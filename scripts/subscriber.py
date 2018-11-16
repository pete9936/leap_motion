#!/usr/bin/env python

""" For backwards compatibility with the old driver files
                Will be DELETED in the future               """

__author__ = 'flier'

import rospy
# from leap_motion.msg import leap
from leap_motion.msg import leapros

# Native datatypes, I've heard this is bad practice, use the geometry messages instead.

# Callback of the ROS subscriber, just print the received data.
def callback_ros(data):
    rospy.loginfo(rospy.get_name() + ": Leap ROS Data %s" % data)


# Our listener aka subscriber. Listens to: leapmotion/data
def listener():
    rospy.init_node('leap_sub', anonymous=True)
    rospy.Subscriber("leapmotion/data", leapros, callback_ros)
    rospy.spin()


if __name__ == '__main__':
    listener()
