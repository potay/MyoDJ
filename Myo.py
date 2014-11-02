# Copyright (C) 2014  Niklas Rosenstein
# All rights reserved.

import myo, math
# from Quaternion import Quat
# import Quaternion
myo.init('myo/myo.framework', False)

from myo.six import print_

class Listener(myo.DeviceListener):
    def on_connect(self, myo, timestamp):
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.request_rssi()

    def on_rssi(self, myo, timestamp, rssi):
        print_("RSSI:", rssi)

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        print_('on_pair')

    def on_disconnect(self, myo, timestamp):
        print_('on_disconnect')

    def on_pose(self, myo, timestamp, pose):
        print_('on_pose', pose)

    def on_orientation_data(self, myo, timestamp, orientation):
        # self.quat = Quat(Quaternion.normalize(orientation))
        # quat = self.quat
        # # Calculate Euler angles (roll, pitch, and yaw) from the unit quaternion.
        # self.roll = math.atan2(2.0 * (quat.q[0] * quat.q[1] + quat.q[2] * quat.q[3]),
        #                    1.0 - 2.0 * (quat.q[1] * quat.q[1] + quat.q[2] * quat.q[2]))
        # self.pitch = math.asin(max(-1.0, min(1.0, 2.0 * (quat.q[0] * quat.q[2] - quat.q[3] * quat.q[1]))))
        # self.yaw = math.atan2(2.0 * (quat.q[0] * quat.q[3] + quat.q[1] * quat.q[2]),
        #                 1.0 - 2.0 * (quat.q[2] * quat.q [2] + quat.q[3] * quat.q[3]))
        # # Convert the floating point angles in radians to a scale from 0 to 20.
        # self.roll_w = int((self.roll + (math.pi)/(math.pi * 2.0) * 20))
        # self.pitch_w = int((self.pitch + (math.pi)/2.0)/math.pi * 20)
        # self.yaw_w = int((self.yaw + (math.pi)/(math.pi) * 2.0) * 20)
        pass

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        # print_('on_accelerometor', acceleration)
        pass

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        # print_('on_gyroscope', gyroscope)
        pass

class MyoHub(object):

    def __init__(self, listener = None):
        self.hub = myo.Hub()
        if listener == None:
            self.listener = Listener()
        else:
            self.listener = listener

    def run(self):
        self.hub.run(1000, self.listener)

        try:
            while self.hub.running:
                myo.time.sleep(0.2)
        except KeyboardInterrupt:
            print_("Quitting ...")
            self.hub.stop(True)

