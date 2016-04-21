from device_tracker import DeviceTracker
import time

devices_macs = ['38:aa:3c:47:6f:3a']

device_tracker = DeviceTracker(network_prefix = '192.168.43.')

device_tracker.start()

for mac in devices_macs:
	device_tracker.add_device(mac)
