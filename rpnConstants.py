#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnConstants.py
# //
# //  RPN command-line calculator constant operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

# Conway's constant:  OEIS A014715
# 1.30357726903429639125709911215255189073070250465940487575486139062855088785246155712681576686442522555

# http://en.wikipedia.org/wiki/Universal_parabolic_constant

# http://primes.utm.edu/glossary/xpage/BrunsConstant.html


# Name        Value           Unit            Description
# R           8.3144621       J / (K mol)     Gas constant
# R_earth     6378136         m               Earth equatorial radius
# R_jup       71492000        m               Jupiter equatorial radius
# R_sun       695508000       m               Solar radius
# Ryd         10973731.6      1 / (m)         Rydberg constant
# a0          5.29177211e-11  m               Bohr radius
# b_wien      0.0028977721    m K             Wien wavelength displacement law constant
# e           1.60217657e-19  C               Electron charge
# eps0        8.85418782e-12  F/m             Electric constant
# m_e         9.10938291e-31  kg              Electron mass
# m_n         1.67492735e-27  kg              Neutron mass
# m_p         1.67262178e-27  kg              Proton mass
# mu0         1.25663706e-06  N/A2            Magnetic constant
# muB         9.27400968e-24  J/T             Bohr magneton
# pc          3.08567758e+16  m               Parsec
# sigma_sb    5.670373e-08    W / (K4 m2)     Stefan-Boltzmann constant
# u           1.66053892e-27  kg              Atomic mass

from mpmath import *

from rpnInput import convertToBase10
from rpnMeasurement import RPNMeasurement
from rpnOutput import convertToBaseN
from rpnPrimeUtils import *
from rpnUtils import *


# //******************************************************************************
# //
# //  getAvogadrosNumber
# //
# //  Based on CODATA 2014
# //
# //******************************************************************************

def getAvogadrosNumber( ):
    return mpf( '6.022140857e23' )


# //******************************************************************************
# //
# //  getPlasticConstant
# //
# //******************************************************************************

def getPlasticConstant( ):
    term = fmul( 12, sqrt( 69 ) )
    return fdiv( fadd( cbrt( fadd( 108, term ) ), cbrt( fsub( 108, term ) ) ), 6 )


# //******************************************************************************
# //
# //  getMillsConstant
# //
# //  http://primes.utm.edu/notes/MillsConstant.html
# //
# //******************************************************************************

