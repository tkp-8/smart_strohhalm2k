import evdev
from evdev import InputDevice, categorize


class Gamepad:
	def __init__(self):
		self.tasten = {'A':305, 'B':304, 'ZL':312, 'ZR':313, \
		               'X':307, 'Y':308, 'ls_x':0, 'ls_y':1}
		self.achsen = {'x':0, 'y':0}
		self.spielmodi = list(range(8))
		self.spielmodus = 0
		self.gedrueckt = False
		self.eingabe = 0
		geraete = []
		for pfad in evdev.list_devices():
			geraete.append(evdev.InputDevice(pfad))
		for geraet in geraete:
			if geraet.name == 'Nintendo Switch Pro Controller':
				input_pfad = geraet.path
		self.gamepad = InputDevice(input_pfad)

	
	def lesen(self, wiederholen=True):
		for eingabe in self.gamepad.read_loop():
			if eingabe.type == 1 and eingabe.code != 0:
				self.eingabe = eingabe.code
				if eingabe.value == 1:
					self.gedrueckt = True
				elif eingabe.code == self.tasten['B']:
					break
				else: 
				    self.gedrueckt = False
				if wiederholen == False:
					break
			elif eingabe.type == 3:
				if eingabe.code == self.tasten['ls_x']:
					if (eingabe.value <= -4000 or eingabe.value >= 4000):
						self.achsen['x'] = eingabe.value 
					else:
						self.achsen['x'] = 0
				elif eingabe.code == self.tasten['ls_y']:
					if (eingabe.value <= -4000 or eingabe.value >= 4000):
						self.achsen['y'] = eingabe.value 
					else:
						self.achsen['y'] = 0
	

	def taste_lesen(self, taste):
		self.gedrueckt = False
		for eingabe in self.gamepad.read_loop():
			if eingabe.code == self.tasten[taste] and eingabe.value == 1:
				self.gedrueckt = True
				return True
				
	
	def modus_aendern(self):
		def vor():
			self.spielmodus = self.spielmodi[(self.spielmodus + 1) % 8]
			
		def zurueck():
			self.spielmodus = self.spielmodi[(self.spielmodus - 1) % 8]
			
		self.lesen(False)
		if self.gedrueckt:
			if self.eingabe == self.tasten['ZR']:
				vor()
			elif self.eingabe == self.tasten['ZL']:
				zurueck()
			

