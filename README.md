# PiCycleRear
Code that runs at the back of my bicycle where the rear-facing turn signal arrows are located.

This is half of a cycling 'Internet of Things' project that was inspired by projects seen by me on the Raspi.tv site.

The concept is that two Raspberry Pi Zero W computers collaborate to provide a wireless connection from a front 'dashboard' on the handlebars and a unit mounted beneath the seat of the bicycle.

Each unit has its own power supply (lithium battery pack). MQTT is used to convey commands entered on the front dashboard to
the rear unit. The rear unit is a Wifi access point that the front unit connects to. As the units are on the same rolling
Wifi network, connectivity is provided. A Mosquitto server running on the rear unit enables MQTT messaging. 

Raspi.tv supplies cleverly packaged LED displays along with terrific Python support using a class called Apa. I assume this is short for
all-points-addressable. It allows each individual LED on the displays to be turned on or off with RGB color support for each.

The LEDs are packaged as two triangular arrays of 24 LEDs per triangle. Raspi.tv also supplies a reasonably proced interface card
that level-shifts the 3.3 v signals from the Raspberry Pi to 5 volts, this to power the LEDs.

Initially, I am only packaging a rear-facing set of arrows to provide turn signaling. Another set of 24 LEDs packaged as a circle
will eventually become the front turn signal. 

See PiCycleFront for the code that provides the dashboard that sits at the front of the bicycle.