def getMillsConstant( ):
    mills = '''
1.3063778838 6308069046 8614492602 6057129167 8458515671 3644368053 7599664340
5376682659 8821501403 7011973957 0729696093 8103086882 2388614478 1635348688
7133922146 1943534578 7110033188 1405093575 3558319326 4801721383 2361522359
0622186016 1085667905 7215197976 0951619929 5279707992 5631721527 8412371307
6584911245 6317518426 3310565215 3513186684 1550790793 7238592335 2208421842
0405320517 6890260257 9344300869 5290636205 6989687262 1227499787 6664385157
6619143877 2844982077 5905648255 6091500412 3788524793 6260880466 8815406437
4425340131 0736114409 4137650364 3793012676 7211713103 0265228386 6154666880
4874760951 4410790754 0698417260 3473107746 7757406400 7810935083 4214374426
5420408531 1165490420 9930908557 4705834879 3757769523 3363648583 0549292738
7281493416 7412502732 6692684046 8154062676 3113223748 8238001180 4120628601
3841914438 8571516091 8938894478 9912125543 3847493590 9274442208 2802260203
3230271063 7502228813 1064778444 8170037233 3640604211 8742608383 3282217696
8781235304 9623008802 6722111040 1606508880 9718347778 3140224908 2184410637
7494000232 8241927007 1233303228 8541285840 8891631372 9295257781 6697309365
1795130470 1393525757 0572884159 9173150678 1288275420 0054622901 2628840580
6701552761 7432706316 2570558788 5293887371 6636318690 9678515848 0771725887
5035917556 1065153430 4682508915 7205292189 7945191865 6896107079 6794540918
0039893947 2486242136 2610780178 5354328900 4499330170 4963668241 3899155939
0863407971 5195210549 1383217875 0248935369 4369110072 7103037261 3750972234
2853231161 6862854394 4188065497 7907392376 1870914189 9171623410 9416383085
7574665951 4814198482 6963646512 3058093661 7898571875 2925589242 6179224596
0356189889 9454332955 3439088187 6592175906 9313497049 8201200298 1508269262
7739578666 5803814559 1108464886 1104685164 0734818557 7243382357 5351063523
0787534450 3736037838 1461950587 4443769595 4021414795 8591467765 9154549440
1109935654 8107725039 6717552839 5344823084 6065578286 8128968938 4614534165
2594710453 0618465557 0366212320 9381911768 1038123324 7253675736 5613040357
5560454761 3371766377 2669711171 8349597802 9379922544 2693282380 1446278547
1209936042 6343210060 6793068847 2340905417 6649612578 1876587122 7138054411
0284476782 7220830725 4218662463 6671401392 0833251680 3107194312 3534390037
3354336266 7688155625 9057587385 2974777343 7738355179 7994120752 9586192686
6856592393 9379440444 1199237410 4665470412 5007296505 6228921055 9394937378
6719583516 9837540168 1664617904 3331648046 5451455123 9786534043 7768447978
5822396096 2567035174 4060523085 1627314291 7789552042 9361197121 8935941751
1822684797 3171994768 9696857464 6542612093 1681370355 4549047302 7842694285
0527742998 3011910840 5852525490 6569366849 1805206022 7862098426 1889432232
7333296288 7985907514 8028436448 1020972122 2062851531 7791526533 7924057130
3754370370 5973473936 5236591179 5290648972 6355555552 2455538616 9027564729
7606203459 7864419595 5284059662 2042692870 1556807231 2327295604 9197275555
1173811743 9498041178 2562100358 0987486943 4916176191 1412957068 4583855277
2863501841 9846633751 2703652944 4439179207 8880546317 7615625056 5779654136
8667966193 8033113000 9197428721 1056334476 2934713049 6591577215 7491354752
7750522281 5477233978 2701206715 6134696675 2804453952 8831111372 5233005379
2614609357 4104273863 1248018639 0768802945 0769952383 9844861429 4191476796
5526689640 4947866568 2961301301 6754386070 9006829296 1653932904 6429713441
7920597606 3902545223 5699550030 5207119585 0888436123 9568280608 2631478860
0212196350 9684204891 3975736162 0582728000 2881499998 4626531583 7340424306
5745146181 9092160709 0999464130 0395781238 8002653463 7749856602 1304989308
6606386016 7711749535 9137939969 8572420298 6141711750 8417496946 0207541319
7419292673 8322336969 4366447594 9535945764 1825039184 1648406526 8129703655
2431649131 5705886920 1706784764 9891920503 4524317771 0382510270 0461527907
4415333590 3760320635 6958144883 4397045748 0747191673 0548810370 2038073973
3012545080 6753862371 8110488187 9417763684 0677050381 9025075958 3527842546
0267588421 7860226294 2258759036 0328933004 7370835123 4243128370 2275223680
1942128044 2334584092 1478125915 5393762375 0349951252 0250353974 0951855001
1784546409 8236141490 1101438550 9097799760 4527250817 0283560657 4395318910
6383508596 3526022951 3451047445 8938326912 3709949467 4629049061 6491522924
5946703198 1572295275 4433366943 6973758769 2027052974 9329485994 8444531112
0001696102 9053191932 4231669808 9865355152 1161524308 8017719669 0349426332
5875165319 4532207576 0326737735 0890963423 7709149472 3463304853 2817149136
6374278165 8034409201 4364436374 4142587515 6889725905 7597652435 5903773395
8553668812 7814136070 7455755974 5834337002 0618899443 4960548072 4879707723
7757577836 3768547779 7660031287 4520669041 8122545225 9669049728 8818902552
4207452807 8789766062 7057012974 4242360519 1625086793 6339025816 6214283741
9236183835 5963898395 6219707223 8370164172 4130153727 9414272047 8835725712
2491981038 0563509271 7683265524 6336425039 3548743536 6214009638 4385067048
4674827332 9440551876 4731061063 5933353896 9800878455 2888808827 5895565365
1575416672 7389528467 3350028205 2735787205 9577464783 9569714478 3863673824
6635935589 7526984469 4518267167 8872736358 6493481839 9661995116 9223252371
3190825898 9790684856 7923797569 5062812946 4604481007 7136511563 8515655498
7043852085 1739260224 0423685187 5777187118 3216743520 7471018378 5603902974
0241020021 3594027613 0313048350 8299596886 9314857444 3720877611 2596829187
4493706521 6856433203 8869270998 2044671637 6366319501 9576600990 2366660881
8680048958 6739491792 6632371296 7806856317 0434284142 5814694044 4748789412
5072706802 8264884747 9528961522 0168417395 9869700459 1313783325 7497053317
5789641524 5432580622 1056598065 7088915582 7539380090 3820251277 3782112879
0944743435 7698080225 8756344089 9915149346 3081175708 7842846402 7551937639
8088671537 3698546330 6927473302 9892281607 1686850580 6448158298 9824058861
4659869903 2059023965 8939155655 7584016919 1025711877 4272715134 3202915748
6196601246 6957459004 6276063059 4646774548 1144196025 3660028441 5427826762
9593334455 1485763794 0237005116 6231636745 6317158182 5468449292 5582361972
1258859381 2550247928 5870666810 4669132652 6742894535 6205108835 8027618840
5574854937 3761590740 8924272755 7916553354 5420700063 2937083181 5974640003
8113080930 5288843535 5773535898 5594979444 4632848488 3408971205 9352154982
9882918987 6847064787 6385207690 4724706664 5816369514 7119010050 2014432987
6805116217 1574160574 8439514042 3548295613 8115060443 0662331808 5817279115
8346447898 7048554751 7440088915 2210972581 3891705672 7586684466 4004055698
7305493686 3405913311 9684646658 1638268121 7100998412 8476714252 6332319404
9631673095 4579660549 2710935088 5466276364 0691865617 9431034302 2042375220
3827722179 5325652555 1904146485 0532853575 3523799670 6188326965 6903798944
1895208781 8808745146 6207990015 2995562530 2605418936 6117026791 8826083198
9450025708 8130525289 6894977764 1124868829 2760755881 4507773131 7588025395
7553225667 2933146884 5113607860 8223722939 0258048670 7922641593 1804248190
4042020682 1539261419 4428119205 1812811382 1528108707 1387651523 2430899385
6330857983 7140840314 6426701075 5656427539 1749832684 3463406445 6155803691
8667914797 9806163224 3905779666 5989360162 4040280996 3846427106 3576288505
3766245609 0881943230 0116637584 7963231032 9538234572 3128011374 9644093988
2446584456 0552393937 1114632419 4901740423 3810657009 5553284142 9577270781
6777791288 1511926511 4237841584 0787995981 2399295139 8684353191 1072954395
4252242366 7227592898 0816145349 4496612806 9895474389 4519854008 6840135
'''

    return mpf( ''.join( [ i for i in mills if i not in ' \n' ] ) )


