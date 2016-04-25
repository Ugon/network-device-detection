from __future__ import print_function

network_prefix = '192.168.0.'

#with device_tracker callbacks:
initial_devices = {
	'38:aa:3c:47:6f:3a' : ('wojtek', lambda : print('wojtek online'), lambda : print('wojtek offline')), 
	'dc:ee:06:a0:b5:56' : ('stasiek', lambda : print('stasiek online'), lambda : print('stasiek offline'))}
	# 'xx:xx:xx:xx:xx:xx' : ('szymon', lambda : print('szymon online,) lambda : print('szymon offline'))}

#without device_tracker callbacks
# initial_devices = {
	# '38:aa:3c:47:6f:3a' : ('wojtek', None, None), 
	# 'dc:ee:06:a0:b5:56' : ('stasiek', None, None)
	# 'xx:xx:xx:xx:xx:xx' : ('szymon', None, None)}

