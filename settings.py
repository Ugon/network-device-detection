from functions import available_callback_functions

class Settings():
	def __init__(self):
		self.macs = {}
		self.available_callbacks = available_callback_functions

	def register(self, mac):
		self.macs[mac] = {
			'alias': '',
			'connected': [],
			'disconnected': []
		}

	def get_macs(self):
		return self.macs.keys()

	def unregister(self, mac):
		del self.macs[mac]

	def function_exists(self, name):
		return name in self.available_callbacks.keys()

	def available_functions(self):
		return self.available_callbacks.keys()

	def registered(self, mac):
		return mac in self.macs.keys()

	def set_alias(self, mac, new_alias):
		self.macs[mac]['alias'] = new_alias

	def add_connected_callback(self, mac, callback_name):
		if self.registered(mac) and self.function_exists(callback_name):
			if callback_name not in self.macs[mac]['connected']:
				self.macs[mac]['connected'].append(callback_name)

	def add_disconnected_callback(self, mac, callback_name):
		if self.registered(mac) and self.function_exists(callback_name):
			if callback_name not in self.macs[mac]['disconnected']:
				self.macs[mac]['disconnected'].append(callback_name)

	def remove_connected_callback(self, mac, callback_name):
		if self.registered(mac) and self.function_exists(callback_name):
			self.macs[mac]['connected'].remove(callback_name)

	def remove_disconnected_callback(self, mac, callback_name):
		if self.registered(mac) and self.function_exists(callback_name):
			self.macs[mac]['disconnected'].remove(callback_name)

	def get_connected_callbacks(self, mac):
		return [self.available_callbacks[name] for name in self.macs[mac]['connected']]

	def get_disconnected_callbacks(self, mac):
		return [self.available_callbacks[name] for name in self.macs[mac]['disconnected']]

	def get_connected_callbacks_names(self, mac):
		return self.macs[mac]['connected']

	def get_disconnected_callbacks_names(self, mac):
		return self.macs[mac]['disconnected']


	def get_aliases(self):
		return {mac: self.macs[mac]['alias'] for mac in self.macs.keys()}