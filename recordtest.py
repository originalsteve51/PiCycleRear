
import time


import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish



MQTT_SERVER = 'localhost'
MQTT_CMD_PATH = "commands"

# main execution block starts here
#
# make a 5 second recording with the camera
#
if __name__ == '__main__':

    def process_record_request():
        cmd = 'record'
        publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)
        time.sleep(5)
        cmd = 'record-off'
        publish.single(MQTT_CMD_PATH, cmd, hostname=MQTT_SERVER)

    process_record_request()



