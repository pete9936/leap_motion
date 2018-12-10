#################################################################################
# Altered LEAP example by Florian Lier, you need to have the LEAP SDK installed #
# for this to work properly ;)                                                  #
# This interface provides access to the LEAP MOTION hardware, you will need to  #
# have the official LEAP MOTION SDK installed in order to load the shared       #
# provided with the SDK.                                                        #
#################################################################################

""" For backwards compatibility with the old driver files
                Will be DELETED in the future               """

import sys
import time
# Set (append) your PYTHONPATH properly, or just fill in the location of your LEAP
# SDK folder, e.g., $HOME/LeapSDK/lib where the Leap.py lives and /LeapSDK/lib/x64 or
# x86 where the *.so files reside.

# Below, you can see the "dirty" version - NOT RECOMMENDED!


sys.path.append("/home/pete9936/catkin_ws/src/leap_motion/LeapSDK/lib")
sys.path.append("/home/pete9936/catkin_ws/src/leap_motion/LeapSDK/lib/x64")
import threading
import Leap
from Leap import KeyTapGesture, ScreenTapGesture, SwipeGesture


class LeapInterface(Leap.Listener):
    def on_init(self, controller):
        # These variables as probably not thread safe
        # TODO: Make thread safe ;)
        self.hand           = [0,0,0]
        self.right_hand = False
        self.left_hand = False
        self.hand_direction = [0,0,0]
        self.hand_normal    = [0,0,0]
        self.hand_palm_pos  = [0,0,0]
        self.hand_pitch     = 0.0
        self.hand_yaw       = 0.0
        self.hand_roll      = 0.0
	self.hands          = 0
        print "Initialized Leap Motion Device"

    def on_connect(self, controller):
        print "Connected to Leap Motion Controller"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected Leap Motion"

    def on_exit(self, controller):
        print "Exited Leap Motion Controller"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()


	print "Frame id: %d, timestamp: %d, hands: %d, gestures: %d" % (frame.id, frame.timestamp, len(frame.hands), len(frame.gestures()))

        if not frame.hands.is_empty: #recently changed in API
            # Get the first hand

            #we are seeking one left and one right hands
            there_is_right_hand=False
            there_is_left_hand=False

            for hand in frame.hands:

                if hand.is_right:
                    there_is_right_hand=True
                    self.right_hand=hand
                elif hand.is_left:
                    there_is_left_hand=True
                    self.left_hand=hand

            if not there_is_right_hand:
                self.right_hand=False

            if not there_is_left_hand:
                self.left_hand=False

            self.hand = frame.hands[0] #old way


            # Get the hand's normal vector and direction
            normal = self.hand.palm_normal
            direction = self.hand.direction
            pos = self.hand.palm_position

            self.hand_direction[0] = direction.x
            self.hand_direction[1] = direction.y
            self.hand_direction[2] = direction.z
            self.hand_normal[0]    = normal.x
            self.hand_normal[1]    = normal.y
            self.hand_normal[2]    = normal.z
            self.hand_palm_pos[0]  = pos.x
            self.hand_palm_pos[1]  = pos.y
            self.hand_palm_pos[2]  = pos.z
            self.hand_pitch        = direction.pitch * Leap.RAD_TO_DEG
            self.hand_yaw          = normal.yaw * Leap.RAD_TO_DEG
            self.hand_roll         = direction.roll * Leap.RAD_TO_DEG
	    self.hands             = len(frame.hands)

            # Calculate the hand's pitch, roll, and yaw angles
            print "Hand pitch: %3.2f degrees, roll: %3.2f degrees, yaw: %3.2f degrees" % (self.hand_pitch, self.hand_roll, self.hand_yaw)

	    print "Hand Direction: x-pos: %3.2f, y-pos: %3.2f, z-pos: %3.2f" % (self.hand_palm_pos[0], self.hand_palm_pos[1], self.hand_palm_pos[2])

	    # Write to a .txt file
	    # f= open("Hand_Directions.txt","w+")
            # f=open("Hand_Info.txt","a+")
            # f.write("\n" + "Hand_Ori (deg):\t pitch: %3.2f, roll: %3.2f, yaw: %3.2f" % (self.hand_pitch, self.hand_roll, self.hand_yaw))
	    # f.write("\n" + "Hand Dir (mm):\t x-pos: %3.2f, y-pos: %3.2f, z-pos: %3.2f" % (self.hand_palm_pos[0], self.hand_palm_pos[1], self.hand_palm_pos[2]))
            # f.close()

            
            # Gestures
            for gesture in frame.gestures():

                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    print "Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                            gesture.id, self.state_string(gesture.state),
                            swipe.position, swipe.direction, swipe.speed)

                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    keytap = KeyTapGesture(gesture)
                    print "Key Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_string(gesture.state),
                            keytap.position, keytap.direction )


        if not (frame.hands.empty and frame.gestures().empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
    

    def get_hand_direction(self):
        return self.hand_direction

    def get_hand_normal(self):
        return self.hand_normal

    def get_hand_palmpos(self):
        return self.hand_palm_pos

    def get_hand_yaw(self):
        return self.hand_yaw

    def get_hand_pitch(self):
        return self.hand_pitch

    def get_hand_roll(self):
        return self.hand_roll

    def get_hands(self):
	return self.hands



class Runner(threading.Thread):

    def __init__(self,arg=None):
        threading.Thread.__init__(self)
        self.arg=arg
        self.listener = LeapInterface()
        self.controller = Leap.Controller()
        self.controller.add_listener(self.listener)

    def __del__(self):
        self.controller.remove_listener(self.listener)

    def get_hand_direction(self):
        return self.listener.get_hand_direction()

    def get_hand_normal(self):
        return self.listener.get_hand_normal()

    def get_hand_palmpos(self):
        return self.listener.get_hand_palmpos()

    def get_hand_roll(self):
        return self.listener.get_hand_roll()

    def get_hand_pitch(self):
        return self.listener.get_hand_pitch()

    def get_hand_yaw(self):
        return self.listener.get_hand_yaw()

    def get_hands(self):
	return self.listener.get_hands()


    def run (self):
        while True:
            # Save some CPU time
            time.sleep(0.001)

