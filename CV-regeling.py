# CV-regeling.py            rpixavrob5   14-12-2021
#
import tempmodule_a
import time
import datetime
import tijd
import os
#import OLED
import RPi.GPIO as GPIO # is dit compatibel met OLED-import : 
#                       #    import board en import busio?
#                       #    ja indien :
#                       #    GPIO.setmode(GPIO.BCM) ipv GPIO.setmode(GPIO.BOARD) in OLED
#
GPIO.setmode(GPIO.BCM)
stook = 9   # stookseizoen
GPIO.setup(stook,GPIO.IN,pull_up_down=GPIO.PUD_UP)
thermo = 25  # thermostaat
GPIO.setup(thermo,GPIO.IN,pull_up_down=GPIO.PUD_UP)
nacht = 7  # geen nachtverlaging
GPIO.setup(nacht,GPIO.IN,pull_up_down=GPIO.PUD_UP)
led1 = 11    # CV-aan oranje led
GPIO.setup(led1,GPIO.OUT)
led2 = 8    # CV-hoog rode led
GPIO.setup(led2,GPIO.OUT)
CV = 24      # CV aansturing dmv relais
GPIO.setup(CV,GPIO.OUT)
relais2 = 13      # voor relais, kanaal 2 # voor elke WHILE : 1 sec
GPIO.setup(relais2,GPIO.OUT)
relais3 = 19      # voor relais, kanaal 3 # als thermostaat aan staat : 1 sec
GPIO.setup(relais3,GPIO.OUT)
relais4 = 26      # voor relais, kanaal 4 # bij elke logging : 1 sec
GPIO.setup(relais4,GPIO.OUT)
buttonA = 5   # OLED Bonnet button A
GPIO.setup(stook,GPIO.IN,pull_up_down=GPIO.PUD_UP)
buttonB = 6  # OLED Bonnet button B
GPIO.setup(thermo,GPIO.IN,pull_up_down=GPIO.PUD_UP)
###################################################
#
# E:\Raspberry Pi\Temp\CV-regeling.xlsx
# -5°C = 40Kohm
# 0°C  = 32Kohm
# 10°C = 20Kohm
# 19°C = 13Kohm
# 25°C = 10Kohm
# 43°C = 4,7Kohm
#
# vanaf 3,5 minuut gaat de CV over naar "hoog vermogen / laag rendement" van "3" naar "5"
# de CV slaat normaal ongeveer 3 x langer aan dan de tijd van de puls
# de CV verbruikt dan ongeveer 60 liter gas per minuut puls, of 20 liter gas per minuut "branden"
# per minuut branden, dus "3 = hoog rendement/ laag vermogen" verbruikt de CV 20 liter/minuut
# bij de instelling van de LOGO bleef de CV "3 = hoog rendement/ laag vermogen" 
#  als er 5 minuten tussen het begin van de pulsen was.
#
# de LOGO was zo ingesteld dat er elke 5 min een puls was van 2 min
#  dwz 12 pulsen/uur om "3 = hoog rendement/ laag vermogen" te krijgen
# indien na één uur de vraag nog steeds is, wordt het aantal pulsen verhoogd,
#  dwz dat men dan tijdelijk "5 = laag rendement/ hoog vermogen" krijgt
#
# 1m³ = 8 pulsen of 125 liter per puls hoog rendement/ laag vermogen ...
#
###################################################
#
# 100 meter kabel heeft een weerstand van 14 Ohm
# 10 meter kabel heeft geen invloed op de weerstand
# 10 meter kabel = 20 meter stroomdraad van en naar de 10K Ohm NTC Epoxy Thermistor
# dus 2,8 Ohm extra
# https://www.adafruit.com/product/372
# adefruit product 372 : 10K Ohm NTC Epoxy Thermistor
#
# https://www.adafruit.com/product/1083
# ADS1015 12-Bit ADC - 4 Channel I2C
# adefruit PRODUCT ID: 1083
#
# relais
# https://www.youtube.com/watch?v=My1BDB1ei0E
# 4-kanaals 5V relais module : kw-1613
# remove jumper and use pins, under jumper, for connecting separatly 5V and 3.3V
# don't use the VCC of the 6-pins GND,IN1,IN2,IN3,IN4,(VCC)
# JD-VCC = 5V
# VCC    = 3.3V
# pin directly to IN1 or 2 or 3 or 4 without resistance
#
def read_stop():
#    lezen van "stop" of "reboot" of "run" opdracht
    stopbestand = open('/home/pi/Program/CV-regeling-stop.txt','r+')
    stop = stopbestand.read()
    stopbestand.close()
    return stop
