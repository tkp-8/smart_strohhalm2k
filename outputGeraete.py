from board import SCL, SDA
from adafruit_pca9685 import PCA9685
import busio
import RPi.GPIO as gpio
import time


class LED():
	def __init__(self, channel, stelle):
		i2c = busio.I2C(SCL, SDA)
		self.channel = channel
		self.stelle = stelle
		self.pwm = PCA9685(i2c)
		self.pwm.frequency = 60
		self.helligkeit = 0x0
		self.pwm.channels[self.channel].duty_cycle = self.helligkeit
		
	
	def einschalten(self):
		while self.helligkeit < 0xFFFF:
			self.helligkeit += 0x80
			if self.helligkeit > 0xFFFF:
				self.helligkeit = 0xFFFF
			self.pwm.channels[self.channel].duty_cycle = self.helligkeit
		
		
	def ausschalten(self):
		while self.helligkeit > 0x0:
			self.helligkeit -= 0x80
			if self.helligkeit < 0x0:
				self.helligkeit = 0x0
			self.pwm.channels[self.channel].duty_cycle = self.helligkeit
		
	
	def zahl_anzeigen(self, zahl):
		binaer = bin(zahl)[2:].zfill(3)
		if int(binaer[self.stelle]) == 1:
			self.einschalten()
		else:
			self.ausschalten()
			

class Motor():
	def __init__(self, channel, puls_min, puls_max):
		i2c = busio.I2C(SCL, SDA)
		self.channel = channel
		self.puls_min = puls_min
		self.puls_max = puls_max
		self.pwm = PCA9685(i2c)
		self.pwm.frequency = 50
		self.pwm.channels[self.channel].duty_cycle = 0x0
		
	
	def winkel_einstellen(self, winkel):
		if 0 <= winkel <= 180:
			breite_puls = (self.puls_max-self.puls_min)/180 * winkel \
						+ self.puls_min
			periode = 1000/50
			duty_cycle = int(int(hex(int(breite_puls/periode*1000)), 16) \
					   / 0x3E8 * 0xFFFF)
			self.pwm.channels[self.channel].duty_cycle = duty_cycle
	
	
	def beenden(self):
		self.pwm.channels[self.channel].duty_cycle = 0x0
		
		
class Pumpe():
	def __init__(self, PIN):
		self.PIN = PIN
		gpio.setmode(gpio.BCM)
		gpio.setup(self.PIN, gpio.OUT)
		self.ausschalten()
		
		
	def einschalten(self):
		gpio.output(self.PIN, False)
	
	
	def ausschalten(self):
		gpio.output(self.PIN, True)
		
	
