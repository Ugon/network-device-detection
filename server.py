from device_tracker import DeviceTracker

from flask import Flask
from flask import make_response
from flask import render_template

app = Flask(__name__)

devices_macs = ['38:aa:3c:47:6f:3a']
device_tracker = DeviceTracker(network_prefix = '192.168.43.')
for mac in devices_macs:
	device_tracker.add_device(mac)

@app.route("/")
def hello():
  #return "ddd"
  #return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])
  return render_template('index.html', macs=device_tracker.get_devices())

@app.route('/devices/<mac>', methods=['POST'])
def add_device(mac):
	device_tracker.add_device(parsed_mac)
	return "ok"

@app.route('/devices/<mac>', methods=['DELETE'])
def delete_device(mac):
	device_tracker.remove_device(parsed_mac)
	return "ok"

@app.route('/devices/registered', methods=['GET'])
def get_registered():
	return str(device_tracker.get_devices())

@app.route('/devices/connected', methods=['GET'])
def get_connected():
	return "aaa"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
	device_tracker.start()

	app.run()