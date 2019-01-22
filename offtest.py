import time
from threading import Thread


import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish



MQTT_SERVER = 'localhost'
MQTT_CMD_PATH = "commands"

# main execution block starts here
if __name__ == '__main__':

    def process_signal_off():
        cmd = 'off'
        publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)

    process_signal_off()


