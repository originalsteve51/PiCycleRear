import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from signalcontroller import SignalController

MQTT_SERVER = 'localhost'
MQTT_CMD_PATH = 'commands'
MQTT_SYNC_PATH = "synchronize"

signal_controller = SignalController()

def on_connect(client, userdata, flags, rc):
    print('CommandProcessor connected with rc = ', rc, ' Ready to receive commands.')
    client.subscribe(MQTT_CMD_PATH)

def on_message(client, userdata, msg):
    if msg.payload == b'left':
        signal_controller.left_arrow()
    if msg.payload == b'right':
        signal_controller.right_arrow()
    if msg.payload == b'off':
        signal_controller.stop_flashing()
    if msg.payload == b'brake':
        signal_controller.brake_on()
    if msg.payload == b'brake-off':
        signal_controller.brake_off()
    if msg.payload == b'ping':
        publish.single(MQTT_SYNC_PATH, 'ping:ack', hostname=MQTT_SERVER)
    if msg.payload == b'warning':
        signal_controller.warning()



class CommandProcessor(object):
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect(MQTT_SERVER, 1883, 60)



    def process(self):
        self.client.loop_forever()