# //******************************************************************************
# //
# //  getChampernowneConstant
# //
# //  This function creates the Champernowne constant for the input base.
# //
# //******************************************************************************

def getChampernowneConstant( ):
    result = ''

    count = 1

    while len( result ) <= mp.dps:
        result += convertToBaseN( count, g.inputRadix, False, g.defaultNumerals )
        count += 1

    return convertToBase10( '0', result, g.inputRadix )


# //******************************************************************************
# //
# //  getCopelandErdosConstant
# //
# //******************************************************************************

def getCopelandErdosConstant( ):
    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += str( getNthPrime( count ) )
        count += 1

    return convertToBase10( '0', result, 10 )


# //******************************************************************************
# //
# //  getPrevostConstant
# //
# //  https://en.wikipedia.org/wiki/Mathematical_constants_and_functions
# //
# //******************************************************************************

def getPrevostConstant( ):
    return nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] )


# //******************************************************************************
# //
# //  getRobbinsConstant
# //
# //  https://en.wikipedia.org/wiki/Robbins_constant
# //
# //******************************************************************************

def getRobbinsConstant( ):
    robbins = fsub( fsub( fadd( 4, fmul( 17, sqrt( 2 ) ) ), fmul( 6, sqrt( 3 ) ) ), fmul( 7, pi ) )
    robbins = fdiv( robbins, 105 )
    robbins = fadd( robbins, fdiv( log( fadd( 1, sqrt( 2 ) ) ), 5 ) )
    robbins = fadd( robbins, fdiv( fmul( 2, log( fadd( 2, sqrt( 3 ) ) ) ), 5 ) )

    return robbins


