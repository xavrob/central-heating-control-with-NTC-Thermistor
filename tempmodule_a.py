#tempmodule-a - het lezen van temperatuur
#met NTC
#VCC(+) 3,3V
#SDA=GPIO02
#SCL=GPIO03
#GND(-)
#pull-down 10K


def weerstand(ruimte=0):
#   ruimte 1 t/m 4 (4 kanalen)
    import ohm
    import board
    import busio
    import adafruit_ads1x15.ads1015 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1015(i2c)

    temperature = 99
# indien nodig krijgt elke ruimte-voeler zijn eigen parameters 
# afhankelijk van de weerstanden van de leidingen
    Vmax     = 3.3
    Ohm_100  = 1.0
    Ohm_0    = 26.0
    Ohm_vast = 10.0
    Ohm      = 1.0
    volt     = 1.0

#    print('ruimte : ',ruimte)
    if ruimte == 1:
# living
        chan1 = AnalogIn(ads, ADS.P0) 
        waarde = chan1.value
        volt   = chan1.voltage
#        print('living : ', waarde, volt)
    elif ruimte == 2:
# water
        chan2 = AnalogIn(ads, ADS.P1) 
        waarde = chan2.value
        volt   = chan2.voltage
#        print('water  : ', waarde, volt)
    elif ruimte == 3:
# retour
        chan3 = AnalogIn(ads, ADS.P2) 
        waarde = chan3.value
        volt   = chan3.voltage
#        print('retour  : ', waarde, volt)
    elif ruimte == 4:
#buiten
        chan4 = AnalogIn(ads, ADS.P3) 
        waarde = chan4.value
        volt   = chan4.voltage
#        print('buiten : ', waarde, volt)
    else:
#        print('ruimte fout : ', ruimte)
        pass

#    print('Ohm         :',Ohm)
#    print('Ohm_vast    :',Ohm_vast)
#    print('Volt        :',volt)
#    print('Vmax        :',Vmax)
    if volt == 0:
        temperature = 99
    else:
        Ohm      = ((Vmax * Ohm_vast) / volt) - Ohm_vast
#        print('Ohm         :',Ohm)
    
    
        temperature = ohm.graden(Ohm)
#    print('temperature :',temperature)

#    print('done')
    return temperature