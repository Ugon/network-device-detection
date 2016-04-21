from device_tracker import DeviceTracker

from flask import Flask
from flask import make_response

app = Flask(__name__)

devices_macs = ['38:aa:3c:47:6f:3a']
device_tracker = DeviceTracker(network_prefix = '192.168.43.')


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/devices/<mac>', methods=['POST'])
def add_device(mac):
	parsed_mac = mac.replace('-', ':')
	device_tracker.add_device(mac)
	return "ok"

@app.route('/devices/<mac>', methods=['DELETE'])
def delete_device(mac):
	parsed_mac = mac.replace('-', ':')
	device_tracker.remove_device(mac)
	return "ok"

@app.route('/devices/registered', methods=['GET'])
def get_registered():
	return device_tracker.devices

@app.route('/devices/connected', methods=['GET'])
def get_connected():
	pass

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
	device_tracker.start()

	app.run()