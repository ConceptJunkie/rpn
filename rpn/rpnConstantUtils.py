#!/usr/bin/env python

#******************************************************************************
#
#  rpnConstantUtils.py
#
#  rpnChilada constant operator utilities
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

# Conway's constant:  OEIS A014715
# 1.30357726903429639125709911215255189073070250465940487575486139062855088785246155712681576686442522555

# http://en.wikipedia.org/wiki/Universal_parabolic_constant

# http://primes.utm.edu/glossary/xpage/BrunsConstant.html

from functools import lru_cache
from mpmath import arange, cbrt, fadd, fdiv, fmul, fsub, log, mp, mpf, mpmathify, pi, sqrt

from rpn.rpnComputer import interpretAsDouble, interpretAsFloat
from rpn.rpnInput import convertToBase10
from rpn.rpnList import getProduct
from rpn.rpnMath import getPower, getRoot
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnNumberTheory import getNthThueMorseNumber
from rpn.rpnOutput import convertToBaseN
from rpn.rpnPrimeUtils import getNthPrime

import rpn.rpnGlobals as g


#******************************************************************************
#
#  loadGlobaConstants
#
#******************************************************************************

def loadGlobalConstants( ):
    g.c = getConstant( 'speed_of_light'  )
    g.e = getConstant( 'electron_charge' )
    g.e0 = getConstant( 'electric_constant' )
    g.G = getConstant( 'newton_constant' )
    g.h = getConstant( 'planck_constant' )
    g.h_bar = getConstant( 'reduced_planck_constant' )
    g.k = getConstant( 'boltzmann_constant' )


#******************************************************************************
#
#  getConstant
#
#******************************************************************************

def getConstant( name ):
    if name not in g.constantOperators:
        raise ValueError( 'Invalid constant: ', name )

    unit = g.constantOperators[ name ].unit
    value = g.constantOperators[ name ].value

    if unit == '':
        return mpmathify( value )

    return RPNMeasurement( value, unit )


#******************************************************************************
#
#  getPlasticConstant
#
#******************************************************************************

def getPlasticConstant( ):
    '''Computes and returns the Plastic constant.'''
    term = fmul( 12, sqrt( 69 ) )
    return fdiv( fadd( cbrt( fadd( 108, term ) ), cbrt( fsub( 108, term ) ) ), 6 )


#******************************************************************************
#
#  getMillsConstant
#
#  http://primes.utm.edu/notes/MillsConstant.html
#
#******************************************************************************

@lru_cache( 1 )
def getMillsConstant( ):
    '''The Mills constant is hard-coded.'''
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


#******************************************************************************
#
#  getChampernowneConstant
#
#******************************************************************************

def getChampernowneConstant( ):
    '''This function creates the Champernowne constant for the input base.'''
    result = ''

    count = 1

    while len( result ) <= mp.dps:
        result += convertToBaseN( count, g.inputRadix )
        count += 1

    return convertToBase10( '0', result, g.inputRadix )


#******************************************************************************
#
#  getCopelandErdosConstant
#
#******************************************************************************

def getCopelandErdosConstant( ):
    result = ''

    count = 1

    while len( result ) < mp.dps:
        # TODO: use a generator
        result += str( getNthPrime( count ) )
        count += 1

    return convertToBase10( '0', result, 10 )


#******************************************************************************
#
#  getRobbinsConstant
#
#  https://en.wikipedia.org/wiki/Robbins_constant
#
#******************************************************************************

def getRobbinsConstant( ):
    robbins = fsub( fsub( fadd( 4, fmul( 17, sqrt( 2 ) ) ), fmul( 6, sqrt( 3 ) ) ), fmul( 7, pi ) )
    robbins = fdiv( robbins, 105 )
    robbins = fadd( robbins, fdiv( log( fadd( 1, sqrt( 2 ) ) ), 5 ) )
    robbins = fadd( robbins, fdiv( fmul( 2, log( fadd( 2, sqrt( 3 ) ) ) ), 5 ) )

    return robbins


#******************************************************************************
#
#  getMaxDouble
#
#******************************************************************************

@lru_cache( 1 )
def getMaxDouble( ):
    return interpretAsDouble( mpmathify( 0x7fef_ffff_ffff_ffff ) )


#******************************************************************************
#
#  getMaxFloat
#
#******************************************************************************