#
# lezen_temp
def lezen_temp():
    global temp_living
    global temp_water
    global temp_retour
    global temp_buiten
    temp_living = round(tempmodule_a.weerstand(1),1)
    print('1 : ',temp_living)
    temp_water = round(tempmodule_a.weerstand(2),1)
    print('2 : ',temp_water)
    temp_retour = round(tempmodule_a.weerstand(3),1)
    print('3 : ',temp_retour)
    temp_buiten = round(tempmodule_a.weerstand(4),1)
    print('4 : ',temp_buiten)
#    
#
# log_temp
def log_temp_titel():
#   week van het jaar in de bestandsnaam
    W=time.strftime('%W')
    bestandsnaam = '/home/pi/CSV/temperatuur-' + str(f'{int(W):02d}') + '.csv'
    csvBestand = open(bestandsnaam,'a')
#    csvBestand = open('/home/pi/CSV/temperatuur.csv','a')
    csvBestand.write('soort;tijd;jmd;week;dag;uur;ums;jmdums;living;water;retour;buiten;puls_oud;puls;aantal_sec;duur_vraag;CV-teller \n')
    csvBestand.close()
#
###################################################
#
# log_temp
def log_temp(soort,temp_living,temp_water,temp_retour,temp_buiten,puls_oud,puls,aantal_sec,duur_vraag,relais4,CVteller):
#   week van het jaar in de bestandsnaam
    W=time.strftime('%W')
    bestandsnaam = '/home/pi/CSV/temperatuur-' + str(f'{int(W):02d}') + '.csv'
    csvBestand = open(bestandsnaam,'a')
#    csvBestand = open('/home/pi/CSV/temperatuur.csv','a')

    temp_US_4 = str(temp_living)  + ';' + str(temp_water) + ';' + str(temp_retour) + ';' + str(temp_buiten) 
    temp_BE_4 = temp_US_4.replace(".",",")
    tijdnu = int(time.time())
    tijddag=[0,0,0]
    tijd.u_dag(tijddag)
    uur        = tijddag[0]
    combinatie = tijddag[1]
#   dag        = tijddag[2]
    duur_vr = int(duur_vraag)
    csvBestand.write('%s ; %s ; %s ; %s ; %s ; %s ; %s ; %s ; %s \n' %
                          (soort,
                           tijdnu,
                           tijddag[1],
                           temp_BE_4,
                           puls_oud,
                           puls,
                           aantal_sec,
                           duur_vr,CVteller
                           ))
    csvBestand.close()
    GPIO.output(relais4,0)  # opgelet CV,0 = aan
    time.sleep(1)
    GPIO.output(relais4,1)  # opgelet CV,1 = uit

##########################################################
# aantal pulsen bepalen per uur
# 12 pulsen per uur = om de 5 minuten
def aantal_pulsen():
    global temp_living
    global temp_water
    global temp_retour
    global temp_buiten
    global puls_oud
    global puls
    global duur_vraag
    global begin_vraag
    global LED2
    global geennachtverlaging
# in het begin is CV-water koud en is water-temp = retour-temp
    if temp_water < 35: 
        puls = 12
    else:
# als retour even warm is als water, is er niet veel warmte nodig
        puls = temp_water - temp_retour
        puls = round(puls,1)
        print("puls-temp : ", puls)
# geen negatieve pulsen !!!!
        if puls < 0:
            puls = 0
        if puls > 12:
            puls = 12
    print("puls1 : ", puls)
# grote nood aan warmte
    if temp_living < 18: 
        puls = puls
    else:
        if temp_living < 19:
            puls = puls - 1
        else:
            if temp_living < 20:
                puls = puls - 4
            else:
                if temp_living < 21:
                    puls = puls - 5
                else:
                    if temp_living < 21.5:
                        puls = puls - 6
                    else:
# vanaf 21° of 22°c werken met 1/2 graden ?
                        if temp_living < 22:
                            puls = puls - 7
                        else:
# vanaf 21° of 22°c werken met 1/2 graden ?
                            if temp_living < 22.5:
                                puls = puls - 8
                            else:
# vanaf 21° of 22°c werken met 1/2 graden ?
                                if temp_living < 23:
                                    puls = puls - 10
                                else:
                                    puls = puls - 12
    puls = round(puls,1)
# geen negatieve pulsen !!!!
    if puls < 0:
        puls = 0
    print("puls2  : ",puls)                    
# koud buiten : elke graad onder nul, verhoogt het aantal pulsen
# koud buiten : elke graad onder +5°C, verhoogt het aantal pulsen
    temp_b = temp_buiten - 5
    if temp_b < 0:
        puls = puls + abs(temp_b)
        puls = round(puls,1)
    print("puls3   : ",puls)                    
#
    if puls < 12:
        begin_vraag = int(time.time())
        LED2 = 0
# is de vraag al lang ?
# begin van de vraag
    if puls_oud < 12 and puls >= 12:
        begin_vraag = int(time.time())
