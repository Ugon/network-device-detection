from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/devices/{mac}', methods=['POST'])
def add_device():
	pass

@app.route('/devices/{mac}', methods=['DELETE'])
def delete_device():
	pass

@app.route('/devices/registered', methods=['GET'])
def get_registered():
	pass

@app.route('/devices/connected', methods=['GET'])
def get_connected():
	pass


if __name__ == "__main__":

    app.run()