@lru_cache( 1 )
def getMaxFloat( ):
    return interpretAsFloat( mpmathify( 0x7f7f_ffff ) )


#******************************************************************************
#
#  getMinDouble
#
#******************************************************************************

@lru_cache( 1 )
def getMinDouble( ):
    return interpretAsDouble( mpmathify( 0x0010_0000_0000_0000 ) )


#******************************************************************************
#
#  getMinFloat
#
#******************************************************************************

@lru_cache( 1 )
def getMinFloat( ):
    return interpretAsFloat( mpmathify( 0x0080_0000 ) )


#******************************************************************************
#
#  getFineStructureConstant
#
#  I'm cheating here, but the units really do cancel out.
#
#******************************************************************************

@lru_cache( 1 )
def getFineStructureConstant( ):
    return getPower( getConstant( 'electron_charge' ), 2 ).divide(
                getProduct( [ g.h_bar, g.c, 4, pi, getConstant( 'electric_constant' ) ] ) )


#******************************************************************************
#
#  getPlanckLength
#
#  All the Planck unit stuff used this source of information:
#
#  https://en.wikipedia.org/wiki/Planck_units
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckLength( ):
    return getRoot( g.h_bar.multiply( g.G ).divide( getPower( g.c, 3 ) ), 2 )


#******************************************************************************
#
#  getPlanckMass
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckMass( ):
    return getRoot( g.h_bar.multiply( g.c ).divide( g.G ), 2 )


#******************************************************************************
#
#  getPlanckTime
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckTime( ):
    return getRoot( g.h_bar.multiply( g.G ).divide( getPower( g.c, 5 ) ), 2 )


#******************************************************************************
#
#  getPlanckCharge
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckCharge( ):
    return getConstant( 'electron_charge' ).divide( getRoot( getFineStructureConstant( ), 2 ) )


#******************************************************************************
#
#  getPlanckTemperature
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckTemperature( ):
    return getRoot( g.h_bar.multiply( getPower( g.c, 5 ) ).
                    divide( g.G.multiply( getPower( g.k, 2 ) ) ), 2 )


#******************************************************************************
#
#  getPlanckArea
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckArea( ):
    return g.h_bar.multiply( g.G ).divide( getPower( g.c, 3 ) )


#******************************************************************************
#
#  getPlanckVolume
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckVolume( ):
    return getRoot( getPower( g.h_bar.multiply( g.G ), 3 ).divide( getPower( g.c, 9 ) ), 2 )


#******************************************************************************
#
#  getPlanckMomentum
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckMomentum( ):
    return getRoot( g.h_bar.multiply( getPower( g.c, 3 ) ).divide( g.G ), 2 )


#******************************************************************************
#
#  getPlanckEnergy
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckEnergy( ):
    return getRoot( g.h_bar.multiply( getPower( g.c, 5 ) ).divide( g.G ), 2 ).convert( 'joule' )


#******************************************************************************
#
#  getPlanckForce
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckForce( ):
    return getPower( g.c, 4 ).divide( g.G ).convert( 'newton' )


#******************************************************************************
#
#  getPlanckPower
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckPower( ):
    return getPower( g.c, 5 ).divide( g.G ).convert( 'watt' )


#******************************************************************************
#
#  getPlanckDensity
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckDensity( ):
    return getPower( g.c, 5 ).divide( g.h_bar. multiply( getPower( g.G, 2 ) ) ).convert( 'kilogram/meter^3' )


#******************************************************************************
#
#  getPlanckEnergyDensity
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckEnergyDensity( ):
    return getPower( g.c, 7 ).divide( g.h_bar.multiply( getPower( g.G, 2 ) ) ).convert( 'pascal' )


#******************************************************************************
#
#  getPlanckEnergyIntensity
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckIntensity( ):
    return getPower( g.c, 8 ).divide( g.h_bar. multiply( getPower( g.G, 2 ) ) ).convert( 'watt/meter^2' )


#******************************************************************************
#
#  getPlanckPressure
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckPressure( ):
    return getPower( g.c, 7 ).divide( g.h_bar.multiply( getPower( g.G, 2 ) ) ).convert( 'pascal' )


