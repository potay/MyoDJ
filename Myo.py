# Copyright (C) 2014  Niklas Rosenstein
# All rights reserved.

import myo
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
        pass

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        pass

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
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

