# //******************************************************************************
# //
# //  testRPN
# //
# //  main test script for RPN
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn import rpn

from testConvert import *


# //******************************************************************************
# //
# //  testRPN
# //
# //******************************************************************************

def testRPN( command ):
    print( command )
    rpn( command.split( ' ' )[ 1 : ] )
    print( )


# //******************************************************************************
# //
# //  runTests
# //
# //  At this point, there is no validation of the answers.  Mostly this tests
# //  that every operator works without throwing unhandled exceptions.
# //
# //******************************************************************************

def runTests( ):
    # command-line options
    testRPN( 'rpn -a20 7 sqrt' )

    testRPN( 'rpn 100101011010011 -b 2' )
    testRPN( 'rpn 120012022211222012 -b 3' )
    testRPN( 'rpn rick -b 36' )

    testRPN( 'rpn 6 8 ** -c' )

    testRPN( 'rpn -a3 7 sqrt -d' )
    testRPN( 'rpn -a12 8 sqrt -d5' )
    testRPN( 'rpn -a50 19 sqrt -d10' )

    testRPN( 'rpn -p50 1 30 range fib -g 3' )
    testRPN( 'rpn -p50 1 30 range fib -g 4' )

    testRPN( 'rpn -h' )

    testRPN( 'rpn 2 sqrt pi * -i' )

    testRPN( 'rpn 1 10 range 3 ** -o' )

    testRPN( 'rpn pi -p 1000' )

    testRPN( 'rpn 10 100 10 range2 -r phi' )

    testRPN( 'rpn 1 100 range -r2' )
    testRPN( 'rpn 1 100 range -r3' )
    testRPN( 'rpn 1 100 range -r4' )
    testRPN( 'rpn 1 100 range -r5' )
    testRPN( 'rpn 1 100 range -r6' )
    testRPN( 'rpn 1 100 range -r7' )
    testRPN( 'rpn 1 100 range -r8' )
    testRPN( 'rpn 1 100 range -r9' )
    testRPN( 'rpn 1 100 range -r10' )
    testRPN( 'rpn 1 100 range -r11' )
    testRPN( 'rpn 1 100 range -r12' )
    testRPN( 'rpn 1 100 range -r13' )
    testRPN( 'rpn 1 100 range -r14' )
    testRPN( 'rpn 1 100 range -r15' )
    testRPN( 'rpn 1 100 range -r16' )
    testRPN( 'rpn 1 100 range -r17' )
    testRPN( 'rpn 1 100 range -r18' )
    testRPN( 'rpn 1 100 range -r19' )
    testRPN( 'rpn 1 100 range -r20' )
    testRPN( 'rpn 1 100 range -r21' )
    testRPN( 'rpn 1 100 range -r22' )
    testRPN( 'rpn 1 100 range -r23' )
    testRPN( 'rpn 1 100 range -r24' )
    testRPN( 'rpn 1 100 range -r25' )
    testRPN( 'rpn 1 100 range -r26' )
    testRPN( 'rpn 1 100 range -r27' )
    testRPN( 'rpn 1 100 range -r28' )
    testRPN( 'rpn 1 100 range -r29' )
    testRPN( 'rpn 1 100 range -r30' )
    testRPN( 'rpn 1 100 range -r31' )
    testRPN( 'rpn 1 100 range -r32' )
    testRPN( 'rpn 1 100 range -r33' )
    testRPN( 'rpn 1 100 range -r34' )
    testRPN( 'rpn 1 100 range -r35' )
    testRPN( 'rpn 1 100 range -r36' )
    testRPN( 'rpn 1 100 range -r37' )
    testRPN( 'rpn 1 100 range -r38' )
    testRPN( 'rpn 1 100 range -r39' )
    testRPN( 'rpn 1 100 range -r40' )
    testRPN( 'rpn 1 100 range -r41' )
    testRPN( 'rpn 1 100 range -r42' )
    testRPN( 'rpn 1 100 range -r43' )
    testRPN( 'rpn 1 100 range -r44' )
    testRPN( 'rpn 1 100 range -r45' )
    testRPN( 'rpn 1 100 range -r46' )
    testRPN( 'rpn 1 100 range -r47' )
    testRPN( 'rpn 1 100 range -r48' )
    testRPN( 'rpn 1 100 range -r49' )
    testRPN( 'rpn 1 100 range -r50' )
    testRPN( 'rpn 1 100 range -r51' )
    testRPN( 'rpn 1 100 range -r52' )
    testRPN( 'rpn 1 100 range -r53' )
    testRPN( 'rpn 1 100 range -r54' )
    testRPN( 'rpn 1 100 range -r55' )
    testRPN( 'rpn 1 100 range -r56' )
    testRPN( 'rpn 1 100 range -r57' )
    testRPN( 'rpn 1 100 range -r58' )
    testRPN( 'rpn 1 100 range -r59' )
    testRPN( 'rpn 1 100 range -r60' )
    testRPN( 'rpn 1 100 range -r61' )
    testRPN( 'rpn 1 100 range -r62' )
    testRPN( 'rpn 1 100 range -rphi' )

    testRPN( 'rpn -a1000 -d5 7 sqrt -r62' )
    testRPN( 'rpn -a1000 -d5 pi -r8' )
    testRPN( 'rpn 2 1 32 range ** -r16' )

    testRPN( 'rpn -t 12 14 ** 1 + factor' )

    testRPN( 'rpn 3 1 20 range ** -x' )

    testRPN( 'rpn 65537 4 ** -r 16 -g8 -z' )

    # operators
    testRPN( 'rpn -394 abs' )

    testRPN( 'rpn 0.8 acos' )

    testRPN( 'rpn 0.6 acosh' )

    testRPN( 'rpn 0.4 acot' )

    testRPN( 'rpn 0.3 acoth' )

    testRPN( 'rpn 0.2 acsc' )

    testRPN( 'rpn 0.67 acsch' )

    testRPN( 'rpn 4 3 add' )
    testRPN( 'rpn 4 cups 13 teaspoons +' )
    testRPN( 'rpn 55 mph 10 miles hour / +' )
    testRPN( 'rpn 55 mph 10 meters second / +' )
    testRPN( 'rpn 55 mph 10 furlongs fortnight / +' )
    testRPN( 'rpn today 3 days add' )
    testRPN( 'rpn today 3 weeks add' )
    testRPN( 'rpn now 150 miles 10 furlongs fortnight / / add' )

    testRPN( 'rpn 13 altfac' )

    testRPN( 'rpn 0x7777 0xdcba and' )

    testRPN( 'rpn apery' )

    testRPN( 'rpn 12 aperynum' )

    testRPN( 'rpn 0.4 asec' )

    testRPN( 'rpn 0.1 asech' )

    testRPN( 'rpn 0.8 asin' )

    testRPN( 'rpn 0.3 asinh' )

    testRPN( 'rpn 0.2 atan' )

    testRPN( 'rpn 0.45 atanh' )

    testRPN( 'rpn avogadro' )

    testRPN( 'rpn 1 10 range balanced' )
    testRPN( 'rpn 53 balanced' )
    testRPN( 'rpn 153 balanced' )
    testRPN( 'rpn 2153 balanced' )

    testRPN( 'rpn 1 10 range balanced_' )
    testRPN( 'rpn 53 balanced_' )
    testRPN( 'rpn 153 balanced_' )
    testRPN( 'rpn 2153 balanced_' )

    testRPN( 'rpn -p43 45 bell' )

    testRPN( 'rpn 4 5 bellpoly' )

    testRPN( 'rpn 16 bernoulli' )

    testRPN( 'rpn 12 9 binomial' )
    testRPN( 'rpn -c 120 108 binomial' )

    testRPN( 'rpn 773 carol' )

    testRPN( 'rpn 85 catalan' )

    testRPN( 'rpn 1965-03 calendar' )
    testRPN( 'rpn 2014-10 calendar' )

    testRPN( 'rpn catalans' )

    testRPN( 'rpn 17 cdecagonal' )

    testRPN( 'rpn 1000 cdecagonal?' )

    testRPN( 'rpn 9.99999 ceiling' )

    testRPN( 'rpn 100 centeredcube' )

    testRPN( 'rpn -p100 champernowne' )

    testRPN( 'rpn 0x101 char' )

    testRPN( 'rpn 102 cheptagonal' )

    testRPN( 'rpn 100000 cheptagonal?' )

    testRPN( 'rpn 103 chexagonal' )

    testRPN( 'rpn 104 cnonagonal' )

    testRPN( 'rpn 5,000,000 cnonagonal?' )

    testRPN( 'rpn 10 coctagonal' )

    testRPN( 'rpn 361 coctagonal?' )

    testRPN( 'rpn -a 1000 copeland' )

    testRPN( 'rpn 45 degrees cos' )
    testRPN( 'rpn pi radians cos' )

    testRPN( 'rpn pi 3 / cosh' )

    testRPN( 'rpn pi 7 / cot' )

    testRPN( 'rpn pi 9 / coth' )

    testRPN( 'rpn 0xffff countbits' )

    testRPN( 'rpn 1024 countdiv' )

    testRPN( 'rpn 1 10 range cousinprime' )
    testRPN( 'rpn 77 cousinprime' )
    testRPN( 'rpn 5176 cousinprime' )

    testRPN( 'rpn 108 cpentagonal' )

    testRPN( 'rpn 9999 cpentagonal?' )

    testRPN( 'rpn 108 5 cpolygonal' )

    testRPN( 'rpn 9999 5 cpolygonal?' )

    testRPN( 'rpn pi 12 / csc' )

    testRPN( 'rpn pi 13 / csch' )

    testRPN( 'rpn 5 csquare' )

    testRPN( 'rpn 49 csquare?' )

    testRPN( 'rpn 100 ctriangular' )

    testRPN( 'rpn 10000 ctriangular?' )

    testRPN( 'rpn 3 cube' )

    testRPN( 'rpn 151 decagonal' )

    testRPN( 'rpn 123454321 decagonal?' )

    testRPN( 'rpn 100 delannoy' )

    testRPN( 'rpn 8 million seconds dhms' )

    testRPN( 'rpn 12 13 divide' )
    testRPN( 'rpn 10 days 7 / dhms' )
    testRPN( 'rpn marathon 100 miles hour / / minutes convert' )
    testRPN( 'rpn 2 zeta sqrt 24 sqrt / 12 *' )
    testRPN( 'rpn now 2014-01-01 - minutes /' )

    testRPN( 'rpn 2 3 ** 3 4 ** * divisors' )
    testRPN( 'rpn 12 ! divisors' )

    testRPN( 'rpn 1 radian dms' )

    testRPN( 'rpn 44 dodecahedral' )

    testRPN( 'rpn -x 10 20 ** double' )

    testRPN( 'rpn 1 5 range doublebal' )
    testRPN( 'rpn 54 doublebal' )
    testRPN( 'rpn 82154 doublebal' )

    testRPN( 'rpn 1 5 range doublebal_' )
    testRPN( 'rpn 54 doublebal_' )
    testRPN( 'rpn 100000 doublebal_' )

    testRPN( 'rpn 9 doublefac' )

    testRPN( 'rpn e' )

    testRPN( 'rpn 45 67 egypt' )

    testRPN( 'rpn 1 10 range 5 element' )
    testRPN( 'rpn -a25 1 100 range fib 55 element' )

    testRPN( 'rpn 150 amps estimate' )
    testRPN( 'rpn 150 barns estimate' )
    testRPN( 'rpn 150 bytes second / estimate' )
    testRPN( 'rpn 150 candelas estimate' )
    testRPN( 'rpn 150 cd meter meter * / estimate' )
    testRPN( 'rpn 150 coulombs estimate' )
    testRPN( 'rpn 150 cubic_feet estimate' )
    testRPN( 'rpn 150 cubic_inches estimate' )
    testRPN( 'rpn 150 cubic_miles estimate' )
    testRPN( 'rpn 150 cubic_mm estimate' )
    testRPN( 'rpn 150 cubic_nm estimate' )
    testRPN( 'rpn 150 cubic_parsecs estimate' )
    testRPN( 'rpn 150 days estimate' )
    testRPN( 'rpn 150 degC estimate' )
    testRPN( 'rpn 150 degrees estimate' )
    testRPN( 'rpn 150 farads estimate' )
    testRPN( 'rpn 150 feet estimate' )
    testRPN( 'rpn 150 G estimate' )
    testRPN( 'rpn 150 gallons estimate' )
    testRPN( 'rpn 150 grams estimate' )
    testRPN( 'rpn 150 GW estimate' )
    testRPN( 'rpn 150 Hz estimate' )
    testRPN( 'rpn 150 joules estimate' )
    testRPN( 'rpn 150 K estimate' )
    testRPN( 'rpn 150 kg liter / estimate' )
    testRPN( 'rpn 150 light-years estimate' )
    testRPN( 'rpn 150 liters estimate' )
    testRPN( 'rpn 150 lumens estimate' )
    testRPN( 'rpn 150 lux estimate' )
    testRPN( 'rpn 150 mach estimate' )
    testRPN( 'rpn 150 MB estimate' )
    testRPN( 'rpn 150 megapascals estimate' )
    testRPN( 'rpn 150 meter second second * / estimate' )
    testRPN( 'rpn 150 mhos estimate' )
    testRPN( 'rpn 150 microfarads estimate' )
    testRPN( 'rpn 150 miles estimate' )
    testRPN( 'rpn 150 minutes estimate' )
    testRPN( 'rpn 150 months estimate' )
    testRPN( 'rpn 150 mph estimate' )
    testRPN( 'rpn 150 mps estimate' )
    testRPN( 'rpn 150 newtons estimate' )
    testRPN( 'rpn 150 ohms estimate' )
    testRPN( 'rpn 150 pascal-seconds estimate' )
    testRPN( 'rpn 150 pascals estimate' )
    testRPN( 'rpn 150 Pg estimate' )
    testRPN( 'rpn 150 picofarads estimate' )
    testRPN( 'rpn 150 pounds estimate' )
    testRPN( 'rpn 150 radians estimate' )
    testRPN( 'rpn 150 seconds estimate' )
    testRPN( 'rpn 150 sieverts estimate' )
    testRPN( 'rpn 150 square_degrees estimate' )
    testRPN( 'rpn 150 square_feet estimate' )
    testRPN( 'rpn 150 square_inches estimate' )
    testRPN( 'rpn 150 square_light-years estimate' )
    testRPN( 'rpn 150 square_miles estimate' )
    testRPN( 'rpn 150 square_mm estimate' )
    testRPN( 'rpn 150 square_nm estimate' )
    testRPN( 'rpn 150 stilbs estimate' )
    testRPN( 'rpn 150 teaspoons estimate' )
    testRPN( 'rpn 150 tesla estimate' )
    testRPN( 'rpn 150 tons estimate' )
    testRPN( 'rpn 150 tTNT estimate' )
    testRPN( 'rpn 150 volts estimate' )
    testRPN( 'rpn 150 watts estimate' )
    testRPN( 'rpn 150 weeks estimate' )
    testRPN( 'rpn 150 years estimate' )
    testRPN( 'rpn c 150 / estimate' )

    testRPN( 'rpn euler' )

    testRPN( 'rpn 10 x 5 * eval' )
    testRPN( 'rpn 57 x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )

    testRPN( 'rpn 13 exp' )

    testRPN( 'rpn 12 exp10' )

    testRPN( 'rpn 100 expphi' )

    testRPN( 'rpn 1.1 1.1 10 exprange' )

    testRPN( 'rpn 883847311 factor' )

    testRPN( 'rpn 23 factorial' )

    testRPN( 'rpn 1 50 range fibonacci' )
    testRPN( 'rpn -c -a 8300 39399 fibonacci' )

    testRPN( 'rpn -x 1029.3 float' )

    testRPN( 'rpn 3.4 floor' )

    testRPN( 'rpn 12 23 fraction' )

    testRPN( 'rpn 1234567890 fromunixtime' )

    testRPN( 'rpn 3 gamma' )

    testRPN( 'rpn 2 8 8 georange' )

    testRPN( 'rpn glaisher' )

    testRPN( 'rpn 34 harmonic' )

    testRPN( 'rpn 203 heptagonal' )

    testRPN( 'rpn 99999 heptagonal?' )

    testRPN( 'rpn 224623 heptanacci' )

    testRPN( 'rpn 2039 hepthex' )

    testRPN( 'rpn 8684 heptpent' )

    testRPN( 'rpn 222 heptsquare' )

    testRPN( 'rpn 399 hepttri' )

    testRPN( 'rpn 340 hexagonal' )

    testRPN( 'rpn 230860 hexagonal?' )

    testRPN( 'rpn 949 hexanacci' )

    testRPN( 'rpn 107 hexpent' )

    testRPN( 'rpn 54658 seconds hms' )

    testRPN( 'rpn 4 3 hyper4_2' )

    testRPN( 'rpn 17 hyperfac' )

    testRPN( 'rpn 3 4 hypot' )

    testRPN( 'rpn 3 i' )

    testRPN( 'rpn 100 icosahedral' )

    testRPN( 'rpn 456 8 integer' )

    testRPN( 'rpn 1000 10000 isdivisible' )

    testRPN( 'rpn 102 isolated' )
    testRPN( 'rpn 1902 isolated' )

    testRPN( 'rpn 1000 1030 range isprime' )
    testRPN( 'rpn 2049 isprime' )
    testRPN( 'rpn 92348759911 isprime' )

    testRPN( 'rpn 1024 issquare' )

    testRPN( 'rpn itoi' )

    testRPN( 'rpn 10 jacobsthal' )

    testRPN( 'rpn khinchin' )

    testRPN( 'rpn 8 kynea' )

    testRPN( 'rpn 5 6 lah' )

    testRPN( 'rpn 5 lambertw' )

    testRPN( 'rpn 7 8 leyland' )

    testRPN( 'rpn 10 lgamma' )

    testRPN( 'rpn 12 li' )

    testRPN( 'rpn inf x fib x 1 - fib / limit' )
    testRPN( 'rpn inf x 1/x 1 + x ** limit' )

    testRPN( 'rpn 1000 ln' )
    testRPN( 'rpn 1000 log10' )

    testRPN( 'rpn 1000 log2' )

    testRPN( 'rpn 6561 3 logxy' )

    testRPN( 'rpn 3456789012 long' )

    testRPN( 'rpn 1234567890123456789012 longlong' )

    testRPN( 'rpn 99 lucas' )
    testRPN( 'rpn e 20 makecf' )

    testRPN( 'rpn maxchar' )
    testRPN( 'rpn maxlong' )

    testRPN( 'rpn maxlonglong' )

    testRPN( 'rpn maxquadlong' )

    testRPN( 'rpn maxshort' )

    testRPN( 'rpn maxuchar' )

    testRPN( 'rpn maxulong' )

    testRPN( 'rpn maxulonglong' )

    testRPN( 'rpn maxuquadlong' )

    testRPN( 'rpn maxushort' )

    testRPN( 'rpn mertens' )

    testRPN( 'rpn minchar' )

    testRPN( 'rpn minlong' )

    testRPN( 'rpn minlonglong' )

    testRPN( 'rpn minquadlong' )

    testRPN( 'rpn minshort' )

    testRPN( 'rpn minuchar' )

    testRPN( 'rpn minulong' )

    testRPN( 'rpn minulonglong' )

    testRPN( 'rpn minuquadlong' )

    testRPN( 'rpn minushort' )

    testRPN( 'rpn 11001 100 modulo' )

    testRPN( 'rpn 56 motzkin' )

    testRPN( 'rpn 5 7 multiply' )
    testRPN( 'rpn 15 mph 10 hours *' )
    testRPN( 'rpn c m/s convert 1 nanosecond * inches convert' )
    testRPN( 'rpn barn gigaparsec * cubic_inch convert' )

    testRPN( 'rpn -c -p100 45 primorial name' )

    testRPN( 'rpn 6 8 narayana' )

    testRPN( 'rpn 4 negative' )

    testRPN( 'rpn 554 nonagonal' )

    testRPN( 'rpn 9 6 ** nonagonal?' )

    testRPN( 'rpn 12 nonahept' )

    testRPN( 'rpn 13 nonahex' )

    testRPN( 'rpn 14 nonaoct' )

    testRPN( 'rpn 15 nonapent' )

    testRPN( 'rpn 16 nonasquare' )

    testRPN( 'rpn 17 nonatri' )

    testRPN( 'rpn -x 0xefefefefefefef not' )

    testRPN( 'rpn now' )

    testRPN( 'rpn 34 inches 3 nspherearea' )
    testRPN( 'rpn 34 square_inches 3 nspherearea' )
    testRPN( 'rpn 34 cubic_inches 3 nspherearea' )

    testRPN( 'rpn 3 meters 4 nsphereradius' )
    testRPN( 'rpn 3 square_meters 4 nsphereradius' )
    testRPN( 'rpn 3 cubic_meters 4 nsphereradius' )

    testRPN( 'rpn 3 square_feet 6 nspherevolume' )

    testRPN( 'rpn 1 10 range nthprime?' )
    testRPN( 'rpn 67 nthprime?' )
    testRPN( 'rpn 16467 nthprime?' )
    testRPN( 'rpn -c 13,000,000,000 nthprime?' )

    testRPN( 'rpn 1 100000 10000 range2 nthquad?' )
    testRPN( 'rpn 453456 nthquad?' )
    testRPN( 'rpn 74,000,000,000 nthquad?' )

    testRPN( 'rpn 102 octagonal' )

    testRPN( 'rpn 8 4 ** 1 + octagonal?' )

    testRPN( 'rpn 23 octahedral' )

    testRPN( 'rpn -p40 8 octhept' )

    testRPN( 'rpn -p30 7 octhex' )

    testRPN( 'rpn 6 octpent' )

    testRPN( 'rpn -p25 11 octsquare' )

    testRPN( 'rpn 10 octtri' )

    testRPN( 'rpn 1000 oeis' )
    testRPN( 'rpn 200000 randint oeis' )

    testRPN( 'rpn 1000 oeiscomment' )
    testRPN( 'rpn 200000 randint oeiscomment' )

    testRPN( 'rpn 1000 oeisex' )
    testRPN( 'rpn 200000 randint oeisex' )

    testRPN( 'rpn 1000 oeisname' )
    testRPN( 'rpn 200000 randint oeisname' )

    testRPN( 'rpn omega' )

    testRPN( 'rpn -x 0x5543 0x7789 or' )

    testRPN( 'rpn 76 padovan' )

    testRPN( 'rpn 0xff889d8f parity' )

    testRPN( 'rpn 12 pascal' )

    testRPN( 'rpn 13 pell' )

    testRPN( 'rpn 16 pentagonal' )

    testRPN( 'rpn 5 5 ** 5 + pentagonal?' )

    testRPN( 'rpn 16 pentanacci' )

    testRPN( 'rpn 12 pentatope' )

    testRPN( 'rpn 8 3 perm' )

    testRPN( 'rpn phi' )

    testRPN( 'rpn pi' )

    testRPN( 'rpn plastic' )

    testRPN( 'rpn 13 polyarea' )

    testRPN( 'rpn 4 5 polygamma' )

    testRPN( 'rpn 9 12 polygonal' )

    testRPN( 'rpn 12 12 ** 12 polygonal?' )

    testRPN( 'rpn 9 3 polylog' )

    testRPN( 'rpn 1 5 range 1 5 range polyprime' )
    testRPN( 'rpn 4 3 polyprime' )
    testRPN( 'rpn 5 8 polyprime' )

    testRPN( 'rpn 1 10 range 7 polytope' )
    testRPN( 'rpn 10 2 8 range polytope' )
    testRPN( 'rpn 1 10 range 2 8 range polytope' )
    testRPN( 'rpn -c 18 47 polytope' )

    testRPN( 'rpn 4 5 power' )
    testRPN( 'rpn 4 1 i power' )
    testRPN( 'rpn 1 10 range 2 10 range power' )

    testRPN( 'rpn 1 101 range prime' )
    testRPN( 'rpn 8783 prime' )
    testRPN( 'rpn 142857 prime' )
    testRPN( 'rpn 367981443 prime' )

    testRPN( 'rpn 1 100 range prime?' )
    testRPN( 'rpn 35 prime?' )
    testRPN( 'rpn 8783 prime?' )
    testRPN( 'rpn 142857 prime?' )
    testRPN( 'rpn -c 6 13 ** 1 + prime?' )

    testRPN( 'rpn 87 primepi' )

    testRPN( 'rpn 1 5 range 5 primes' )
    testRPN( 'rpn 1 1 5 range primes' )
    testRPN( 'rpn 2 1 5 range primes' )
    testRPN( 'rpn 3 1 5 range primes' )
    testRPN( 'rpn 4 1 5 range primes' )
    testRPN( 'rpn 150 10 primes' )
    testRPN( 'rpn 98765 20 primes' )
    testRPN( 'rpn 176176176 25 primes' )

    testRPN( 'rpn 304 pyramid' )

    testRPN( 'rpn 17 quadprime' )
    testRPN( 'rpn 99831 quadprime' )

    testRPN( 'rpn 8 quadprime?' )
    testRPN( 'rpn 8871 quadprime?' )

    testRPN( 'rpn 17 quadprime_' )
    testRPN( 'rpn 55731 quadprime_' )

    testRPN( 'rpn 18 quintprime' )
    testRPN( 'rpn 9387 quintprime' )

    testRPN( 'rpn 62 quintprime_' )
    testRPN( 'rpn 74238 quintprime_' )

    testRPN( 'rpn random' )

    testRPN( 'rpn 50 random_' )

    testRPN( 'rpn 100 randint' )
    testRPN( 'rpn 10 12 ^ randint' )

    testRPN( 'rpn 23 265 randint_' )

    testRPN( 'rpn 1 23 range' )

    testRPN( 'rpn 1 23 2 range2' )

    testRPN( 'rpn 6 7 / reciprocal' )

    testRPN( 'rpn 23 5 repunit' )

    testRPN( 'rpn 89 rhombdodec' )

    testRPN( 'rpn 23 riesel' )

    testRPN( 'rpn 8 3 root' )

    testRPN( 'rpn 2 root2' )

    testRPN( 'rpn pi root3' )

    testRPN( 'rpn 4.5 round' )

    testRPN( 'rpn 45 safeprime' )
    testRPN( 'rpn 5199846 safeprime' )

    testRPN( 'rpn -p50 67 schroeder' )

    testRPN( 'rpn pi 7 / sec' )

    testRPN( 'rpn pi 7 / sech' )

    testRPN( 'rpn 29 sextprime' )
    testRPN( 'rpn 1176 sextprime' )

    testRPN( 'rpn 29 sextprime_' )
    testRPN( 'rpn 556 sextprime' )

    testRPN( 'rpn 1 sextprime_' )
    testRPN( 'rpn 587 sextprime_' )
    testRPN( 'rpn 835 sextprime_' )

    testRPN( 'rpn 29 sexyprime' )
    testRPN( 'rpn 23235 sexyprime' )

    testRPN( 'rpn 1 sexyprime' )
    testRPN( 'rpn 2 sexyprime' )
    testRPN( 'rpn 1487 sexyprime' )
    testRPN( 'rpn -c 89,999,999 sexyprime' )

    testRPN( 'rpn 1 10 range sexyprime_' )
    testRPN( 'rpn 29 sexyprime_' )
    testRPN( 'rpn 21985 sexyprime_' )
    testRPN( 'rpn -c 100,000,000 sexyprime_' )

    testRPN( 'rpn 1 10 range sexyquad' )
    testRPN( 'rpn 29 sexyquad' )
    testRPN( 'rpn -c 289747 sexyquad' )

    testRPN( 'rpn 1 10 range sexyquad_' )
    testRPN( 'rpn 29 sexyquad_' )
    testRPN( 'rpn 2459 sexyquad_' )

    testRPN( 'rpn 1 10 range sexytriplet' )
    testRPN( 'rpn 29 sexytriplet' )
    testRPN( 'rpn -c 593847 sexytriplet' )
    testRPN( 'rpn -c 8574239 sexytriplet' )

    testRPN( 'rpn 1 10 range sexytriplet_' )
    testRPN( 'rpn 52 sexytriplet_' )
    testRPN( 'rpn 5298 sexytriplet_' )
    testRPN( 'rpn -c 10984635 sexytriplet_' )

    testRPN( 'rpn -x 0x10 3 shiftleft' )

    testRPN( 'rpn -x 0x1000 4 shiftright' )

    testRPN( 'rpn 32800 short' )

    testRPN( 'rpn pi 2 / sin' )

    testRPN( 'rpn pi 2 / sinh' )

    testRPN( 'rpn 8 9 10 solve2' )

    testRPN( 'rpn 10 -10 10 -10 solve3' )

    testRPN( 'rpn 2 -3 2 -3 2 solve4' )

    testRPN( 'rpn 1 10 range sophieprime' )
    testRPN( 'rpn 87 sophieprime' )
    testRPN( 'rpn 6,500,000 sophieprime' )

    testRPN( 'rpn 8 inches spherearea' )
    testRPN( 'rpn 8 sq_inches spherearea' )
    #testRPN( 'rpn 8 cu_inches spherearea' )    # not implemented yet

    testRPN( 'rpn 4 inches sphereradius' )
    testRPN( 'rpn 4 square_inches sphereradius' )
    testRPN( 'rpn 4 cubic_inches sphereradius' )

    testRPN( 'rpn 5 inches spherevolume' )
    #testRPN( 'rpn 5 sq_inches spherevolume' )  # not implemented yet
    testRPN( 'rpn 5 cubic_in spherevolume' )

    testRPN( 'rpn 45 square' )

    testRPN( 'rpn 34 squaretri' )

    testRPN( 'rpn 3945 steloct' )

    testRPN( 'rpn 19 subfac' )

    testRPN( 'rpn 3948 474 subtract' )
    testRPN( 'rpn 4 cups 27 teaspoons -' )
    testRPN( 'rpn 57 hectares 23 acres -' )
    testRPN( 'rpn 10 Mb second / 700 MB hour / -' )
    testRPN( 'rpn today 3 days -' )
    testRPN( 'rpn today 3 weeks -' )
    testRPN( 'rpn today 3 months -' )
    testRPN( 'rpn now earth_radius 2 pi * * miles convert 4 mph / -' )

    testRPN( 'rpn 12 superfac' )

    testRPN( 'rpn 89 superprime' )

    testRPN( 'rpn 45 sylvester' )

    testRPN( 'rpn pi 3 / tan' )

    testRPN( 'rpn pi 4 / tanh' )

    testRPN( 'rpn 19978 tetrahedral' )

    testRPN( 'rpn 87 tetranacci' )

    testRPN( 'rpn 3 2 tetrate' )

    testRPN( 'rpn 45 thabit' )

    testRPN( 'rpn 123 456 789 trianglearea' )

    testRPN( 'rpn 203 triangular' )

    testRPN( 'rpn 20706 triangular?' )

    testRPN( 'rpn 1 20 range tribonacci' )
    testRPN( 'rpn -c -a 2800 10239 tribonacci' )

    testRPN( 'rpn 1 10 range triplebal' )
    testRPN( 'rpn 5588 triplebal' )

    testRPN( 'rpn 1 10 range triplebal_' )
    testRPN( 'rpn 6329 triplebal_' )

    testRPN( 'rpn 1 10 range tripletprime' )
    testRPN( 'rpn 192834 tripletprime' )

    testRPN( 'rpn 394 truncoct' )

    testRPN( 'rpn 683 trunctet' )

    testRPN( 'rpn 1 20 range twinprime' )
    testRPN( 'rpn 39485 twinprime' )

    testRPN( 'rpn 1 10 range twinprime_' )
    testRPN( 'rpn 57454632 twinprime_' )

    testRPN( 'rpn 290 uchar' )

    testRPN( 'rpn 200 8 uinteger' )

    testRPN( 'rpn 234567890 ulong' )

    testRPN( 'rpn 12345678901234567890 ulonglong' )

    testRPN( 'rpn 7 unitroots' )

    testRPN( 'rpn 23456 ushort' )

    testRPN( 'rpn 0x1939 0x3948 xor' )

    testRPN( 'rpn 14578 seconds ydhms' )

    testRPN( 'rpn 4 zeta' )

    testRPN( 'rpn 142857 ~' )

    testRPN( 'rpn 1 10 range altsign' )

    testRPN( 'rpn 1 10 range altsign2' )

    testRPN( 'rpn 1 10 range altsum' )

    testRPN( 'rpn 1 10 range altsum2' )

    testRPN( 'rpn 1 10 range 45 50 range append' )
    testRPN( 'rpn 1 10 range 11 20 range append 21 30 range append' )

    testRPN( 'rpn 1 10 range 2 base' )
    testRPN( 'rpn 1 10 range 3 base' )
    testRPN( 'rpn 1 10 range 4 base' )
    testRPN( 'rpn 1 10 range 5 base' )
    testRPN( 'rpn 1 10 range 6 base' )
    testRPN( 'rpn 1 10 range 7 base' )
    testRPN( 'rpn 1 10 range 8 base' )
    testRPN( 'rpn 1 10 range 9 base' )
    testRPN( 'rpn -p30 1 20 range 11 base' )
    testRPN( 'rpn -p30 1 20 range 12 base' )
    testRPN( 'rpn -p30 1 20 range 13 base' )
    testRPN( 'rpn -p30 1 20 range 14 base' )
    testRPN( 'rpn -p30 1 20 range 15 base' )
    testRPN( 'rpn -p30 1 20 range 16 base' )
    testRPN( 'rpn -p30 1 20 range 17 base' )
    testRPN( 'rpn -p30 1 20 range 18 base' )
    testRPN( 'rpn -p30 1 20 range 19 base' )
    testRPN( 'rpn -p30 1 20 range 20 base' )

    testRPN( 'rpn 1 10 range cf' )

    testRPN( 'rpn 1 10 range count' )

    testRPN( 'rpn 1 10 range diffs' )
    testRPN( 'rpn 1 10 range fib diffs' )

    testRPN( 'rpn 1 10 range diffs2' )
    testRPN( 'rpn 1 10 range fib diffs2' )

    testRPN( 'rpn pi double' )
    testRPN( 'rpn 0x400921fb54442d18 undouble' )
    testRPN( 'rpn 0xcdcdcdcdcdcdcdcd undouble' )

    testRPN( 'rpn pi float' )
    testRPN( 'rpn 0x40490fdb unfloat' )
    testRPN( 'rpn 0xcdcdcdcd unfloat' )

    testRPN( 'rpn 1 100 range gcd' )

    testRPN( 'rpn 1 10 range 1 10 range interleave' )

    testRPN( 'rpn 1 10 range 1 8 range intersection' )

    testRPN( 'rpn 1 10 range 2 5 range 17 linearrecur' )

    testRPN( 'rpn 1 10 range max' )

    testRPN( 'rpn maxdouble' )

    testRPN( 'rpn maxfloat' )

    testRPN( 'rpn 1 10 range maxindex' )

    testRPN( 'rpn 1 10 range mean' )

    testRPN( 'rpn 1 10 range min' )

    testRPN( 'rpn mindouble' )

    testRPN( 'rpn minfloat' )

    testRPN( 'rpn 1 10 range minindex' )

    testRPN( 'rpn 1 10 range nonzero' )

    testRPN( 'rpn -x [ 192 168 0 1 ] [ 8 8 8 8 ] pack' )

    testRPN( 'rpn 1 10 range 1 10 range polyadd' )

    testRPN( 'rpn 1 10 range 1 10 range polymul' )

    testRPN( 'rpn [ [ 1 10 range ] [ 1 10 range ] [ 2 11 range ] ] polyprod' )

    testRPN( 'rpn [ [ 1 10 range ] [ 2 11 range ] ] polysum' )

    testRPN( 'rpn 1 10 range 6 polyval' )

    testRPN( 'rpn 1 10 range product' )

    testRPN( 'rpn result' )

    testRPN( 'rpn 1 8 range solve' )

    testRPN( 'rpn 10 1 -1 range2 sort' )

    testRPN( 'rpn 1 10 range sortdesc' )

    testRPN( 'rpn 1 10 range stddev' )

    testRPN( 'rpn 1 10 range sum' )

    testRPN( 'rpn [ 2014 4 30 0 0 0 ] maketime tounixtime' )

    testRPN( 'rpn -c -a30 [ 2 3 2 ] tower' )

    testRPN( 'rpn [ 4 4 4 ] tower2' )

    testRPN( 'rpn 1 10 range 11 20 range union' )

    testRPN( 'rpn 1 10 range unique' )
    testRPN( 'rpn 1 10 range 1 10 range append unique' )
    testRPN( 'rpn [ 1 10 range 10 dup ] unique' )

    testRPN( 'rpn 503942034 [ 3 4 5 11 4 4 ] unpack' )

    testRPN( 'rpn 1965 year_calendar' )
    testRPN( 'rpn today year_calendar' )

    testRPN( 'rpn -10 10 range zero' )
    testRPN( 'rpn 1 10 range zero' )

    testRPN( 'rpn today 7 days +' )
    testRPN( 'rpn today 2 months -' )
    testRPN( 'rpn today 3 weeks +' )
    testRPN( 'rpn today 50 years +' )

    testRPN( 'rpn today 1965-03-31 -' )
    testRPN( 'rpn 2015-01-01 1965-03-31 -' )
    testRPN( 'rpn 2015 dst_start' )
    testRPN( 'rpn 2015 dst_end' )
    testRPN( 'rpn 2015 easter' )
    testRPN( 'rpn 2015 election_day' )
    testRPN( 'rpn today iso_day' )
    testRPN( 'rpn today julian_day' )
    testRPN( 'rpn 2015 labor_day' )
    testRPN( 'rpn 2015 memorial_day' )
    testRPN( 'rpn 2015 presidents_day' )
    testRPN( 'rpn 2015 thanksgiving' )
    testRPN( 'rpn 2015 march 4 thursday nthweekday' )
    testRPN( 'rpn 2015 march -1 thursday nthweekday' )
    testRPN( 'rpn 2015 20 thursday nthweekdayofyear' )
    testRPN( 'rpn 2015 -1 thursday nthweekdayofyear' )

    testRPN( 'rpn 4 3 debruijn' )

    testRPN( 'rpn 4 3 less' )
    testRPN( 'rpn 4 3 greater' )
    testRPN( 'rpn 4 3 equal' )
    testRPN( 'rpn 4 3 not_equal' )
    testRPN( 'rpn 4 3 not_less' )
    testRPN( 'rpn 4 3 not_greater' )

    testRPN( 'rpn 5 fibonorial' )
    testRPN( 'rpn -a50 24 fibonorial' )

    testRPN( 'rpn 3 3 i + arg' )
    testRPN( 'rpn 3 3 i + conj' )

    testRPN( 'rpn 1 100 range geomean' )
    testRPN( 'rpn [ 1 10 range 1 20 range 1 30 range ] geomean' )

    testRPN( 'rpn help' )
    testRPN( 'rpn help about' )
    testRPN( 'rpn help arithmetic' )
    testRPN( 'rpn help add' )

    testRPN( 'rpn _dumpalias' )
    testRPN( 'rpn _dumpops' )
    testRPN( 'rpn _stats' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runTests( )
    runConvertTests( )