# één uur vraag naar warmte : dus hoger regime
# enkel als het aantal pulse minimum 12 is
    duur_vraag = int(time.time()) - begin_vraag
    print('duur_vraag : ',duur_vraag)
    if duur_vraag > 3600 and duur_vraag <= 7200:
        if puls >= 12:
            puls = 24
            LED2 = 1
    print("puls4     : ",puls)                    
    print("duur_vraag : ",duur_vraag)                    
# hoog regime stopt na één uur
    if duur_vraag > 7200: 
        begin_vraag = int(time.time())
        LED2 = 0
#
# invloed van het moment van de dag 
# 's nacht : uit
# 's morgens : half
# 's namiddags : normaal
    t = time.localtime()
    uur = t[3]
    print("uur  : ",uur)                    
#
#uur =      5:00        10:00        15:00        20:00
#------------|------------|------------|------------|------------|
#puls = 0         1/3           1/2          1/1          0
#
#
#uur =    4:00       8:00      12:00      16:00      20:00
#----------|----------|----------|----------|----------|----------|
#puls = 0       1/5       1/3         1/2        1/1          0
#
#
#uur =    2:00       6:00      10:00      14:00      18:00
#----------|----------|----------|----------|----------|----------|
#puls = 0       1/4       1/2         1/1.5      1/1          0
#
    if uur < 2:
        print("nacht : uur<2 : ",uur)                    
        puls = 0
    else:
        if uur >= 18:
            print("nacht : uur>=18 : ",uur)                    
            puls = 0
        else:
#   voormiddag
            if uur < 6:
#               CVteller_old < 5 : gisteren werkte de CV niet, dus is alles koud
#                if CVteller_old < 5 or geennachtverlaging == 1:
                if CVteller_old < 5:
                    print("voormiddag : uur<6 : ",uur)                    
                    print("CVteller_old       : ",CVteller_old)                    
                    puls = puls / 2
                else:
                    print("voormiddag : uur<6 : ",uur)                    
                    print("CVteller_old       : ",CVteller_old)                    
                    puls = puls / 4
            else:
#   namiddag
                if uur < 10:
#                   CVteller_old < 5 : gisteren werkte de CV niet, dus is alles koud
#                    if CVteller_old < 5 or geennachtverlaging == 1:
                    if CVteller_old < 5:
                        print("voormiddag : uur<10 : ",uur)                    
                        print("CVteller_old        : ",CVteller_old)                    
                        puls = puls / 1.5
                    else:
                        print("voormiddag : uur<10 : ",uur)                    
                        print("CVteller_old        : ",CVteller_old)                    
                        puls = puls / 2
                else:
#   vooravond
                    if uur < 14:
                        print("voormiddag : uur<14 : ",uur)                    
                        puls = puls / 1.5
#   avond : geen vermindering
#
    print("puls5    : ",puls)                    
    puls = round(puls,1)
    print("puls6    : ",puls)                    
#
    print("puls7      : ",puls)                    
    if puls > 0 and puls < 1:
        puls = 1
    print("puls8      : ",puls)                    
    puls_oud = puls    
# beveiliging te hoge watertemperatuur
    if temp_water > 50:
        puls = 0
#    return puls_oud,puls,duur_vraag
#
log_temp_titel()
temp_living = 0.1
temp_water  = 0.1
temp_retour = 0.1
temp_buiten = 0.1
stookseizoen = 1
thermostaat = 1
puls_oud = 0.1
puls = 0.1
duur_vraag = 0
begin_vraag = int(time.time())
uur = 0
soort = "begin"
uur_old = 25
aantal_sec = 99
CVteller = 0
CVteller_old = 0
geennachtverlaging = 0 # 1 = geen nachtverlaging
stop = "run"
LED2 = 0 # verhoogde vermogen na één uur vraag, één uur lang
begin_vraag = int(time.time())
##########################################################
GPIO.output(led1,1)
time.sleep(1) 
GPIO.output(led1,0)
#
GPIO.output(led2,1)
time.sleep(1) 
GPIO.output(led2,0)
#
GPIO.output(relais2,0)  # opgelet kanaal2,0 = aan
time.sleep(1) 
GPIO.output(relais2,1)  # opgelet kanaal2,1 = uit
#
GPIO.output(relais3,0)  # opgelet kanaal3,0 = aan
time.sleep(1) 
GPIO.output(relais3,1)  # opgelet kanaal3,1 = uit
#
GPIO.output(relais4,0)  # opgelet kanaal4,0 = aan
time.sleep(1) 
GPIO.output(relais4,1)  # opgelet kanaal4,1 = uit
#
GPIO.output(CV,1)       # opgelet CV,1 = uit
#
stop = read_stop()
#
while stop != "stop" and stop != "reboot":

    GPIO.output(CV,1)  # opgelet CV,1 = uit
    GPIO.output(relais2,0)  # opgelet CV,0 = aan
    time.sleep(1)
    GPIO.output(relais2,1)  # opgelet CV,1 = uit

    lezen_temp()
    print('living : ',temp_living)
    print('water  : ',temp_water)
    print('retour : ',temp_retour)
    print('buiten : ',temp_buiten)

    stookseizoen = GPIO.input(stook)
    thermostaat  = GPIO.input(thermo)
    geennachtverlaging = GPIO.input(nacht)

    aantal_pulsen()
