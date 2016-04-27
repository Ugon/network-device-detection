from scapy.all import *
from copy import deepcopy
from threading import Thread
import datetime
import time
import logging
import os
import subprocess

FNULL = open('/dev/null', 'w')

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

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
				first_ip,
				last_ip,
				config_object,
				start_pinging_after = datetime.timedelta(seconds=5),
				connection_lost_after = datetime.timedelta(seconds=15),
				deamon_period_seconds = 5,
				full_network_search_period_seconds = 30):
		self.devices = {}
		self.config = config_object

		self.first_ip = first_ip
		self.last_ip = last_ip
		self.start_pinging_after = start_pinging_after
		self.connection_lost_after = connection_lost_after
		self.deamon_period_seconds = deamon_period_seconds
		self.full_network_search_period_seconds = full_network_search_period_seconds

	def add_device(self, mac, connected_callback = None, disconnected_callback = None):
		_log(mac, 'added device')
		self.devices[mac] = {
			'ip' : None, 
			'lastActive' : datetime.datetime(year=1, month=1, day=1), 
			'detected' : False,
			'connected_callback' : connected_callback,
			'disconnected_callback' : disconnected_callback }
		self.config.register(mac)

	def set_connected_callback(self, mac, connected_callback):
		self.devices[mac]['connected_callback'] = connected_callback

	def set_disconnected_callback(self, mac, disconnected_callback):
		self.devices[mac]['disconnected_callback'] = disconnected_callback

	def remove_device(self, mac):
		_log(mac, 'removed device')
		self.config.unregister(mac)
		del self.devices[mac]

	def start(self):
		Thread(target = self._sniffer_thread_fun).start()
		Thread(target = self._deamon_thread_fun).start()
		Thread(target = self._full_network_search_deamon_thread_fun).start()

	def get_registered(self):
		return self.devices.keys()

	def get_connected(self):
		connected = [k for k, v in self.devices.iteritems() if v['detected']]
		return connected

	#############################################################
	##########################INTERNAL###########################
	#############################################################

	def _execute_connected_functions_for(self, mac):
		cbs = self.config.get_connected_callbacks(mac)
		for cb in cbs:
			cb()

	def _execute_disconnected_functions_for(self, mac):
		cbs = self.config.get_disconnected_callbacks(mac)
		for cb in cbs:
			cb()

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
		if value == False and self.devices[mac]['disconnected_callback'] is not None:
			self.devices[mac]['disconnected_callback']()
		elif value == True and self.devices[mac]['connected_callback'] is not None:
			self.devices[mac]['connected_callback']()

	#############################################################
	##########################DEMONS#############################
	#############################################################

	def _full_network_search_deamon_thread_fun(self):
		while(True):
			_log(msg='Performing network search')
			subprocess.call('fping -c 1 -g ' + self.first_ip + ' ' + self.last_ip, shell=True, stdout=FNULL, stderr=FNULL)

			time.sleep(self.full_network_search_period_seconds)

	def _sniffer_action(self, packet):
		mac = packet.src
		if mac != '00:00:00:00:00:00' and self._contains_mac(mac):
			self._update_last_active(mac)

			if not self._get_info(mac)['detected']:
				self._set_detected(mac, True)
				self._execute_connected_functions_for(mac)

			if Ether in packet and ICMP in packet[Ether] and packet[Ether][ICMP].type == 0:
				if not self.devices[mac]['ip'] == packet[IP].src:
					self._set_ip(mac, packet[IP].src)
				
	def _sniffer_thread_fun(self):
		sniff(prn=self._sniffer_action)

	def _deamon_thread_fun(self):
		while(True):
			infos = self._get_all_info()
			for mac, info in infos.iteritems():
				if info['lastActive'] + self.connection_lost_after < datetime.datetime.now():
					if info['detected']:
						self._set_detected(mac, False)
						self._execute_disconnected_functions_for(mac)
	
					if info['ip'] is not None:
						self._remove_ip(mac)
	
				elif info['lastActive'] + self.start_pinging_after < datetime.datetime.now() and info['ip'] is not None:
					_log(mac, 'ping: ' + info['ip'])
					# send(IP(dst=info['ip'])/ICMP(), verbose=False)
					subprocess.call('ping ' + info['ip'] + ' -c 1 -w 1', shell=True, stdout=FNULL, stderr=FNULL)

			time.sleep(self.deamon_period_seconds)
