# ohm.py
def graden(weerstanden=270):
        
        import time
        #import tempmodule-a
        temperatuur = -40.01
        tijd = time.time()
        print('tijd : ',tijd)
        
        #while True:
        
        #    temperatuur = tempmodule-a.graden(1)
        #    print('1 : ',temperatuur)
        
        #    tijd = time.time()
        #    print('tijd : ',tijd)    
        #    time.sleep(1)
        
#        weerstand = 11
        
        #tabel = [-40, 0
        #         -39, 1
        #         -38, 2
        #         -37, 3
        #         -36, 4
        #         -35, 5
        #         -34, 6
        #         -33] 7
        
        tabel = [
                277.2,
                 263.6,
                 250.1,
                 236.8,
                 224,
                 211.5,
                 199.6,
                 188.1,
                 177.3,
                 167,
                 157.2,
                 148.1,
                 139.4,
                 131.3,
                 123.7,
                 116.6,
                 110,
                 103.7,
                 97.9,
                 92.5,
                 87.43,
                 82.79,
                 78.44,
                 74.36,
                 70.53,
                 66.92,
                 63.54,
                 60.34,
                 57.33,
                 54.5,
                 51.82,
                 49.28,
                 46.89,
                 44.62,
                 42.48,
                 40.45,
                 38.53,
                 36.7,
                 34.97,
                 33.33,
                 31.77,
                 30.25,
                 28.82,
                 27.45,
                 26.16,
                 24.94,
                 23.77,
                 22.67,
                 21.62,
                 20.63,
                 19.68,
                 18.78,
                 17.93,
                 17.12,
                 16.35,
                 15.62,
                 14.93,
                 14.26,
                 13.63,
                 13.04,
                 12.47,
                 11.92,
                 11.41,
                 10.91,
                 10.45,
                 10,
                 9.575,
                 9.17,
                 8.784,
                 8.416,
                 8.064,
                 7.73,
                 7.41,
                 7.106,
                 6.815,
                 6.538,
                 6.273,
                 6.02,
                 5.778,
                 5.548,
                 5.327,
                 5.117,
                 4.915,
                 4.723,
                 4.539,
                 4.363,
                 4.195,
                 4.034,
                 3.88,
                 3.733,
                 3.592,
                 3.457,
                 3.328,
                 3.204,
                 3.086,
                 2.972,
                 2.863,
                 2.759,
                 2.659,
                 2.564,
                 2.472,
                 2.384,
                 2.299,
                 2.218,
                 2.141,
                 2.066,
                 1.994,
                 1.926,
                 1.86,
                 1.796,
                 1.735,
                 1.677,
                 1.621,
                 1.567,
                 1.515,
                 1.465,
                 1.417,
                 1.371,
                 1.326,
                 1.284,
                 1.243,
                 1.203,
                 1.165,
                 1.128,
                 1.093,
                 1.059,
                 1.027,
                 0.9955,
                 0.9654,
                 0.9363,
                 0.9083,
                 0.8812,
                 0.855,
                 0.8297,
                 0.8052,
                 0.7816,
                 0.7587,
                 0.7366,
                 0.7152,
                 0.6945,
                 0.6744,
                 0.6558,
                 0.6376,
                 0.6199,
                 0.6026,
                 0.5858,
                 0.5694,
                 0.5535,
                 0.538,
                 0.5229,
                 0.5083,
                 0.4941,
                 0.4803,
                 0.4669,
                 0.4539,
                 0.4412,
                 0.429,
                 0.4171,
                 0.4055,
                 0.3944,
                 0.3835,
                 0.373,
                 0.3628,
                 0.353,
                 0.3434,
                 0.3341,
                 0.3253,
                 0.3167,
                 0.3083,
                 0.3002,
                 0.2924,
                 0.2848,
                 0.2774,
                 0.2702,
                 0.2633,
                 0.2565,
                 0.25,
                 0.2437,
                 0.2375,
                 0.2316,
                 0.2258,
                 0.2202,
                 0.2148,
                 0.2095,
                 0.2044,
                 0.1994,
                 0.1946,
                 0.19,
                 0.1855,
                 0.1811,
                 0.1769,
                 0.1728,
                 0.1688,
                 0.165,
                 0.1612,
                 0.1576,
                 0.1541,
                 0.1507,
                 0.1474,
                 0.1441,
                 0.141,
                 0.1379,
                 0.135,
                 0.1321,
                 0.1293,
                 0.1265,
                 0.1239,
                 0.1213,
                 0.1187,
                 0.1163,
                 0.1139,
                 0.1115,
                 0.1092,
                 0.107,
                 0.1048,
                 0.1027,
                 0.1006,
                 0.0986,
                 0.0966,
                 0.0947,
                 0.0928,
                 0.0909,
                 0.0891,
                 0.0873,
                 0.0856,
                 0.0839,
                 0.0822,
                 0.0806,
                 0.079,
                 0.0774,
                 0.0759,
                 0.0743,
                 0.0729,
                 0.0714,
                 0.07,
                 0.0686,
                 0.0672,
                 0.0658,
                 0.0645,
                 0.0631,
                 0.0619
        ]

# weerstand zoeken in tabel/lijst
# index is de temperatuur
# verfijning gebeurt door in verhouding een tussen waarde te vinden

        i = 0
        while i < 200:
        #    print('weerstand : ',weerstand)
                if weerstanden < tabel[i]:
        #        print('tabel i : ',tabel[i])
                        i += 1
        #        print('i : ',i)
        #        print('tabel  i+1: ',tabel[i])
        #        time.sleep(1)
                else:
# waarde gevonden
                        temperatuur = i - 40
        #        print(temp)
        #        time.sleep(1)
        #        print(tabel[i-1])
        #        print(tabel[i])
# verhouding tussen temperatuut(i) en temperatuur(i-1)
                        dif = tabel[i-1] - tabel[i]
        #        print(dif)
                        dif2 = tabel[i-1] - weerstanden
        #        print(dif2)
                        temperatuur = i - 1 + (dif2/dif) - 40
                        break
        
        print(temperatuur)
        tijd = time.time()
        print('tijd : ',tijd)        
 
        #    print('done')
        return temperatuur