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


# //******************************************************************************
# //
# //  loadChemistryTables
# //
# //  The table key is Atomic number.
# //
# //  The columns are:  Name, Atomic Symbol, Group, Period, Block, State (at STP),
# //  Occurrence, Description
# //
# //******************************************************************************

def loadChemistryTables( ):
    g.elements = {
        1 :   [ 'Hydrogen',       'H',   1,   1,   's',  'Gas',     'Primordial',  'Diatomic nonmetal',            ],
        2 :   [ 'Helium',         'He',  18,  1,   's',  'Gas',     'Primordial',  'Noble gas',                    ],
        3 :   [ 'Lithium',        'Li',  1,   2,   's',  'Solid',   'Primordial',  'Alkali metal',                 ],
        4 :   [ 'Beryllium',      'Be',  2,   2,   's',  'Solid',   'Primordial',  'Alkaline earth metal',         ],
        5 :   [ 'Boron',          'B',   13,  2,   'p',  'Solid',   'Primordial',  'Metalloid',                    ],
        6 :   [ 'Carbon',         'C',   14,  2,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',          ],
        7 :   [ 'Nitrogen',       'N',   15,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',            ],
        8 :   [ 'Oxygen',         'O',   16,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',            ],
        9 :   [ 'Fluorine',       'F',   17,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',            ],
        10 :  [ 'Neon',           'Ne',  18,  2,   'p',  'Gas',     'Primordial',  'Noble gas',                    ],
        11 :  [ 'Sodium',         'Na',  1,   3,   's',  'Solid',   'Primordial',  'Alkali metal',                 ],
        12 :  [ 'Magnesium',      'Mg',  2,   3,   's',  'Solid',   'Primordial',  'Alkaline earth metal',         ],
        13 :  [ 'Aluminium',      'Al',  13,  3,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        14 :  [ 'Silicon',        'Si',  14,  3,   'p',  'Solid',   'Primordial',  'Metalloid',                    ],
        15 :  [ 'Phosphorus',     'P',   15,  3,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',          ],
        16 :  [ 'Sulfur',         'S',   16,  3,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',          ],
        17 :  [ 'Chlorine',       'Cl',  17,  3,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',            ],
        18 :  [ 'Argon',          'Ar',  18,  3,   'p',  'Gas',     'Primordial',  'Noble gas',                    ],
        19 :  [ 'Potassium',      'K',   1,   4,   's',  'Solid',   'Primordial',  'Alkali metal',                 ],
        20 :  [ 'Calcium',        'Ca',  2,   4,   's',  'Solid',   'Primordial',  'Alkaline earth metal',         ],
        21 :  [ 'Scandium',       'Sc',  3,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        22 :  [ 'Titanium',       'Ti',  4,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        23 :  [ 'Vanadium',       'V',   5,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        24 :  [ 'Chromium',       'Cr',  6,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        25 :  [ 'Manganese',      'Mn',  7,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        26 :  [ 'Iron',           'Fe',  8,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        27 :  [ 'Cobalt',         'Co',  9,   4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        28 :  [ 'Nickel',         'Ni',  10,  4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        29 :  [ 'Copper',         'Cu',  11,  4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        30 :  [ 'Zinc',           'Zn',  12,  4,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        31 :  [ 'Gallium',        'Ga',  13,  4,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        32 :  [ 'Germanium',      'Ge',  14,  4,   'p',  'Solid',   'Primordial',  'Metalloid',                    ],
        33 :  [ 'Arsenic',        'As',  15,  4,   'p',  'Solid',   'Primordial',  'Metalloid',                    ],
        34 :  [ 'Selenium',       'Se',  16,  4,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',          ],
        35 :  [ 'Bromine',        'Br',  17,  4,   'p',  'Liquid',  'Primordial',  'Diatomic nonmetal',            ],
        36 :  [ 'Krypton',        'Kr',  18,  4,   'p',  'Gas',     'Primordial',  'Noble gas',                    ],
        37 :  [ 'Rubidium',       'Rb',  1,   5,   's',  'Solid',   'Primordial',  'Alkali metal',                 ],
        38 :  [ 'Strontium',      'Sr',  2,   5,   's',  'Solid',   'Primordial',  'Alkaline earth metal',         ],
        39 :  [ 'Yttrium',        'Y',   3,   5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        40 :  [ 'Zirconium',      'Zr',  4,   5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        41 :  [ 'Niobium',        'Nb',  5,   5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        42 :  [ 'Molybdenum',     'Mo',  6,   5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        43 :  [ 'Technetium',     'Tc',  7,   5,   'd',  'Solid',   'Transient',   'Transition metal',             ],
        44 :  [ 'Ruthenium',      'Ru',  8,   5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        45 :  [ 'Rhodium',        'Rh',  9,   5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        46 :  [ 'Palladium',      'Pd',  10,  5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        47 :  [ 'Silver',         'Ag',  11,  5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        48 :  [ 'Cadmium',        'Cd',  12,  5,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        49 :  [ 'Indium',         'In',  13,  5,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        50 :  [ 'Tin',            'Sn',  14,  5,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        51 :  [ 'Antimony',       'Sb',  15,  5,   'p',  'Solid',   'Primordial',  'Metalloid',                    ],
        52 :  [ 'Tellurium',      'Te',  16,  5,   'p',  'Solid',   'Primordial',  'Metalloid',                    ],
        53 :  [ 'Iodine',         'I',   17,  5,   'p',  'Solid',   'Primordial',  'Diatomic nonmetal',            ],
        54 :  [ 'Xenon',          'Xe',  18,  5,   'p',  'Gas',     'Primordial',  'Noble gas',                    ],
        55 :  [ 'Caesium',        'Cs',  1,   6,   's',  'Solid',   'Primordial',  'Alkali metal',                 ],
        56 :  [ 'Barium',         'Ba',  2,   6,   's',  'Solid',   'Primordial',  'Alkaline earth metal',         ],
        57 :  [ 'Lanthanum',      'La',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        58 :  [ 'Cerium',         'Ce',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        59 :  [ 'Praseodymium',   'Pr',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        60 :  [ 'Neodymium',      'Nd',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        61 :  [ 'Promethium',     'Pm',  3,   6,   'f',  'Solid',   'Transient',   'Lanthanide',                   ],
        62 :  [ 'Samarium',       'Sm',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        63 :  [ 'Europium',       'Eu',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        64 :  [ 'Gadolinium',     'Gd',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        65 :  [ 'Terbium',        'Tb',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        66 :  [ 'Dysprosium',     'Dy',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        67 :  [ 'Holmium',        'Ho',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        68 :  [ 'Erbium',         'Er',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        69 :  [ 'Thulium',        'Tm',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        70 :  [ 'Ytterbium',      'Yb',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',                   ],
        71 :  [ 'Lutetium',       'Lu',  3,   6,   'd',  'Solid',   'Primordial',  'Lanthanide',                   ],
        72 :  [ 'Hafnium',        'Hf',  4,   6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        73 :  [ 'Tantalum',       'Ta',  5,   6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        74 :  [ 'Tungsten',       'W',   6,   6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        75 :  [ 'Rhenium',        'Re',  7,   6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        76 :  [ 'Osmium',         'Os',  8,   6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        77 :  [ 'Iridium',        'Ir',  9,   6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        78 :  [ 'Platinum',       'Pt',  10,  6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        79 :  [ 'Gold',           'Au',  11,  6,   'd',  'Solid',   'Primordial',  'Transition metal',             ],
        80 :  [ 'Mercury',        'Hg',  12,  6,   'd',  'Liquid',  'Primordial',  'Transition metal',             ],
        81 :  [ 'Thallium',       'Tl',  13,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        82 :  [ 'Lead',           'Pb',  14,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        83 :  [ 'Bismuth',        'Bi',  15,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',        ],
        84 :  [ 'Polonium',       'Po',  16,  6,   'p',  'Solid',   'Transient',   'Post-transition metal',        ],
        85 :  [ 'Astatine',       'At',  17,  6,   'p',  'Solid',   'Transient',   'Metalloid',                    ],
        86 :  [ 'Radon',          'Rn',  18,  6,   'p',  'Gas',     'Transient',   'Noble gas',                    ],
        87 :  [ 'Francium',       'Fr',  1,   7,   's',  'Solid',   'Transient',   'Alkali metal',                 ],
        88 :  [ 'Radium',         'Ra',  2,   7,   's',  'Solid',   'Transient',   'Alkaline earth metal',         ],
        89 :  [ 'Actinium',       'Ac',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                     ],
        90 :  [ 'Thorium',        'Th',  3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                     ],
        91 :  [ 'Protactinium',   'Pa',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                     ],
        92 :  [ 'Uranium',        'U',   3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                     ],
        93 :  [ 'Neptunium',      'Np',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                     ],
        94 :  [ 'Plutonium',      'Pu',  3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                     ],
        95 :  [ 'Americium',      'Am',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                     ],
        96 :  [ 'Curium',         'Cm',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                     ],
        97 :  [ 'Berkelium',      'Bk',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                     ],
        98 :  [ 'Californium',    'Cf',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                     ],
        99 :  [ 'Einsteinium',    'Es',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                     ],
        100 : [ 'Fermium',        'Fm',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                     ],
        101 : [ 'Mendelevium',    'Md',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                     ],
        102 : [ 'Nobelium',       'No',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                     ],
        103 : [ 'Lawrencium',     'Lr',  3,   7,   'd',  'unknown', 'Synthetic',   'Actinide',                     ],
        104 : [ 'Rutherfordium',  'Rf',  4,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',             ],
        105 : [ 'Dubnium',        'Db',  5,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',             ],
        106 : [ 'Seaborgium',     'Sg',  6,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',             ],
        107 : [ 'Bohrium',        'Bh',  7,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',             ],
        108 : [ 'Hassium',        'Hs',  8,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',             ],
        109 : [ 'Meitnerium',     'Mt',  9,   7,   'd',  'unknown', 'Synthetic',   'unknown',                      ],
        110 : [ 'Darmstadtium',   'Ds',  10,  7,   'd',  'unknown', 'Synthetic',   'unknown',                      ],
        111 : [ 'Roentgenium',    'Rg',  11,  7,   'd',  'unknown', 'Synthetic',   'unknown',                      ],
        112 : [ 'Copernicium',    'Cn',  12,  7,   'd',  'unknown', 'Synthetic',   'Transition metal',             ],
        113 : [ 'Nihonium',       'Nh',  13,  7,   'p',  'unknown', 'Synthetic',   'unknown',                      ],
        114 : [ 'Flerovium',      'Fl',  14,  7,   'p',  'unknown', 'Synthetic',   'Post-transition metal',        ],
        115 : [ 'Moscovium',      'Mc',  15,  7,   'p',  'unknown', 'Synthetic',   'unknown',                      ],
        116 : [ 'Livermorium',    'Lv',  16,  7,   'p',  'unknown', 'Synthetic',   'unknown',                      ],
        117 : [ 'Tennessine',     'Ts',  17,  7,   'p',  'unknown', 'Synthetic',   'unknown',                      ],
        118 : [ 'Oganesson',      'Og',  18,  7,   'p',  'unknown', 'Synthetic',   'unknown',                      ],
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

