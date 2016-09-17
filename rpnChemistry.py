#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnChemistry.py
# //
# //  RPN command-line calculator chemistry functions
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import rpnGlobals as g

from rpnMeasurement import RPNMeasurement

from mpmath import fadd, fdiv, fmul, fsub, mpmathify


# //******************************************************************************
# //
# //  loadChemistryTables
# //
# //  The table key is Atomic number.
# //
# //  The columns are:  Name, Atomic Symbol, Group, Period, Block, State (at STP),
# //  Occurrence, Description, Weight Low, Weight High
# //
# //  http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=&ascii=html&isotype=some
# //  https://en.wikipedia.org/wiki/Densities_of_the_elements_%28data_page%29
# //
# //******************************************************************************

def loadChemistryTables( ):
    g.elements = {
        1 :   [ 'Hydrogen',       'H',   1,   1,   's',  'Gas',     'Primordial',  'Diatomic nonmetal',       mpmathify( '1.00784' ),       mpmathify( '1.00811' ),         mpmathify( '0.00008988' ),      ],
        2 :   [ 'Helium',         'He',  18,  1,   's',  'Gas',     'Primordial',  'Noble gas',               mpmathify( '4.002601' ),      mpmathify( '4.002603' ),        mpmathify( '0.0001786' ),       ],
        3 :   [ 'Lithium',        'Li',  1,   2,   's',  'Solid',   'Primordial',  'Alkali metal',            mpmathify( '6.938' ),         mpmathify( '6.997' ),           mpmathify( '0.534' ),           ],
        4 :   [ 'Beryllium',      'Be',  2,   2,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    mpmathify( '9.01218285' ),    mpmathify( '9.01218335' ),      mpmathify( '1.85' ),            ],
        5 :   [ 'Boron',          'B',   13,  2,   'p',  'Solid',   'Primordial',  'Metalloid',               mpmathify( '10.806' ),        mpmathify( '10.821' ),          mpmathify( '2.34' ),            ],
        6 :   [ 'Carbon',         'C',   14,  2,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     mpmathify( '12.0096' ),       mpmathify( '12.0116' ),         mpmathify( '2.267' ),           ],
        7 :   [ 'Nitrogen',       'N',   15,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       mpmathify( '14.00643' ),      mpmathify( '14.00728' ),        mpmathify( '0.001251' ),        ],
        8 :   [ 'Oxygen',         'O',   16,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       mpmathify( '15.99903' ),      mpmathify( '15.99977' ),        mpmathify( '0.001429' ),        ],
        9 :   [ 'Fluorine',       'F',   17,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       mpmathify( '18.998403160' ),  mpmathify( '18.998403166' ),    mpmathify( '0.0017' ),          ],
        10 :  [ 'Neon',           'Ne',  18,  2,   'p',  'Gas',     'Primordial',  'Noble gas',               mpmathify( '20.1794' ),       mpmathify( '20.1800' ),         mpmathify( '0.0009002' ),       ],
        11 :  [ 'Sodium',         'Na',  1,   3,   's',  'Solid',   'Primordial',  'Alkali metal',            mpmathify( '22.98976927' ),   mpmathify( '22.98976929' ),     mpmathify( '0.968' ),           ],
        12 :  [ 'Magnesium',      'Mg',  2,   3,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    mpmathify( '24.304' ),        mpmathify( '24.307' ),          mpmathify( '1.738' ),           ],
        13 :  [ 'Aluminium',      'Al',  13,  3,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '26.98153815' ),   mpmathify( '26.98153885' ),     mpmathify( '2.70' ),            ],
        14 :  [ 'Silicon',        'Si',  14,  3,   'p',  'Solid',   'Primordial',  'Metalloid',               mpmathify( '28.084' ),        mpmathify( '28.086' ),          mpmathify( '2.33' ),            ],
        15 :  [ 'Phosphorus',     'P',   15,  3,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     mpmathify( '30.9737619955' ), mpmathify( '30.9737620005' ),   mpmathify( '1.823' ),           ],
        16 :  [ 'Sulfur',         'S',   16,  3,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     mpmathify( '32.059' ),        mpmathify( '32.076' ),          mpmathify( '2.08' ),            ],
        17 :  [ 'Chlorine',       'Cl',  17,  3,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       mpmathify( '35.446' ),        mpmathify( '35.457' ),          mpmathify( '0.0032' ),          ],
        18 :  [ 'Argon',          'Ar',  18,  3,   'p',  'Gas',     'Primordial',  'Noble gas',               mpmathify( '39.9485' ),       mpmathify( '39.9475' ),         mpmathify( '0.001784' ),        ],
        19 :  [ 'Potassium',      'K',   1,   4,   's',  'Solid',   'Primordial',  'Alkali metal',            mpmathify( '39.09825' ),      mpmathify( '39.09835' ),        mpmathify( '0.89' ),            ],
        20 :  [ 'Calcium',        'Ca',  2,   4,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    mpmathify( '40.076' ),        mpmathify( '40.080' ),          mpmathify( '1.55' ),            ],
        21 :  [ 'Scandium',       'Sc',  3,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '44.9559055' ),    mpmathify( '44.9559105' ),      mpmathify( '2.985' ),           ],
        22 :  [ 'Titanium',       'Ti',  4,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '47.8665' ),       mpmathify( '47.8675' ),         mpmathify( '4.506' ),           ],
        23 :  [ 'Vanadium',       'V',   5,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '50.94145' ),      mpmathify( '50.94155' ),        mpmathify( '6.0' ),             ],
        24 :  [ 'Chromium',       'Cr',  6,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '51.9958' ),       mpmathify( '51.9964' ),         mpmathify( '7.15' ),            ],
        25 :  [ 'Manganese',      'Mn',  7,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '54.9380425' ),    mpmathify( '54.9380455' ),      mpmathify( '7.21' ),            ],
        26 :  [ 'Iron',           'Fe',  8,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '55.844' ),        mpmathify( '55.846' ),          mpmathify( '7.86' ),            ],
        27 :  [ 'Cobalt',         'Co',  9,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '58.933192' ),     mpmathify( '58.933196' ),       mpmathify( '8.90' ),            ],
        28 :  [ 'Nickel',         'Ni',  10,  4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '58.6932' ),       mpmathify( '58.6936' ),         mpmathify( '8.908' ),           ],
        29 :  [ 'Copper',         'Cu',  11,  4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '64.5445' ),       mpmathify( '64.5475' ),         mpmathify( '8.96' ),            ],
        30 :  [ 'Zinc',           'Zn',  12,  4,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '65.37' ),         mpmathify( '65.39' ),           mpmathify( '7.14' ),            ],
        31 :  [ 'Gallium',        'Ga',  13,  4,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '69.7225' ),       mpmathify( '69.7235' ),         mpmathify( '5.91' ),            ],
        32 :  [ 'Germanium',      'Ge',  14,  4,   'p',  'Solid',   'Primordial',  'Metalloid',               mpmathify( '72.626' ),        mpmathify( '72.634' ),          mpmathify( '5.323' ),           ],
        33 :  [ 'Arsenic',        'As',  15,  4,   'p',  'Solid',   'Primordial',  'Metalloid',               mpmathify( '74.921592' ),     mpmathify( '74.921598' ),       mpmathify( '5.727' ),           ],
        34 :  [ 'Selenium',       'Se',  16,  4,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     mpmathify( '78.967' ),        mpmathify( '78.975' ),          mpmathify( '4.81' ),            ],
        35 :  [ 'Bromine',        'Br',  17,  4,   'p',  'Liquid',  'Primordial',  'Diatomic nonmetal',       mpmathify( '79.901' ),        mpmathify( '79.907' ),          mpmathify( '3.1028' ),          ],
        36 :  [ 'Krypton',        'Kr',  18,  4,   'p',  'Gas',     'Primordial',  'Noble gas',               mpmathify( '83.797' ),        mpmathify( '83.799' ),          mpmathify( '0.003749' ),        ],
        37 :  [ 'Rubidium',       'Rb',  1,   5,   's',  'Solid',   'Primordial',  'Alkali metal',            mpmathify( '85.46765' ),      mpmathify( '85.46795' ),        mpmathify( '1.532' ),           ],
        38 :  [ 'Strontium',      'Sr',  2,   5,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    mpmathify( '87.615' ),        mpmathify( '87.625' ),          mpmathify( '2.64' ),            ],
        39 :  [ 'Yttrium',        'Y',   3,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '88.90583' ),      mpmathify( '88.90585' ),        mpmathify( '4.472' ),           ],
        40 :  [ 'Zirconium',      'Zr',  4,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '91.223' ),        mpmathify( '91.225' ),          mpmathify( '6.52' ),            ],
        41 :  [ 'Niobium',        'Nb',  5,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '92.90636' ),      mpmathify( '92.90638' ),        mpmathify( '8.57' ),            ],
        42 :  [ 'Molybdenum',     'Mo',  6,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '95.945' ),        mpmathify( '95.955' ),          mpmathify( '10.28' ),           ],
        43 :  [ 'Technetium',     'Tc',  7,   5,   'd',  'Solid',   'Transient',   'Transition metal',        mpmathify( '98' ),            mpmathify( '98' ),              mpmathify( '11.0' ),            ],
        44 :  [ 'Ruthenium',      'Ru',  8,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '101.06' ),        mpmathify( '101.08' ),          mpmathify( '12.45' ),           ],
        45 :  [ 'Rhodium',        'Rh',  9,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '102.90549' ),     mpmathify( '102.90551' ),       mpmathify( '12.41' ),           ],
        46 :  [ 'Palladium',      'Pd',  10,  5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '106.415' ),       mpmathify( '106.425' ),         mpmathify( '12.023' ),          ],
        47 :  [ 'Silver',         'Ag',  11,  5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '107.8681' ),      mpmathify( '107.8683' ),        mpmathify( '10.49' ),           ],
        48 :  [ 'Cadmium',        'Cd',  12,  5,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '112.412' ),       mpmathify( '112.416' ),         mpmathify( '8.65' ),            ],
        49 :  [ 'Indium',         'In',  13,  5,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '114.8175' ),      mpmathify( '114.8185' ),        mpmathify( '7.31' ),            ],
        50 :  [ 'Tin',            'Sn',  14,  5,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '118.7065' ),      mpmathify( '118.7135' ),        mpmathify( '7.265' ),           ],
        51 :  [ 'Antimony',       'Sb',  15,  5,   'p',  'Solid',   'Primordial',  'Metalloid',               mpmathify( '121.7595' ),      mpmathify( '121.7605' ),        mpmathify( '6.697' ),           ],
        52 :  [ 'Tellurium',      'Te',  16,  5,   'p',  'Solid',   'Primordial',  'Metalloid',               mpmathify( '127.585' ),       mpmathify( '127.615' ),         mpmathify( '6.24' ),            ],
        53 :  [ 'Iodine',         'I',   17,  5,   'p',  'Solid',   'Primordial',  'Diatomic nonmetal',       mpmathify( '126.904455' ),    mpmathify( '126.904485' ),      mpmathify( '4.933' ),           ],
        54 :  [ 'Xenon',          'Xe',  18,  5,   'p',  'Gas',     'Primordial',  'Noble gas',               mpmathify( '131.290' ),       mpmathify( '131.296' ),         mpmathify( '0.005894' ),        ],
        55 :  [ 'Caesium',        'Cs',  1,   6,   's',  'Solid',   'Primordial',  'Alkali metal',            mpmathify( '132.90545193' ),  mpmathify( '132.90545199' ),    mpmathify( '1.93' ),            ],
        56 :  [ 'Barium',         'Ba',  2,   6,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    mpmathify( '137.3235' ),      mpmathify( '137.3305' ),        mpmathify( '3.51' ),            ],
        57 :  [ 'Lanthanum',      'La',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '138.905435' ),    mpmathify( '138.905505' ),      mpmathify( '6.162' ),           ],
        58 :  [ 'Cerium',         'Ce',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '140.1155' ),      mpmathify( '140.1165' ),        mpmathify( '6.770' ),           ],
        59 :  [ 'Praseodymium',   'Pr',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '140.90765' ),     mpmathify( '140.90767' ),       mpmathify( '6.77' ),            ],
        60 :  [ 'Neodymium',      'Nd',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '144.2405' ),      mpmathify( '144.2435' ),        mpmathify( '7.01' ),            ],
        61 :  [ 'Promethium',     'Pm',  3,   6,   'f',  'Solid',   'Transient',   'Lanthanide',              mpmathify( '145' ),           mpmathify( '145' ),             mpmathify( '7.26' ),            ],
        62 :  [ 'Samarium',       'Sm',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '150.35' ),        mpmathify( '150.37' ),          mpmathify( '7.52' ),            ],
        63 :  [ 'Europium',       'Eu',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '151.9635' ),      mpmathify( '151.9645' ),        mpmathify( '5.244' ),           ],
        64 :  [ 'Gadolinium',     'Gd',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '157.235' ),       mpmathify( '157.265' ),         mpmathify( '7.90' ),            ],
        65 :  [ 'Terbium',        'Tb',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '158.92534' ),     mpmathify( '158.92536' ),       mpmathify( '8.23' ),            ],
        66 :  [ 'Dysprosium',     'Dy',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '162.4995' ),      mpmathify( '162.5005' ),        mpmathify( '8.540' ),           ],
        67 :  [ 'Holmium',        'Ho',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '164.93032' ),     mpmathify( '164.93034' ),       mpmathify( '8.79' ),            ],
        68 :  [ 'Erbium',         'Er',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '167.2575' ),      mpmathify( '167.2605' ),        mpmathify( '9.066' ),           ],
        69 :  [ 'Thulium',        'Tm',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '168.93421' ),     mpmathify( '168.93423' ),       mpmathify( '9.32' ),            ],
        70 :  [ 'Ytterbium',      'Yb',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '173.0515' ),      mpmathify( '173.0565' ),        mpmathify( '6.90' ),            ],
        71 :  [ 'Lutetium',       'Lu',  3,   6,   'd',  'Solid',   'Primordial',  'Lanthanide',              mpmathify( '174.96675' ),     mpmathify( '174.96685' ),       mpmathify( '9.841' ),           ],
        72 :  [ 'Hafnium',        'Hf',  4,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '178.48' ),        mpmathify( '178.50' ),          mpmathify( '13.31' ),           ],
        73 :  [ 'Tantalum',       'Ta',  5,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '180.94787' ),     mpmathify( '180.94789' ),       mpmathify( '16.69' ),           ],
        74 :  [ 'Tungsten',       'W',   6,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '183.835' ),       mpmathify( '183.845' ),         mpmathify( '19.25' ),           ],
        75 :  [ 'Rhenium',        'Re',  7,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '186.2065' ),      mpmathify( '186.2075' ),        mpmathify( '21.02' ),           ],
        76 :  [ 'Osmium',         'Os',  8,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '190.215' ),       mpmathify( '190.245' ),         mpmathify( '22.59' ),           ],
        77 :  [ 'Iridium',        'Ir',  9,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '192.2155' ),      mpmathify( '192.2185' ),        mpmathify( '22.56' ),           ],
        78 :  [ 'Platinum',       'Pt',  10,  6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '195.0795' ),      mpmathify( '195.0885' ),        mpmathify( '21.45' ),           ],
        79 :  [ 'Gold',           'Au',  11,  6,   'd',  'Solid',   'Primordial',  'Transition metal',        mpmathify( '196.9665665' ),   mpmathify( '196.9665715' ),     mpmathify( '19.3' ),            ],
        80 :  [ 'Mercury',        'Hg',  12,  6,   'd',  'Liquid',  'Primordial',  'Transition metal',        mpmathify( '200.5905' ),      mpmathify( '200.5935' ),        mpmathify( '13.534' ),          ],
        81 :  [ 'Thallium',       'Tl',  13,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '204.382' ),       mpmathify( '204.385' ),         mpmathify( '11.85' ),           ],
        82 :  [ 'Lead',           'Pb',  14,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '207.15' ),        mpmathify( '207.25' ),          mpmathify( '11.34' ),           ],
        83 :  [ 'Bismuth',        'Bi',  15,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',   mpmathify( '208.980395' ),    mpmathify( '208.980405' ),      mpmathify( '9.78' ),            ],
        84 :  [ 'Polonium',       'Po',  16,  6,   'p',  'Solid',   'Transient',   'Post-transition metal',   mpmathify( '209' ),           mpmathify( '209' ),             mpmathify( '9.398' ),           ],
        85 :  [ 'Astatine',       'At',  17,  6,   'p',  'Solid',   'Transient',   'Metalloid',               mpmathify( '210' ),           mpmathify( '210' ),             mpmathify( '0' ),               ],
        86 :  [ 'Radon',          'Rn',  18,  6,   'p',  'Gas',     'Transient',   'Noble gas',               mpmathify( '222' ),           mpmathify( '222' ),             mpmathify( '0.00973' ),         ],
        87 :  [ 'Francium',       'Fr',  1,   7,   's',  'Solid',   'Transient',   'Alkali metal',            mpmathify( '223' ),           mpmathify( '223' ),             mpmathify( '1.87' ),            ],
        88 :  [ 'Radium',         'Ra',  2,   7,   's',  'Solid',   'Transient',   'Alkaline earth metal',    mpmathify( '226' ),           mpmathify( '226' ),             mpmathify( '5.5' ),             ],
        89 :  [ 'Actinium',       'Ac',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                mpmathify( '227' ),           mpmathify( '227' ),             mpmathify( '10.0' ),            ],
        90 :  [ 'Thorium',        'Th',  3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                mpmathify( '232.0375' ),      mpmathify( '232.0379' ),        mpmathify( '11.7' ),            ],
        91 :  [ 'Protactinium',   'Pa',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                mpmathify( '231.03587' ),     mpmathify( '231.03589' ),       mpmathify( '15.37' ),           ],
        92 :  [ 'Uranium',        'U',   3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                mpmathify( '238.028895' ),    mpmathify( '238.028925' ),      mpmathify( '19.1' ),            ],
        93 :  [ 'Neptunium',      'Np',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                mpmathify( '237' ),           mpmathify( '237' ),             mpmathify( '20.2' ),            ],
        94 :  [ 'Plutonium',      'Pu',  3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                mpmathify( '244' ),           mpmathify( '244' ),             mpmathify( '19.816' ),          ],
        95 :  [ 'Americium',      'Am',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                mpmathify( '243' ),           mpmathify( '243' ),             mpmathify( '12.0' ),            ],
        96 :  [ 'Curium',         'Cm',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                mpmathify( '247' ),           mpmathify( '247' ),             mpmathify( '13.51' ),           ],
        97 :  [ 'Berkelium',      'Bk',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                mpmathify( '247' ),           mpmathify( '247' ),             mpmathify( '14.78' ),           ],
        98 :  [ 'Californium',    'Cf',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                mpmathify( '251' ),           mpmathify( '251' ),             mpmathify( '15.1' ),            ],
        99 :  [ 'Einsteinium',    'Es',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                mpmathify( '252' ),           mpmathify( '252' ),             mpmathify( '8.84' ),            ],
        100 : [ 'Fermium',        'Fm',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                mpmathify( '257' ),           mpmathify( '257' ),             mpmathify( '0' ),               ],
        101 : [ 'Mendelevium',    'Md',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                mpmathify( '258' ),           mpmathify( '258' ),             mpmathify( '0' ),               ],
        102 : [ 'Nobelium',       'No',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                mpmathify( '259' ),           mpmathify( '259' ),             mpmathify( '0' ),               ],
        103 : [ 'Lawrencium',     'Lr',  3,   7,   'd',  'unknown', 'Synthetic',   'Actinide',                mpmathify( '262' ),           mpmathify( '262' ),             mpmathify( '0' ),               ],
        104 : [ 'Rutherfordium',  'Rf',  4,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        mpmathify( '267' ),           mpmathify( '267' ),             mpmathify( '0' ),               ],
        105 : [ 'Dubnium',        'Db',  5,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        mpmathify( '268' ),           mpmathify( '268' ),             mpmathify( '0' ),               ],
        106 : [ 'Seaborgium',     'Sg',  6,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        mpmathify( '271' ),           mpmathify( '271' ),             mpmathify( '0' ),               ],
        107 : [ 'Bohrium',        'Bh',  7,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        mpmathify( '272' ),           mpmathify( '272' ),             mpmathify( '0' ),               ],
        108 : [ 'Hassium',        'Hs',  8,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        mpmathify( '270' ),           mpmathify( '270' ),             mpmathify( '0' ),               ],
        109 : [ 'Meitnerium',     'Mt',  9,   7,   'd',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '276' ),           mpmathify( '276' ),             mpmathify( '0' ),               ],
        110 : [ 'Darmstadtium',   'Ds',  10,  7,   'd',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '281' ),           mpmathify( '281' ),             mpmathify( '0' ),               ],
        111 : [ 'Roentgenium',    'Rg',  11,  7,   'd',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '280' ),           mpmathify( '280' ),             mpmathify( '0' ),               ],
        112 : [ 'Copernicium',    'Cn',  12,  7,   'd',  'unknown', 'Synthetic',   'Transition metal',        mpmathify( '285' ),           mpmathify( '285' ),             mpmathify( '0' ),               ],
        113 : [ 'Nihonium',       'Nh',  13,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '284' ),           mpmathify( '284' ),             mpmathify( '0' ),               ],
        114 : [ 'Flerovium',      'Fl',  14,  7,   'p',  'unknown', 'Synthetic',   'Post-transition metal',   mpmathify( '289' ),           mpmathify( '289' ),             mpmathify( '0' ),               ],
        115 : [ 'Moscovium',      'Mc',  15,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '288' ),           mpmathify( '288' ),             mpmathify( '0' ),               ],
        116 : [ 'Livermorium',    'Lv',  16,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '293' ),           mpmathify( '293' ),             mpmathify( '0' ),               ],
        117 : [ 'Tennessine',     'Ts',  17,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '294' ),           mpmathify( '294' ),             mpmathify( '0' ),               ],
        118 : [ 'Oganesson',      'Og',  18,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 mpmathify( '294' ),           mpmathify( '294' ),             mpmathify( '0' ),               ],
    }

    g.atomic_numbers = { }
    for k, v in g.elements.items( ):
        g.atomic_numbers[ v[ 1 ] ] = k


# //******************************************************************************
# //
# //  getElementAttribute
# //
# //******************************************************************************

def getElementAttribute( n, k ):
    if int( n ) < 1 or n > 118:
        raise ValueError( 'invalid atomic number' )

    if ( 0 > k > 7 ):
        raise ValueError( 'invalid element attribute' )

    if g.elements is None:
        loadChemistryTables( )

    return g.elements[ int( n ) ][ k ]


# //******************************************************************************
# //
# //  getAtomicNumber
# //
# //******************************************************************************

def getAtomicNumber( n ):
    if g.elements is None:
        loadChemistryTables( )

    if n not in g.atomic_numbers:
        raise ValueError( 'invalid atomic symbol' )

    return g.atomic_numbers[ n ]


# //******************************************************************************
# //
# //  getAtomicWeight
# //
# //******************************************************************************

def getAtomicWeight( n ):
    return fdiv( fadd( getElementAttribute( n, 9 ), getElementAttribute( n, 8 ) ), 2 )


# //******************************************************************************
# //
# //  getElementDensity
# //
# //******************************************************************************

def getElementDensity( n ):
    return RPNMeasurement( getElementAttribute( n, 10 ), 'g/cm^3' )


