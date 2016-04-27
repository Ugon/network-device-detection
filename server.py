#!/usr/bin/python
# -*- coding: utf-8 -*-

from device_tracker import DeviceTracker
from settings import Settings

from flask import Flask
from flask import make_response
from flask import render_template
import logging
import parameters
import functions

logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
config = Settings()

device_tracker = DeviceTracker(first_ip=parameters.first_ip, last_ip=parameters.last_ip, config_object=config)

for mac, tuple in parameters.initial_devices.iteritems():
  device_tracker.add_device(mac)
  config.set_alias(mac, tuple[0])
  config.add_connected_callback(mac, tuple[1])
  config.add_disconnected_callback(mac, tuple[2])

@app.route("/")
def hello():
  macs = config.get_macs()
  connected = device_tracker.get_connected()
  aliases = config.get_aliases()
  return render_template('index.html', macs=macs, connected_macs=connected, aliases=aliases)

@app.route("/devices/<mac>", methods=['GET'])
def settings(mac):
  macs = config.get_macs()
  if mac not in macs:
    return hello()
  connected = device_tracker.get_connected()
  aliases = config.get_aliases()
  connected_callbacks = config.get_connected_callbacks_names(mac)
  disconnected_callbacks = config.get_disconnected_callbacks_names(mac)
  available_functions = config.available_functions()
  return render_template('settings.html', macs=macs, connected_macs=connected, aliases=aliases, mac=mac, connected_callbacks=connected_callbacks, disconnected_callbacks=disconnected_callbacks, available_functions=available_functions)

@app.route('/devices/<mac>/alias/<alias>', methods=['POST'])
def set_alias(mac, alias):
  config.set_alias(mac, alias)
  return "ok"

@app.route('/devices/<mac>', methods=['POST'])
def add_device(mac):
  config.register(mac)
  device_tracker.add_device(mac)
  return "ok"

@app.route('/devices/<mac>', methods=['DELETE'])
def delete_device(mac):
  config.unregister(mac)
  device_tracker.remove_device(mac)
  return "ok"

@app.route('/devices/<mac>/connected/<function>', methods=['POST'])
def add_connected(mac, function):
  config.add_connected_callback(mac, function)
  return "ok"

@app.route('/devices/<mac>/connected/<function>', methods=['DELETE'])
def remove_connected(mac, function):
  config.remove_connected_callback(mac, function)
  return "ok"

@app.route('/devices/<mac>/disconnected/<function>', methods=['POST'])
def add_disconnected(mac, function):
  config.add_disconnected_callback(mac, function)
  return "ok"

@app.route('/devices/<mac>/disconnected/<function>', methods=['DELETE'])
def remove_disconnected(mac, function):
  config.remove_disconnected_callback(mac, function)
  return "ok"

@app.route('/devices/registered', methods=['GET'])
def get_registered():
  return str(device_tracker.get_registered())

@app.route('/devices/connected', methods=['GET'])
def get_connected():
  return str(device_tracker.get_connected())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
  device_tracker.start()

  app.run(host='0.0.0.0', port=80)
