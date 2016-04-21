from flask import Flask, render_template
app = Flask(__name__)

macs = [123, 234, 345]

@app.route("/")
def hello():
  #return "ddd"
  #return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])
  return render_template('index.html', macs=macs)

@app.route('/devices/{mac}', methods=['POST'])
def add_device(mac):
	macs.append(mac)
	return ""

@app.route('/devices/{mac}', methods=['DELETE'])
def delete_device(mac):
	macs.remove(mac)
	return ""

@app.route('/devices/registered', methods=['GET'])
def get_registered():
	return "ddd"

@app.route('/devices/connected', methods=['GET'])
def get_connected():
	return "aaa"


if __name__ == "__main__":

    app.run()