#    if LED2 == 0:
#        GPIO.output(led2,0)
#    else:
#        GPIO.output(led2,1)
        
#   de thermostaat living staat aan
    if stookseizoen == 0:
# nieuw begin
        begin_vraag = int(time.time())
        print("stookseizoen-uit")
        time.sleep(300) # om de 5 minuten temperatuur lezen
        soort = "stookseizoen-uit"
#        als seizoen uit is geen print om de 5 minuten
        log_temp(soort,temp_living,temp_water,temp_retour,temp_buiten,puls_oud,puls,aantal_sec,duur_vraag,relais4,CVteller)
    else:
        print("stookseizoen ON")
        if thermostaat == 0:
# nieuw begin
            begin_vraag = int(time.time())
            print("thermostaat uit")
            time.sleep(300) # om de 5 minuten temperatuur lezen
            soort = "thermostaat-uit"
#            als thermostaat uit is geen print om de 5 minuten
            log_temp(soort,temp_living,temp_water,temp_retour,temp_buiten,puls_oud,puls,aantal_sec,duur_vraag,relais4,CVteller)
        else:
            GPIO.output(relais3,0)  # opgelet CV,0 = aan
            time.sleep(1)
            GPIO.output(relais3,1)  # opgelet CV,1 = uit
            print("thermostaat ON")
            if puls > 0:
                print("puls > 0 : ",puls)
# aantal keren de CV aangestuurd wordt per dag
                CVteller = CVteller + 1
# te hoge watertemperatuur
                if temp_water > 50:
                    i = 1
                    while i < 6:
                        GPIO.output(led2,1)
                        time.sleep(1) 
                        GPIO.output(led2,0)
                        i += 1
#
                GPIO.output(CV,0)  # opgelet CV,0 = aan
                GPIO.output(led1,1)
                if LED2 == 1:
                    GPIO.output(led2,1)
                time.sleep(1) # LED-CV 1 sec aan
                GPIO.output(led1,0)
                GPIO.output(led2,0)
                time.sleep(89) # CV 1,5 minuten aan
                GPIO.output(CV,1)  # opgelet CV,1 = uit
                print("puls9      : ",puls)                    
                aantal_sec = int(3600 / puls)
                print("aantal_sec : ",aantal_sec)
#           na 1,5 minuten "aan", "x minuten" wachten tot minimum 5 minuten in normale omstandigheden
                wachttijd = aantal_sec - 90
                if wachttijd < 0:
                    wachttijd = 10 # 10 seconden
                print("wachttijd : ", wachttijd)    
                time.sleep(wachttijd)
                soort = "cv-aan"
                log_temp(soort,temp_living,temp_water,temp_retour,temp_buiten,puls_oud,puls,aantal_sec,duur_vraag,relais4,CVteller)
            else:
# nieuw begin
                begin_vraag = int(time.time())
                print("puls=0")
                time.sleep(300) # om de 5 minuten temperatuur lezen
                soort = "puls-zero"
#            als puls uit is geen print om de 5 minuten
                log_temp(soort,temp_living,temp_water,temp_retour,temp_buiten,puls_oud,puls,aantal_sec,duur_vraag,relais4,CVteller)


    t = time.localtime()
    uur = t[3]
    if uur_old != uur:
#   elk uur een logging
        soort1 = "uur-" + soort
        print("uur      : ",uur)                    
        print("soort1   : ",soort1)                    
        GPIO.output(led1,1)
        time.sleep(1) 
        GPIO.output(led1,0)
#
        if uur == 0:
#   nieuwe titel voor nieuw weekbestand
#   week van het jaar in de bestandsnaam
            log_temp_titel()
#
        log_temp(soort1,temp_living,temp_water,temp_retour,temp_buiten,puls_oud,puls,aantal_sec,duur_vraag,relais4,CVteller)
        if uur == 0:
# heeft de CV gisteren gewerkt ?
            CVteller_old = CVteller
            CVteller = 0
        uur_old = uur
#
    stop = read_stop()
#
GPIO.output(CV,1)  # opgelet CV,1 = uit
time.sleep(1) 
GPIO.cleanup()
time.sleep(1) 
if stop == "reboot":
    os.system("sudo reboot now")