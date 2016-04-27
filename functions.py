available_callback_functions = {}

try:
	import RPi.GPIO as GPIO
	import time

	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(21,GPIO.OUT)
	GPIO.setup(20,GPIO.OUT)
	GPIO.setup(16,GPIO.OUT)

	GPIO.output(21,GPIO.LOW)
	GPIO.output(20,GPIO.LOW)
	GPIO.output(16,GPIO.LOW)

	available_callback_functions['on_red'] =     lambda : GPIO.output(21,GPIO.HIGH)
	available_callback_functions['off_red'] =    lambda : GPIO.output(21,GPIO.LOW)
	available_callback_functions['on_green'] =   lambda : GPIO.output(20,GPIO.HIGH)
	available_callback_functions['off_green'] =  lambda : GPIO.output(20,GPIO.LOW)
	available_callback_functions['on_yellow'] =  lambda : GPIO.output(16,GPIO.HIGH)
	available_callback_functions['off_yellow'] = lambda : GPIO.output(16,GPIO.LOW)







	def disco():
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		sequence = [16,20,21,20,16,20,21,20,16,20,21]
		for pin in sequence:
			GPIO.setup(pin,GPIO.OUT)
			GPIO.output(pin,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(pin,GPIO.LOW)

	available_callback_functions['disco'] = disco

	def blink_red():
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		pin = 21
		for i in range(10):
			GPIO.setup(pin,GPIO.OUT)
			GPIO.output(pin,GPIO.HIGH)
			time.sleep(0.2)
			GPIO.output(pin,GPIO.LOW)

	available_callback_functions['blink_red'] = blink_red

except:
	pass

def iseeyou():
	print "OH, I SEE YOU!"

available_callback_functions['i_see_you'] = iseeyou