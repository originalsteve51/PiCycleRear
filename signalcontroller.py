import apa
import time
from threading import Thread
from threading import Event


import paho.mqtt.publish as publish

MQTT_SERVER = 'localhost'
MQTT_SYNC_PATH = 'synchronize'

left_range = range (0,24)
right_range = range (24,48)


class SignalController(object):

	def __init__(self):
		self.__direction = None
		self.__keep_flashing = True
		self.__brake_on=False
		self.__brake_event = Event()
		self.__brake_event.set()

		self.__led_arrows = apa.Apa(48)
		self.__led_arrows.flush_leds()

		self.__brake_signal = apa.Apa(48)
		self.__brake_signal.flush_leds()
		for led in range(0,48):
			self.__brake_signal.led_set(led, 31, 0, 0, 255)

	def __flash(self, direction):
		self.__direction = direction
		self.__keep_flashing = True
		flashThread = Thread(target=self.run_flasher)
		flashThread.start()

	def run_flasher(self):
		print('flash thread starting')
		while self.__keep_flashing:
			self.__brake_event.wait()
			self.__led_arrows.write_leds()
			publish.single(MQTT_SYNC_PATH, 'on:'+self.__direction, hostname=MQTT_SERVER)
			time.sleep(0.5)
			self.__brake_event.wait()
			self.__led_arrows.reset_leds()
			publish.single(MQTT_SYNC_PATH, 'off:'+self.__direction, hostname=MQTT_SERVER)
			time.sleep(0.5)
		self.__led_arrows.zero_leds()

	def stop_flashing(self):
		print('signal stop flashing')
		self.__keep_flashing = False
		publish.single(MQTT_SYNC_PATH, 'stop:both', hostname=MQTT_SERVER)

	def right_arrow(self):
		print('signal right arrow')
		self.__keep_flashing = True
		self.__led_arrows.zero_leds()
		for led in right_range:
			self.__led_arrows.led_set(led, 31, 0, 255, 255)
		self.__flash('r')

	def left_arrow(self):
		print('signal left arrow')
		self.__keep_flashing = True
		self.__led_arrows.zero_leds()
		for led in left_range:
			self.__led_arrows.led_set(led, 31, 0, 255, 255)
		self.__flash('l')

	def brake_on(self):
		print('brake on')
		self.__brake_event.clear()
		time.sleep(0.2)
		self.__brake_signal.write_leds()
		publish.single(MQTT_SYNC_PATH, 'brake:on', hostname=MQTT_SERVER)

	def brake_off(self):
		print('brake off')
		self.__brake_signal.reset_leds()
		self.__brake_event.set()
		publish.single(MQTT_SYNC_PATH, 'brake:off', hostname=MQTT_SERVER)

	# warning will be replaced by camera_on, which will record for some
	# amount of time (30 sec?) each time it is processed.
	def warning(self):
		print('warning')
		publish.single(MQTT_SYNC_PATH, 'warning:ack', hostname=MQTT_SERVER)