# //******************************************************************************
# //
# //  getMagneticConstant
# //
# //  https://en.wikipedia.org/wiki/Vacuum_permeability
# //
# //******************************************************************************

def getMagneticConstant( ):
    return RPNMeasurement( fprod( [ 4, pi, power( 10, -7 ) ] ), [ { 'newton' : 1 }, { 'ampere' : -2 } ] )


# //******************************************************************************
# //
# //  getNewtonsConstant
# //
# //  https://en.wikipedia.org/wiki/Gravitational_constant
# //
# //  updated value based on CODATA 2014
# //
# //******************************************************************************

def getNewtonsConstant( ):
    return RPNMeasurement( mpmathify( '6.67408e-11' ), [ { 'meter' : 3 }, { 'kilogram' : -1 }, { 'second' : -2 } ] )



#
#    'moon_gravity' :
#        UnitInfo( 'acceleration', 'moon_gravity', 'moon_gravities', '', [ 'moon_g' ], [ 'natural' ],
#                  '''The equivalent surface gravity on the moon.''' ),
#
#    'standard_gravity' :
#        UnitInfo( 'acceleration', 'standard_gravity', 'standard_gravities', 'G', [ 'grav', 'gee' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'electron_charge' :
#        UnitInfo( 'charge', 'electron_charge', 'electron_charges', '', [ 'elementary_charge', 'proton_charge' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'density_of_water' :
#        UnitInfo( 'density', 'x density_of_water', 'x density_of_water', '', [ 'water' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'impedance_of_free_space' :
#        UnitInfo( 'electrical_resistance', 'impedance_of_free_space', 'x impedance_of_free_space', 'Z0', [ 'vacuum_impedence' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'jupiter_radius' :
#        UnitInfo( 'length', 'jupiter_radius', 'jupiter_radii', 'Rjov', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'solar_radius' :
#        UnitInfo( 'length', 'solar_radius', 'solar_radii', 'Rsol', [ 'sun_radius', 'sun_radii' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'solar_mass' :
#        UnitInfo( 'mass', 'solar_mass', 'solar_masses', 'Msol', [ 'sun_mass', 'sun_masses' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    # particle masses
#
#    'alpha_particle_mass' :
#        UnitInfo( 'mass', 'alpha_particle_mass', 'alpha_particle_masses', '', [ 'alpha_mass', 'alpha_masses' ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'deuteron_mass' :
#        UnitInfo( 'mass', 'deuteron_mass', 'deuteron_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'electron_mass' :
#        UnitInfo( 'mass', 'electron_mass', 'electron_masses', '', [ 'electron_rest_mass', 'electron_rest_masses' ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'helion_mass' :
#        UnitInfo( 'mass', 'helion_mass', 'helion_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'proton_mass' :
#        UnitInfo( 'mass', 'proton_mass', 'proton_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'muon_mass' :
#        UnitInfo( 'mass', 'muon_mass', 'muon_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'neutron_mass' :
#        UnitInfo( 'mass', 'neutron_mass', 'neutron_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'proton_mass' :
#        UnitInfo( 'mass', 'proton_mass', 'proton_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'tau_mass' :
#        UnitInfo( 'mass', 'tau_mass', 'tau_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    'triton_mass' :
#        UnitInfo( 'mass', 'triton_mass', 'triton_masses', '', [ ], [ 'natural', 'science' ],
#                  '''
#                  ''' ),
#
#    # planet masses
#
#    'mercury_mass' :
#        UnitInfo( 'mass', 'mercury_mass', 'mercury_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'venus_mass' :
#        UnitInfo( 'mass', 'venus_mass', 'venus_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'earth_mass' :
#        UnitInfo( 'mass', 'earth_mass', 'earth_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'earth_moon_mass' :
#        UnitInfo( 'mass', 'earth_moon_mass', 'earth_moon_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'mars_mass' :
#        UnitInfo( 'mass', 'mars_mass', 'mars_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'jupiter_mass' :
#        UnitInfo( 'mass', 'jupiter_mass', 'jupiter_masses', 'Mjov', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'saturn_mass' :
#        UnitInfo( 'mass', 'saturn_mass', 'saturn_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'uranus_mass' :
#        UnitInfo( 'mass', 'uranus_mass', 'uranus_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'neptune_mass' :
#        UnitInfo( 'mass', 'neptune_mass', 'neptune_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'pluto_mass' :
#        UnitInfo( 'mass', 'pluto_mass', 'pluto_masses', '', [ ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#
#    'solar_luminosity' :
#        UnitInfo( 'power', 'solar_luminosity', 'solar_luminosities', '', [ 'solar_output' ], [ 'natural' ],
#                  '''
#                  ''' ),
#
#    'lunar_day' :
#        UnitInfo( 'time', 'lunar_day', 'lunar_days', '', [ 'tidal_day', 'tidal_days' ], [ 'science' ],
#                  '''
#                  ''' ),
#
#
#    # planet days
#
#    'mercury_day' :
#        UnitInfo( 'time', 'mercury_day', 'mercury_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'venus_day' :
#        UnitInfo( 'time', 'venus_day', 'venus_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'mars_day' :
#        UnitInfo( 'time', 'mars_day', 'mars_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'jupiter_day' :
#        UnitInfo( 'time', 'jupiter_day', 'jupiter_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'saturn_day' :
#        UnitInfo( 'time', 'saturn_day', 'saturn_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'uranus_day' :
#        UnitInfo( 'time', 'uranus_day', 'uranus_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'neptune_day' :
#        UnitInfo( 'time', 'neptune_day', 'neptune_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'pluto_day' :
#        UnitInfo( 'time', 'pluto_day', 'pluto_days', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    # planet years
#
#    'mercury_year' :
#        UnitInfo( 'time', 'mercury_year', 'mercury_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'venus_year' :
#        UnitInfo( 'time', 'venus_year', 'venus_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'mars_year' :
#        UnitInfo( 'time', 'mars_year', 'mars_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'jupiter_year' :
#        UnitInfo( 'time', 'jupiter_year', 'jupiter_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'saturn_year' :
#        UnitInfo( 'time', 'saturn_year', 'saturn_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'uranus_year' :
#        UnitInfo( 'time', 'uranus_year', 'uranus_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'neptune_year' :
#        UnitInfo( 'time', 'neptune_year', 'neptune_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    'pluto_year' :
#        UnitInfo( 'time', 'pluto_year', 'pluto_years', '', [ ], [ 'science' ],
#                  '''
#                  ''' ),
#
#    ( 'jupiter_day',                'day' )                                 : mpmathify( '0.41354' ),
#    ( 'jupiter_radius',             'meter' )                               : mpmathify( '7.1492e7' ),
#    ( 'jupiter_year',               'year' )                                : mpmathify( '11.862615' ),
#    ( 'mars_day',                   'day' )                                 : mpmathify( '1.02595675' ),
#    ( 'mars_year',                  'year' )                                : mpmathify( '1.8808476' ),
#    ( 'mercury_day',                'day' )                                 : mpmathify( '58.6462' ),
#    ( 'mercury_year',               'year' )                                : mpmathify( '0.2408467' ),
#    ( 'neptune_day',                'day' )                                 : mpmathify( '0.768' ),
#    ( 'neptune_year',               'year' )                                : mpmathify( '164.79132' ),
#    ( 'pluto_day',                  'day' )                                 : mpmathify( '6.3867' ),
#    ( 'pluto_year',                 'year' )                                : mpmathify( '247.92065' ),
#    ( 'saturn_day',                 'day' )                                 : mpmathify( '0.4375' ),
#    ( 'saturn_year',                'year' )                                : mpmathify( '29.447498' ),
#    ( 'uranus_day',                 'day' )                                 : mpmathify( '0.65' ),
#    ( 'uranus_year',                'year' )                                : mpmathify( '84.016846' ),
#    ( 'venus_day',                  'day' )                                 : mpmathify( '243.01' ),
#    ( 'venus_year',                 'year' )                                : mpmathify( '0.61519726' ),
#    ( 'lunar_day',                  'minute' )                              : mpmathify( '1490' ),
#
#    ( 'solar_luminosity',           'watt' )                                : mpmathify( '3.826e26' ),
#    ( 'solar_mass',                 'earth_moon_mass' )                     : mpmathify( '328900.56' ), # 0.02
#    ( 'solar_mass',                 'gram' )                                : mpmathify( '1.9891e33' ),
#    ( 'solar_mass',                 'jupiter_mass' )                        : mpmathify( '1047.3486' ), # 0.0008
#    ( 'solar_mass',                 'mars_mass' )                           : mpmathify( '3098708' ),   # 9
#    ( 'solar_mass',                 'mercury_mass' )                        : mpmathify( '6023600' ),   # 250
#    ( 'solar_mass',                 'neptune_mass' )                        : mpmathify( '19412.24' ),  # 0.04
#    ( 'solar_mass',                 'pluto_mass' )                          : mpmathify( '1.35e8' ),    # 0.07e8
#    ( 'solar_mass',                 'saturn_mass' )                         : mpmathify( '3497.898' ),  # 0.018
#    ( 'solar_mass',                 'uranus_mass' )                         : mpmathify( '22902.98' ),  # 0.03
#    ( 'solar_mass',                 'venus_mass' )                          : mpmathify( '408523.71' ), # 0.06
#    ( 'solar_radius',               'meter' )                               : mpmathify( '6.9599e8' ),
#
#    ( 'alpha_particle_mass',        'dalton' )                              : mpmathify( '4.001506179125' ),
#    ( 'electron_mass',              'gram' )                                : mpmathify( '9.10938291e-28' ),
#    ( 'earth_mass',                 'gram' )                                : mpmathify( '5.9742e27' ),
#    ( 'deuteron_mass',              'dalton' )                              : mpmathify( '2.013553212712' ),
#    ( 'earth_radius',               'meter' )                               : mpmathify( '6378136' ),
#    ( 'helion_mass',                'dalton' )                              : mpmathify( '3.0149322468' ),
#    ( 'neutron_mass',               'dalton' )                              : mpmathify( '1.00866491600' ),
#    ( 'muon_mass',                  'dalton' )                              : mpmathify( '0.1134289267' ),
#    ( 'proton_mass',                'dalton' )                              : mpmathify( '1.007276466812' ),
#    ( 'proton_mass',                'gram' )                                : mpmathify( '1.6726218e-24' ),
#    ( 'tau_mass',                   'dalton' )                              : mpmathify( '1.90749' ),
#    ( 'triton_mass',                'dalton' )                              : mpmathify( '3.0155007134' ),
#    ( 'bohr_radius',                'meter' )                               : mpmathify( '5.2917721e-11' ),
#    ( 'von_klitzing_constant',      'ohm' )                                 : mpmathify( '25812.807557' ),
#    ( 'planck_area',                'square_meter' )                        : mpmathify( '2.6121003e-70' ),
#    ( 'planck_charge',              'coulomb' )                             : mpmathify( '1.875545956e-18' ),
#    ( 'planck_energy',              'joule' )                               : mpmathify( '1.956e9' ),
#    ( 'planck_length',              'meter' )                               : mpmathify( '1.616199e-35' ),
#    ( 'planck_mass',                'gram' )                                : mpmathify( '2.17651e-8' ),
#    ( 'planck_time',                'second' )                              : mpmathify( '5.39106e-44' ),
#    ( 'planck_volume',              'cubic_meter' )                         : mpmathify( '4.22419e-105' ),
#    ( 'electron_charge',            'coulomb' )                             : mpmathify( '1.602176565e-19' ),
#    ( 'gallon_of_gasoline',         'gallon_of_ethanol' )                   : mpmathify( '1.425' ),  # approx.
#    ( 'gallon_of_gasoline',         'joule' )                               : mpmathify( '1.2e8' ),  # approx. obviously
#    ( 'aa_battery',                 'joule' )                               : mpmathify( '15400' ),
#    ( 'alpha'                       'unity' )                               : mpmathify( '0.0072973526' ),
#    ( 'moon_gravity'                'meter/second^2' )                      : mpmathify( '1.62' ),


#  http://www.numericana.com/answer/constants.htm
#  (2014-05-15)    1-1/e  =  0.632120558828557678404476229838539...
#  Rise time and fixed-point probability:  1/1! - 1/2! + 1/3! - 1/4! + 1/5! - ...


