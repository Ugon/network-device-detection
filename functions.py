available_callback_functions = {}

try:
	import RPi.GPIO as GPIO
	import time

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