#******************************************************************************
#
#  getPlanckCurrent
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckCurrent( ):
    return getRoot( getProduct( [ 4, pi, g.e0, getPower( g.c, 6 ) ] ).divide( g.G ), 2 )


#******************************************************************************
#
#  getPlanckVoltage
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckVoltage( ):
    return getRoot( getProduct( [ 4, pi, g.e0, getPower( g.c, 6 ) ] ).divide( g.G ), 2 )


#******************************************************************************
#
#  getPlanckImpedance
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckImpedance( ):
    return getVacuumImpedance( ).divide( fmul( 4, pi ) )


#******************************************************************************
#
#  getPlanckMagneticInductance
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckMagneticInductance( ):
    return getRoot( getPower( g.c, 5 ).divide( getProduct( [ g.h_bar,
                                                             getPower( g.G, 2 ), 4, pi, g.e0 ] ) ),
                    2 ).convert( 'tesla' )


#******************************************************************************
#
#  getPlanckElectricalInductance
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckElectricalInductance( ):
    return getRoot( g.G.multiply( g.h_bar ).divide( getPower( g.c, 7 ).
                                                    multiply( getPower( getProduct( [ 4, pi, g.e0 ] ), 2 ) ) ),
                    2 ).convert( 'henry' )


#******************************************************************************
#
#  getPlanckVolumetricFlowRate
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckVolumetricFlowRate( ):
    return g.h_bar.multiply( g.G ).divide( getPower( g.c, 2 ) )


#******************************************************************************
#
#  getPlanckViscosity
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckViscosity( ):
    return getRoot( getPower( g.c, 9 ).divide( getPower( g.G, 3 ).multiply( g.h_bar ) ), 2 ).convert( 'pascal*second' )


#******************************************************************************
#
#  getPlanckAcceleration
#
#******************************************************************************

@lru_cache( 1 )
def getPlanckAcceleration( ):
    return getRoot( getPower( g.c, 7 ).divide( g.h_bar.multiply( g.G ) ), 2 )


#******************************************************************************
#
#  getStefanBoltzmannConstant
#
#******************************************************************************

@lru_cache( 1 )
def getStefanBoltzmannConstant( ):
    nSubA = RPNMeasurement( getConstant( 'avogadro_number' ), 'mole^-1' )

    return getProduct( [ 2, getPower( pi, 5 ), getPower( getConstant( 'molar_gas_constant' ), 4 ) ] ).divide(
        getProduct( [ 15, getPower( g.h, 3 ), getPower( g.c, 2 ),
                      getPower( nSubA, 4 ) ] ) )


#******************************************************************************
#
#  getThueMorseConstant
#
#  https://en.wikipedia.org/wiki/Prouhet%E2%80%93Thue%E2%80%93Morse_constant
#
#******************************************************************************

def getThueMorseConstant( ):
    result = 0
    factor = mpmathify( '0.5' )

    for i in arange( 0, mp.prec + 1 ):
        result = fadd( result, fmul( getNthThueMorseNumber( i ), factor ) )
        factor = fdiv( factor, 2 )

    return result


#******************************************************************************
#
#  getRadiationConstant
#
#  https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant
#
#******************************************************************************

@lru_cache( 1 )
def getRadiationConstant( ):
    return getStefanBoltzmannConstant( ).multiply( 4 ).divide( g.c )


#******************************************************************************
#
#  getFaradayConstant
#
#  https://en.wikipedia.org/wiki/Faraday_constant
#
#******************************************************************************

@lru_cache( 1 )
def getFaradayConstant( ):
    return RPNMeasurement( getConstant( 'avogadro_number' ), '1/mole' ). \
                        multiply( getConstant( 'electron_charge' ) )


#******************************************************************************
#
#  getVacuumImpedance
#
#  https://en.wikipedia.org/wiki/Impedance_of_free_space
#
#******************************************************************************

@lru_cache( 1 )
def getVacuumImpedance( ):
    return getConstant( 'magnetic_constant' ).multiply( g.c ).convert( 'ohm' )


#******************************************************************************
#
#  getvonKlitzingConstant
#
#  https://www.easycalculation.com/constant/von-klitzing-constant.html
#
#******************************************************************************

@lru_cache( 1 )
def getvonKlitzingConstant( ):
    return g.h.divide( getPower( g.e, 2 ) ).convert( 'ohm' )

