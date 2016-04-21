from scapy.all import *
from copy import deepcopy
from threading import Thread, Timer
import datetime

def _log(mac=None, msg=None):
	if mac is not None:
		print datetime.datetime.now().isoformat(' ')[0:19] + ' [' + mac + '] ' + msg
	else:
		print datetime.datetime.now().isoformat(' ')[0:19] + ' ' + msg

class DeviceTracker():

	#############################################################
	############################API##############################
	#############################################################

	def __init__(self, 
				network_prefix,
				start_pinging_after = datetime.timedelta(seconds=5),
				connection_lost_after = datetime.timedelta(seconds=10),
				deamon_period_seconds = 1,
				full_network_search_period_seconds = 30):
		
		def on_connected(mac):
			print '#############################################################'
			print '########## [' + mac       + '] connected ####################'
			print '#############################################################'
	
		def on_disconnected(mac):
			print '#############################################################'
			print '########## [' + mac       + '] disconnected #################'
			print '#############################################################'

		self.devices = {}
		self.on_connected = on_connected
		self.on_disconnected = on_disconnected

		self.network_prefix = network_prefix
		self.start_pinging_after = start_pinging_after
		self.connection_lost_after = connection_lost_after
		self.deamon_period_seconds = deamon_period_seconds
		self.full_network_search_period_seconds = full_network_search_period_seconds


	def add_device(self, mac):
		_log(mac, 'added device')
		self.devices[mac] = {'ip': None, 'lastActive': datetime.datetime(year=1, month=1, day=1), 'detected': False}
	
	def remove_device(self, mac):
		_log(mac, 'removed device')
		del self.devices[mac]

	def set_on_connected(self, function):
		self.on_connected = function;

	def set_on_disconnected(self, function):
		self.on_disconnected = function;

	def start(self):
		Thread(target = self._sniffer_thread_fun).start()
		Thread(target = self._deamon_thread_fun).start()
		Thread(target = self._full_network_search_deamon_thread_fun).start()


	#############################################################
	##########################INTERNAL###########################
	#############################################################

	def _contains_mac(self, mac):
		return mac in self.devices
		
	def _remove_ip(self, mac):
		_log(mac, 'removed ip')
		self.devices[mac]['ip'] = None
		
	def _set_ip(self, mac, ip):
		_log(mac, 'set ip: ' + ip)
		self.devices[mac]['ip'] = ip
		
	def _update_last_active(self, mac):
		_log(mac, 'activity detected')
		self.devices[mac]['lastActive'] = datetime.datetime.now()
		
	def _get_info(self, mac):
		return self.devices[mac].copy()
		
	def _get_all_info(self):
		return deepcopy(self.devices)
		
	def _set_detected(self, mac, value):
		_log(mac, 'set detected ' + str(value))
		self.devices[mac]['detected'] = value


	#############################################################
	##########################DEMONS#############################
	#############################################################

	def _full_network_search_deamon_thread_fun(self):
		if any(map(lambda info: info['ip'] is None, self._get_all_info().values())):
			_log(msg='Performing network search')
			for i in xrange(1, 255):
				arping(self.network_prefix + str(i), verbose=False, timeout=0.001)

		Timer(self.full_network_search_period_seconds, self._full_network_search_deamon_thread_fun).start()

	def _sniffer_action(self, packet):
		mac = packet.src
		if mac != '00:00:00:00:00:00' and self._contains_mac(mac):
			self._update_last_active(mac)

			if not self._get_info(mac)['detected']:
				self._set_detected(mac, True)
				self.on_connected(mac)

			if Ether in packet and packet[Ether].type == 0x0806 and packet.psrc.startswith(self.network_prefix): #if packet is ARP
				self._set_ip(mac, packet.psrc)
			
				
	def _sniffer_thread_fun(self):
		sniff(prn=self._sniffer_action)

	def _deamon_thread_fun(self):
		infos = self._get_all_info()
		for mac, info in infos.iteritems():
			if info['lastActive'] + self.connection_lost_after < datetime.datetime.now():
				if info['detected']:
					self._set_detected(mac, False)
					self.on_disconnected(mac)

				if info['ip'] is not None:
					self._remove_ip(mac)

			elif info['lastActive'] + self.start_pinging_after < datetime.datetime.now() and info['ip'] is not None:
				_log(mac, 'ping: ' + info['ip'])
				sr(IP(dst=info['ip'])/ICMP(), verbose=False, timeout=3)

		Timer(self.deamon_period_seconds, self._deamon_thread_fun).start()