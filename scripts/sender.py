#!/usr/bin/env python

__author__ = 'flier'

import argparse

import rospy
import leap_interface
from leap_motion.msg import leap
from leap_motion.msg import leapros

FREQUENCY_ROSTOPIC_DEFAULT = 0.01
NODENAME = 'leap_pub'
PARAMNAME_FREQ = 'freq'
PARAMNAME_FREQ_ENTIRE = '/' + NODENAME + '/' + PARAMNAME_FREQ

def sender():
    # This method publishes the data defined in leapros.msg to /leapmotion/data
   
    rospy.loginfo("Parameter set on server: PARAMNAME_FREQ={}".format(rospy.get_param(PARAMNAME_FREQ_ENTIRE, FREQUENCY_ROSTOPIC_DEFAULT)))

    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    pub_ros   = rospy.Publisher('leapmotion/data',leapros, queue_size=2)
    rospy.init_node(NODENAME)
    # rate = rospy.Rate(5) # 5hz (Does nothing)

    while not rospy.is_shutdown():
        hand_direction_   = li.get_hand_direction()
        hand_normal_      = li.get_hand_normal()
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()

        msg = leapros()
        msg.direction.x = hand_direction_[0]
        msg.direction.y = hand_direction_[1]
        msg.direction.z = hand_direction_[2]
        msg.normal.x = hand_normal_[0]
        msg.normal.y = hand_normal_[1]
        msg.normal.z = hand_normal_[2]
        msg.palmpos.x = hand_palm_pos_[0]
        msg.palmpos.y = hand_palm_pos_[1]
        msg.palmpos.z = hand_palm_pos_[2]
        msg.ypr.x = hand_yaw_
        msg.ypr.y = hand_pitch_
        msg.ypr.z = hand_roll_

        pub_ros.publish(msg)
	# rate.sleep() # (Does Nothing)
        rospy.sleep(rospy.get_param(PARAMNAME_FREQ_ENTIRE, FREQUENCY_ROSTOPIC_DEFAULT))


if __name__ == '__main__':
    try:
        sender()
    except rospy.ROSInterruptException:
        pass
