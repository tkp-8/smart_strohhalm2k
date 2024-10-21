import threading
import time
from gamepad import Gamepad
from gesichtserkennung import Gesicht
from outputGeraete import LED, Motor, Pumpe


eingeschaltet = True
liste_led = [LED(4, 2), LED(5, 1), LED(6, 0)]
while eingeschaltet:
    motor_x = Motor(channel=0, puls_min=0.63, puls_max=2.66)
    motor_y = Motor(channel=1, puls_min=0.63, puls_max=2.66)
    pumpe = Pumpe(17)
    while True:
        try:
            gamepad = Gamepad()
            while gamepad.eingabe != gamepad.tasten['A']:
                gamepad.modus_aendern()
                for led in liste_led:
                    led.zahl_anzeigen(gamepad.spielmodus)
        except:
            continue
            
        def fernsteuern(motor, achse):
            winkel = {'x':90, 'y':90}
            motor.winkel_einstellen(winkel[achse])
            while gamepad.eingabe != gamepad.tasten['B']:
                if gamepad.eingabe == gamepad.tasten['X'] and gamepad.gedrueckt:
                    pumpe.einschalten()          
                elif gamepad.eingabe == gamepad.tasten['X'] and gamepad.gedrueckt == False:                
                    pumpe.ausschalten()
                if gamepad.achsen[achse] > 0 and winkel[achse] < 179:
                    winkel[achse] += gamepad.achsen[achse]/32768
                    time.sleep(0.006)
                elif gamepad.achsen[achse] < 0 and winkel[achse] > 1:
                    winkel[achse] += gamepad.achsen[achse]/32768
                    time.sleep(0.006)    
                motor.winkel_einstellen(winkel[achse])
                
        def aufnehmen():
            while gamepad.eingabe != gamepad.tasten['B']:
                gesicht.erkennen()
                gesicht.anzeigen()
                gesicht.waitKey()
            gesicht.abbrechen()
            
        def gesichtserkennung(spielmodus):
            while True:
                gesicht.erkennen()
                if (gesicht.mund_offen and spielmodus == 2) or \
                (gesicht.mund_offen == False and spielmodus == 3):
                    pumpe.einschalten()
                elif (gesicht.mund_offen and spielmodus == 3) or \
                (gesicht.mund_offen == False and spielmodus == 2):
                    pumpe.ausschalten() 
                gesicht.anzeigen()
                gesicht.waitKey()
                if gamepad.gedrueckt:
                    gesicht.abbrechen()
                    break
                    
        def verfolgen(motor):
            i = 90
            motor.winkel_einstellen(i)
            while gamepad.gedrueckt == False:
                if motor == motor_x:              
                    if gesicht.mitte[0] - 40 > gesicht.mitte_aufnahme[0]:
                        if i >= 1:
                            i -= 0.045
                            motor.winkel_einstellen(i)
                            time.sleep(0.0002)       
                    elif gesicht.mitte[0] + 40 < gesicht.mitte_aufnahme[0]:
                        if i <= 179:
                            i += 0.045
                            motor.winkel_einstellen(i)
                            time.sleep(0.0002)
                elif motor == motor_y:
                    if gesicht.mitte[1] - 20 > gesicht.mitte_aufnahme[1]:
                        if i <= 120:
                            i += 0.03
                            motor.winkel_einstellen(i)
                            time.sleep(0.0008)       
                    elif gesicht.mitte[1] + 20 < gesicht.mitte_aufnahme[1]:
                        if i >= 60:
                            i -= 0.03
                            motor.winkel_einstellen(i)
                            time.sleep(0.0008)
        
        def automatisch(spielmodus):
            thread_taste_lesen = threading.Thread(target=lambda: gamepad.taste_lesen('B'))
            thread_verfolgen_x = threading.Thread(target=lambda: verfolgen(motor_x))
            thread_verfolgen_y = threading.Thread(target=lambda: verfolgen(motor_y))
            thread_taste_lesen.start()
            thread_verfolgen_x.start()
            thread_verfolgen_y.start()
            gesichtserkennung(gamepad.spielmodus)
            thread_taste_lesen.join()
            thread_verfolgen_x.join()
            thread_verfolgen_y.join()
            motor_x.beenden()
            motor_y.beenden()  
                          	        
        if gamepad.spielmodus == 1:
            gesicht = Gesicht(0)      
            thread_joystick = threading.Thread(target=gamepad.lesen)
            thread_motor_x = threading.Thread(target=lambda: fernsteuern(motor_x, 'x'))
            thread_motor_y = threading.Thread(target=lambda: fernsteuern(motor_y, 'y'))
            thread_joystick.start()
            thread_motor_x.start()
            thread_motor_y.start()
            aufnehmen()
            thread_joystick.join()
            thread_motor_x.join()
            thread_motor_y.join() 
            motor_x.beenden()
            motor_y.beenden()       
            break
        if gamepad.spielmodus == 2:
            gesicht = Gesicht(1)
            automatisch(gamepad.spielmodus) 
            break
        if gamepad.spielmodus == 3:
            gesicht = Gesicht(1)
            automatisch(gamepad.spielmodus)
            break

            
              
        
