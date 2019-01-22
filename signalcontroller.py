import apa
import time
from threading import Thread
from threading import Event
import camera


import paho.mqtt.publish as publish

MQTT_SERVER = 'localhost'
MQTT_SYNC_PATH = 'synchronize'

left_range = range (0, 24)
right_range = range (32, 56)

brake_range = range (24, 32)

animation_left_on = [
       [0,1,2,3,4,5,6,7],
       [0,1,2,3,4,5,6,7, 8,                                         23],
       [0,1,2,3,4,5,6,7, 8,9,                                    22,23],
       [0,1,2,3,4,5,6,7, 8,9,10,                              21,22,23],
       [0,1,2,3,4,5,6,7, 8,9,10,11,                        20,21,22,23],
       [0,1,2,3,4,5,6,7, 8,9,10,11,12,                  19,20,21,22,23],
       [0,1,2,3,4,5,6,7, 8,9,10,11,12,13,            18,19,20,21,22,23],
       [0,1,2,3,4,5,6,7, 8,9,10,11,12,13,14,      17,18,19,20,21,22,23],
       [0,1,2,3,4,5,6,7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] ]


animation_left_off = [
      [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
      [    10,11,12,13,14,15,16,17,18,19,20,21      ],
      [       11,12,13,14,15,16,17,18,19,20         ],
      [          12,13,14,15,16,17,18,19            ],
      [             13,14,15,16,17,18               ],
      [                14,15,16,17                  ],
      [                   15,16                     ],
      [                                             ]  ]

animation_right_on = [
       [32,33,34,35,36,37,38,39],
       [32,33,34,35,36,37,38,39, 40,                                         55],
       [32,33,34,35,36,37,38,39, 40,41,                                    54,55],
       [32,33,34,35,36,37,38,39, 40,41,42,                              53,54,55],
       [32,33,34,35,36,37,38,39, 40,41,42,43,                        52,53,54,55],
       [32,33,34,35,36,37,38,39, 40,41,42,43,44,                  51,52,53,54,55],
       [32,33,34,35,36,37,38,39, 40,41,42,43,44,45,            50,51,52,53,54,55],
       [32,33,34,35,36,37,38,39, 40,41,42,43,44,45,46,      49,50,51,52,53,54,55],
       [32,33,34,35,36,37,38,39, 40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55] ]


animation_right_off = [
      [40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55],
      [   41,42,43,44,45,46,47,48,49,50,51,52,53,54   ],
      [      42,43,44,45,46,47,48,49,50,51,52,53      ],
      [         43,44,45,46,47,48,49,50,51,52         ],
      [            44,45,46,47,48,49,50,51            ],
      [               45,46,47,48,49,50               ],
      [                  46,47,48,49                  ],
      [                     47,48                     ] ]

# Future: animate the brake bar too
animation_brake_on = [
      [24,                  31],
      [24,25,            30,31],
      [24,25,26,      29,30,31],
      [24,25,26,27,28,29,30,31] ]

animation_brake_off = [
      [ 25,26,27,28,29,30 ],
      [    26,27,28,29    ],
      [       27,28       ],
      [                   ] ]

class SignalController(object):

	def __init__(self):
		self.__direction = None
		self.__braking = False
		self.__keep_flashing = True
		self.__arrow_on = False

		self.__camera = camera.PiCycleCamera()

		self.__led_arrows = apa.Apa(56)
		self.__led_arrows.flush_leds()
		self.__led_arrows.zero_leds()
		self.__led_arrows.write_leds()

		signalsThread = Thread(target=self.run_signals)
		signalsThread.start()


	def animate_arrow(self, animation_on, animation_off, dark_range, direction):
		publish.single(MQTT_SYNC_PATH, 'on:'+direction, hostname=MQTT_SERVER)

		for idx in range(0,8,2):
			on_leds = animation_on[idx]
			off_leds = animation_off[idx]

			for jdx in range(0, len(on_leds)):
				self.__led_arrows.led_set(on_leds[jdx], 31, 0, 255, 255)

			for jdx in range(0, len(off_leds)):
				self.__led_arrows.led_set(off_leds[jdx], 0, 0, 0, 0)

			self.__led_arrows.write_leds()

		on_leds = animation_on[8]
		off_leds = animation_off[7]
		for jdx in range(0, len(on_leds)):
			self.__led_arrows.led_set(on_leds[jdx], 31, 0, 255, 255)

		for jdx in range(0, len(off_leds)):
			self.__led_arrows.led_set(off_leds[jdx], 0, 0, 0, 0)

		self.__led_arrows.write_leds()


	"""
	def animate_arrow(self, ranges, direction, on_off):
		print('animating arrow')
		if on_off == 'on':
			intensity = 31
		else:
			intensity = 0
		for range_idx in range(0, len(ranges)):
			for led in ranges[range_idx]:
				self.__led_arrows.led_set(led, intensity, 0, 255, 255)
		publish.single(MQTT_SYNC_PATH, on_off+':'+direction, hostname=MQTT_SERVER)
		self.__led_arrows.write_leds()
	"""

	def arrow(self, direction):
		print('arrow:'+direction)
		if direction == 'r':
			animation_on = animation_right_on
			animation_off = animation_left_off
			dark_range = left_range
		else:
			animation_on = animation_left_on
			animation_off = animation_left_off
			dark_range = right_range

		if self.__keep_flashing:
			if self.__arrow_on == False:
				self.__arrow_on = True
				self.animate_arrow(animation_on, animation_off, dark_range, direction)
			else:
				self.__arrow_on = False
				self.off_arrows()

	def off_arrows(self):
		self.__arrow_on = False
		for led in left_range:
			self.__led_arrows.led_set(led, 0, 0, 255, 255)
		publish.single(MQTT_SYNC_PATH, 'off:l', hostname=MQTT_SERVER)
		for led in right_range:
			self.__led_arrows.led_set(led, 0, 0, 255, 255)
		publish.single(MQTT_SYNC_PATH, 'off:r', hostname=MQTT_SERVER)
		self.__led_arrows.write_leds()


	def brake_light(self):
		if self.__braking:
			for led in brake_range:
				self.__led_arrows.led_set(led, 31, 0, 0, 255)
		else:
			for led in brake_range:
				self.__led_arrows.led_set(led, 0, 0, 0, 255)


	def run_signals(self):
		print('signals thread starting')
		while True:
			if self.__direction is None:
				self.off_arrows()
			if self.__direction is not None or self.__braking:
				if self.__direction == 'r':
					self.arrow('r')
				if self.__direction == 'l':
					self.arrow('l')
			self.brake_light()
			self.__led_arrows.write_leds()
			time.sleep(0.5)

	def stop_flashing(self):
		print('signal stop flashing')
		self.__keep_flashing = False
		self.__direction = None
		publish.single(MQTT_SYNC_PATH, 'stop:both', hostname=MQTT_SERVER)

	def right_arrow(self):
		print('signal right arrow')
		if self.__direction == 'l':
			self.off_arrows()
		self.__keep_flashing = True
		self.__direction = 'r'

	def left_arrow(self):
		print('signal left arrow')
		if self.__direction == 'r':
			self.off_arrows()
		self.__keep_flashing = True
		self.__direction = 'l'

	def brake_on(self):
		print('brake on')
		self.__braking = True
		publish.single(MQTT_SYNC_PATH, 'brake:on', hostname=MQTT_SERVER)

	def brake_off(self):
		print('brake off')
		self.__braking = False
		publish.single(MQTT_SYNC_PATH, 'brake:off', hostname=MQTT_SERVER)

	def start_recording(self, filename):
		print('start recording: ', filename)
		self.__camera.start_recording(filename)
		publish.single(MQTT_SYNC_PATH, 'start-recording', hostname=MQTT_SERVER)

	def stop_recording(self):
		print('stop recording')
		self.__camera.stop_recording()
		publish.single(MQTT_SYNC_PATH, 'stop-recording', hostname=MQTT_SERVER)


