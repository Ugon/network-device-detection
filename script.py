from scapy.all import *
from copy import deepcopy
from threading import Thread, Timer
import datetime

#############################################################
########################PARAMETERS###########################
#############################################################
devices_macs = ['38:aa:3c:47:6f:3a']

network_prefix = '192.168.1.'
start_pinging_after = datetime.timedelta(seconds=5)
connection_lost_after = datetime.timedelta(seconds=10)

deamon_period_seconds = 1
full_network_search_period_seconds = 30

def on_connected(mac):
	print '#############################################################'
	print '########## [' + mac       + '] connected ####################'
	print '#############################################################'

def on_lost(mac):
	print '#############################################################'
	print '########## [' + mac       + '] disconnected #################'
	print '#############################################################'

#############################################################
#############################################################
#############################################################%


def log(mac=None, msg=None):
	if mac is not None:
		print datetime.datetime.now().isoformat(' ')[0:19] + ' [' + mac + '] ' + msg
	else:
		print datetime.datetime.now().isoformat(' ')[0:19] + ' ' + msg


class DeviceCollection:
	def __init__(self):
		self.devices = {}

	def add_device(self, mac):
		log(mac, 'added device')
		self.devices[mac] = {'ip': None, 'lastActive': datetime.datetime(year=1, month=1, day=1), 'detected': False}
	
	def remove_device(self, mac):
		log(mac, 'removed device')
		del self.devices[mac]

	def contain_mac(self, mac):
		return mac in self.devices

	def remove_ip(self, mac):
		log(mac, 'removed ip')
		self.devices[mac]['ip'] = None

	def set_ip(self, mac, ip):
		log(mac, 'set ip: ' + ip)
		self.devices[mac]['ip'] = ip

	def update_last_active(self, mac):
		log(mac, 'activity detected')
		self.devices[mac]['lastActive'] = datetime.datetime.now()

	def get_info(self, mac):
		return self.devices[mac].copy()

	def get_all_info(self):
		return deepcopy(self.devices)

	def set_detected(self, mac, value):
		log(mac, 'set detected ' + str(value))
		self.devices[mac]['detected'] = value


devices = DeviceCollection()


def full_network_search_deamon_thread():
	if any(map(lambda info: info['ip'] is None, devices.get_all_info().values())):
		log(msg='Performing network search')
		for i in xrange(1, 256):
			arping(network_prefix + str(i), verbose=False, timeout=0.001)

	Timer(full_network_search_period_seconds, full_network_search_deamon_thread).start()


def custom_action(packet):
	global devices
	mac = packet.src
	if mac != '00:00:00:00:00:00' and devices.contain_mac(mac):
		devices.update_last_active(mac)

		if not devices.get_info(mac)['detected']:
			devices.set_detected(mac, True)
			on_connected(mac)

		if Ether in packet and packet[Ether].type == 0x0806 and packet.psrc.startswith(network_prefix): #if packet is ARP
			devices.set_ip(mac, packet.psrc)
			

def sniffer_thread():
	sniff(prn=custom_action)


def deamon_thread():
	global devices
	infos = devices.get_all_info()
	for mac, info in infos.iteritems():
		if info['lastActive'] + connection_lost_after < datetime.datetime.now():
			if info['detected']:
				devices.set_detected(mac, False)
				on_lost(mac)

			if info['ip'] is not None:
				devices.remove_ip(mac)

		elif info['lastActive'] + start_pinging_after < datetime.datetime.now() and info['ip'] is not None:
			log(mac, 'ping: ' + info['ip'])
			sr(IP(dst=info['ip'])/ICMP(), verbose=False, timeout=3)

	Timer(deamon_period_seconds, deamon_thread).start()


for mac in devices_macs:
	devices.add_device(mac)
	
Thread(target = sniffer_thread).start()
Thread(target = deamon_thread).start()
Thread(target = full_network_search_deamon_thread).start()
