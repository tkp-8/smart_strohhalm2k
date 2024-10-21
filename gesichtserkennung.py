import cv2
import dlib
import math
from imutils import face_utils


class Gesicht:
	def __init__(self, erkennung):
		pfad = 'shape_predictor_68_face_landmarks.dat'
		self.mund_offen = False
		self.gesicht_erkannt = False
		self.erkennung = erkennung
		if self.erkennung:
			self.face_detector = dlib.get_frontal_face_detector()
			self.face_predictor = dlib.shape_predictor(pfad)
		self.aufnahme = cv2.VideoCapture(0)
		self.mitte_aufnahme = (1280*0.35 // 2 + 40, 720*0.35 // 2)
		self.mitte = self.mitte_aufnahme
			
		
	def erkennen(self):
		global frame
		_, frame = self.aufnahme.read()
		global klein 
		klein = cv2.resize(frame, (int(frame.shape[1]*0.35),int(frame.shape[0]*0.35)))
		if self.erkennung:
			grau = cv2.cvtColor(klein, cv2.COLOR_BGR2GRAY)
			try:
				gesichter = self.face_detector(grau, 1)
				global landmark_anzeige
				for gesicht in gesichter:
					landmark = self.face_predictor(grau, gesicht)
					landmark = landmark_anzeige = face_utils.shape_to_np(landmark)
				punkte = [
				[50, 61, 67, 58], 
				[51, 62, 66, 57], 
				[52, 63, 65, 56],
				]
				wb_punkte = {}
				for liste in punkte:
					for punkt in liste:
						wb_punkte[(punkt,'x')] = landmark[punkt][0]
						wb_punkte[(punkt,'y')] = landmark[punkt][1]
				self.mitte = (wb_punkte[(62,'x')], 
							 int(wb_punkte[(66,'y')] 
							 + (wb_punkte[(62,'y')]
							 -wb_punkte[(66,'y')])
							 /2))
							 
				def abstand(p1, p2):
					abstand = (math.sqrt(
							  (wb_punkte[(p2, 'x')]-wb_punkte[(p1, 'x')]) ** 2 
							+ (wb_punkte[(p2, 'y')]-wb_punkte[(p1, 'y')]) ** 2))
					return abstand	
				
				breite_oberlippe = 0
				breite_oeffnung = 0
				breite_unterlippe = 0
				for i in range(3):
					breite_oberlippe += abstand(punkte[i][0], punkte[i][1]) / 3
					breite_oeffnung += abstand(punkte[i][1], punkte[i][2]) / 3
					breite_unterlippe += abstand(punkte[i][2], punkte[i][3]) / 3
				if breite_oeffnung > 1.7*(breite_oberlippe+breite_unterlippe) / 2:
					self.mund_offen = True
				else:
					self.mund_offen = False
				self.gesicht_erkannt = True
				landmark = None
			except:
				self.gesicht_erkannt = False
				self.mund_offen = False
				self.mitte = self.mitte_aufnahme
				
			
	def anzeigen(self):
		if self.gesicht_erkannt:
			for index, koordinaten in enumerate(landmark_anzeige):
				if index > 48:
					cv2.circle(img=klein, center=koordinaten, 
					radius=2, color=(255,0,0), thickness=-1)
			cv2.circle(img=klein, center=self.mitte, 
			radius=2, color=(0,255,0), thickness=-1)
			if self.mund_offen:
				cv2.putText(klein, 'offen', (23, 50), \
					        cv2.FONT_HERSHEY_PLAIN, 2, \
					        (255, 0, 0), 3, cv2.LINE_AA)
			else:
				cv2.putText(klein, 'geschlossen', (23, 50), \
				            cv2.FONT_HERSHEY_PLAIN, 2, \
				            (255, 0, 0), 3, cv2.LINE_AA)
		if self.erkennung:
			cv2.imshow('frame', klein)
		else:
			cv2.imshow('frame', frame)
		
		
	def waitKey(self):
		k = cv2.waitKey(1)
	
	
	def abbrechen(self):
		cv2.destroyAllWindows()
		self.aufnahme.release()
