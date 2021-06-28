import flask
from network import Bluetooth

bt = Bluetooth()

@app.route("/calibration", methods=['GET'])
def calibration:
    return bt.BluetoothManagerMeter()