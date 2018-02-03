#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnChemistry.py
# //
# //  RPN command-line calculator chemistry functions
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import string

from mpmath import fadd, fdiv, fmul, fsub, mpmathify

from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnUtils import oneArgFunctionEvaluator

import rpn.rpnGlobals as g


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
# //  https://en.wikipedia.org/wiki/Melting_points_of_the_elements_%28data_page%29
# //  https://en.wikipedia.org/wiki/Boiling_points_of_the_elements_%28data_page%29
# //
# //******************************************************************************

def loadChemistryTables( ):
    g.elements = {
        1 :   [ 'Hydrogen',       'H',   1,   1,   's',  'Gas',     'Primordial',  'Diatomic nonmetal',       '1.00784',       '1.00811',         '0.00008988', '13.99',    '20.271',   ],
        2 :   [ 'Helium',         'He',  18,  1,   's',  'Gas',     'Primordial',  'Noble gas',               '4.002601',      '4.002603',        '0.0001786',  '0',        '4.222',    ],
        3 :   [ 'Lithium',        'Li',  1,   2,   's',  'Solid',   'Primordial',  'Alkali metal',            '6.938',         '6.997',           '0.534',      '453.65',   '1603',     ],
        4 :   [ 'Beryllium',      'Be',  2,   2,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    '9.01218285',    '9.01218335',      '1.85',       '1560',     '2742',     ],
        5 :   [ 'Boron',          'B',   13,  2,   'p',  'Solid',   'Primordial',  'Metalloid',               '10.806',        '10.821',          '2.34',       '2349',     '4200',     ],
        6 :   [ 'Carbon',         'C',   14,  2,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     '12.0096',       '12.0116',         '2.267',      '3800',     '4300',     ],
        7 :   [ 'Nitrogen',       'N',   15,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       '14.00643',      '14.00728',        '0.001251',   '63.15',    '77.355',   ],
        8 :   [ 'Oxygen',         'O',   16,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       '15.99903',      '15.99977',        '0.001429',   '54.36',    '90.188',   ],
        9 :   [ 'Fluorine',       'F',   17,  2,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       '18.998403160',  '18.998403166',    '0.0017',     '53.48',    '85.04',    ],
        10 :  [ 'Neon',           'Ne',  18,  2,   'p',  'Gas',     'Primordial',  'Noble gas',               '20.1794',       '20.1800',         '0.0009002',  '24.56',    '27.104',   ],

        11 :  [ 'Sodium',         'Na',  1,   3,   's',  'Solid',   'Primordial',  'Alkali metal',            '22.98976927',   '22.98976929',     '0.968',      '307.944',  '1156.090', ],
        12 :  [ 'Magnesium',      'Mg',  2,   3,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    '24.304',        '24.307',          '1.738',      '923',      '1363',     ],
        13 :  [ 'Aluminium',      'Al',  13,  3,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '26.98153815',   '26.98153885',     '2.70',       '933.47',   '2743',     ],
        14 :  [ 'Silicon',        'Si',  14,  3,   'p',  'Solid',   'Primordial',  'Metalloid',               '28.084',        '28.086',          '2.33',       '1687',     '3538',     ],
        15 :  [ 'Phosphorus',     'P',   15,  3,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     '30.9737619955', '30.9737620005',   '1.823',      '883',      '550',      ],
        16 :  [ 'Sulfur',         'S',   16,  3,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     '32.059',        '32.076',          '2.08',       '388.36',   '717.8',    ],
        17 :  [ 'Chlorine',       'Cl',  17,  3,   'p',  'Gas',     'Primordial',  'Diatomic nonmetal',       '35.446',        '35.457',          '0.0032',     '171.6',    '239.11',   ],
        18 :  [ 'Argon',          'Ar',  18,  3,   'p',  'Gas',     'Primordial',  'Noble gas',               '39.9485',       '39.9475',         '0.001784',   '83.81',    '87.302',   ],
        19 :  [ 'Potassium',      'K',   1,   4,   's',  'Solid',   'Primordial',  'Alkali metal',            '39.09825',      '39.09835',        '0.89',       '336.7',    '1032',     ],
        20 :  [ 'Calcium',        'Ca',  2,   4,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    '40.076',        '40.080',          '1.55',       '1115',     '1757',     ],

        21 :  [ 'Scandium',       'Sc',  3,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '44.9559055',    '44.9559105',      '2.985',      '1814',     '3109',     ],
        22 :  [ 'Titanium',       'Ti',  4,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '47.8665',       '47.8675',         '4.506',      '1941',     '2560',     ],
        23 :  [ 'Vanadium',       'V',   5,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '50.94145',      '50.94155',        '6.0',        '2183',     '2680',     ],
        24 :  [ 'Chromium',       'Cr',  6,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '51.9958',       '51.9964',         '7.15',       '2180',     '2755',     ],
        25 :  [ 'Manganese',      'Mn',  7,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '54.9380425',    '54.9380455',      '7.21',       '1519',     '2334',     ],
        26 :  [ 'Iron',           'Fe',  8,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '55.844',        '55.846',          '7.86',       '1811',     '3134',     ],
        27 :  [ 'Cobalt',         'Co',  9,   4,   'd',  'Solid',   'Primordial',  'Transition metal',        '58.933192',     '58.933196',       '8.90',       '1768',     '3200',     ],
        28 :  [ 'Nickel',         'Ni',  10,  4,   'd',  'Solid',   'Primordial',  'Transition metal',        '58.6932',       '58.6936',         '8.908',      '1728',     '2003',     ],
        29 :  [ 'Copper',         'Cu',  11,  4,   'd',  'Solid',   'Primordial',  'Transition metal',        '64.5445',       '64.5475',         '8.96',       '1357.77',  '2835',     ],
        30 :  [ 'Zinc',           'Zn',  12,  4,   'd',  'Solid',   'Primordial',  'Transition metal',        '65.37',         '65.39',           '7.14',       '692.68',   '1180',     ],

        31 :  [ 'Gallium',        'Ga',  13,  4,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '69.7225',       '69.7235',         '5.91',       '302.9146', '2673',     ],
        32 :  [ 'Germanium',      'Ge',  14,  4,   'p',  'Solid',   'Primordial',  'Metalloid',               '72.626',        '72.634',          '5.323',      '1211.40',  '3106',     ],
        33 :  [ 'Arsenic',        'As',  15,  4,   'p',  'Solid',   'Primordial',  'Metalloid',               '74.921592',     '74.921598',       '5.727',      '1090',     '887',      ],
        34 :  [ 'Selenium',       'Se',  16,  4,   'p',  'Solid',   'Primordial',  'Polyatomic nonmetal',     '78.967',        '78.975',          '4.81',       '494',      '958',      ],
        35 :  [ 'Bromine',        'Br',  17,  4,   'p',  'Liquid',  'Primordial',  'Diatomic nonmetal',       '79.901',        '79.907',          '3.1028',     '265.8',    '332',      ],
        36 :  [ 'Krypton',        'Kr',  18,  4,   'p',  'Gas',     'Primordial',  'Noble gas',               '83.797',        '83.799',          '0.003749',   '115.78',   '119.735',  ],
        37 :  [ 'Rubidium',       'Rb',  1,   5,   's',  'Solid',   'Primordial',  'Alkali metal',            '85.46765',      '85.46795',        '1.532',      '312.45',   '961',      ],
        38 :  [ 'Strontium',      'Sr',  2,   5,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    '87.615',        '87.625',          '2.64',       '1050',     '1650',     ],
        39 :  [ 'Yttrium',        'Y',   3,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        '88.90583',      '88.90585',        '4.472',      '1799',     '3203',     ],
        40 :  [ 'Zirconium',      'Zr',  4,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        '91.223',        '91.225',          '6.52',       '2128',     '4650',     ],

        41 :  [ 'Niobium',        'Nb',  5,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        '92.90636',      '92.90638',        '8.57',       '2750',     '5017',     ],
        42 :  [ 'Molybdenum',     'Mo',  6,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        '95.945',        '95.955',          '10.28',      '2896',     '4912',     ],
        43 :  [ 'Technetium',     'Tc',  7,   5,   'd',  'Solid',   'Transient',   'Transition metal',        '98',            '98',              '11.0',       '2430',     '4538',     ],
        44 :  [ 'Ruthenium',      'Ru',  8,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        '101.06',        '101.08',          '12.45',      '2607',     '4423',     ],
        45 :  [ 'Rhodium',        'Rh',  9,   5,   'd',  'Solid',   'Primordial',  'Transition metal',        '102.90549',     '102.90551',       '12.41',      '2237',     '3968',     ],
        46 :  [ 'Palladium',      'Pd',  10,  5,   'd',  'Solid',   'Primordial',  'Transition metal',        '106.415',       '106.425',         '12.023',     '1828.05',  '3236',     ],
        47 :  [ 'Silver',         'Ag',  11,  5,   'd',  'Solid',   'Primordial',  'Transition metal',        '107.8681',      '107.8683',        '10.49',      '1234.93',  '2483',     ],
        48 :  [ 'Cadmium',        'Cd',  12,  5,   'd',  'Solid',   'Primordial',  'Transition metal',        '112.412',       '112.416',         '8.65',       '594.22',   '1040',     ],
        49 :  [ 'Indium',         'In',  13,  5,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '114.8175',      '114.8185',        '7.31',       '429.75',   '2345',     ],
        50 :  [ 'Tin',            'Sn',  14,  5,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '118.7065',      '118.7135',        '7.265',      '505.8',    '2875',     ],

        51 :  [ 'Antimony',       'Sb',  15,  5,   'p',  'Solid',   'Primordial',  'Metalloid',               '121.7595',      '121.7605',        '6.697',      '903.78',   '1908',     ],
        52 :  [ 'Tellurium',      'Te',  16,  5,   'p',  'Solid',   'Primordial',  'Metalloid',               '127.585',       '127.615',         '6.24',       '722.66',   '1261',     ],
        53 :  [ 'Iodine',         'I',   17,  5,   'p',  'Solid',   'Primordial',  'Diatomic nonmetal',       '126.904455',    '126.904485',      '4.933',      '386.85',   '457.4',    ],
        54 :  [ 'Xenon',          'Xe',  18,  5,   'p',  'Gas',     'Primordial',  'Noble gas',               '131.290',       '131.296',         '0.005894',   '161.40',   '165.051',  ],
        55 :  [ 'Cesium',         'Cs',  1,   6,   's',  'Solid',   'Primordial',  'Alkali metal',            '132.90545193',  '132.90545199',    '1.93',       '301.7',    '944',      ],
        56 :  [ 'Barium',         'Ba',  2,   6,   's',  'Solid',   'Primordial',  'Alkaline earth metal',    '137.3235',      '137.3305',        '3.51',       '1000',     '1910',     ],
        57 :  [ 'Lanthanum',      'La',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '138.905435',    '138.905505',      '6.162',      '1193',     '3737',     ],
        58 :  [ 'Cerium',         'Ce',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '140.1155',      '140.1165',        '6.770',      '1068',     '3716',     ],
        59 :  [ 'Praseodymium',   'Pr',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '140.90765',     '140.90767',       '6.77',       '1208',     '3403',     ],
        60 :  [ 'Neodymium',      'Nd',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '144.2405',      '144.2435',        '7.01',       '1297',     '3347',     ],

        61 :  [ 'Promethium',     'Pm',  3,   6,   'f',  'Solid',   'Transient',   'Lanthanide',              '145',           '145',             '7.26',       '1315',     '3273',     ],
        62 :  [ 'Samarium',       'Sm',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '150.35',        '150.37',          '7.52',       '1345',     '2173',     ],
        63 :  [ 'Europium',       'Eu',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '151.9635',      '151.9645',        '5.244',      '1099',     '1802',     ],
        64 :  [ 'Gadolinium',     'Gd',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '157.235',       '157.265',         '7.90',       '1585',     '3273',     ],
        65 :  [ 'Terbium',        'Tb',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '158.92534',     '158.92536',       '8.23',       '1629',     '3396',     ],
        66 :  [ 'Dysprosium',     'Dy',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '162.4995',      '162.5005',        '8.540',      '1680',     '2840',     ],
        67 :  [ 'Holmium',        'Ho',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '164.93032',     '164.93034',       '8.79',       '1734',     '2873',     ],
        68 :  [ 'Erbium',         'Er',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '167.2575',      '167.2605',        '9.066',      '1802',     '3141',     ],
        69 :  [ 'Thulium',        'Tm',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '168.93421',     '168.93423',       '9.32',       '1818',     '2223',     ],
        70 :  [ 'Ytterbium',      'Yb',  3,   6,   'f',  'Solid',   'Primordial',  'Lanthanide',              '173.0515',      '173.0565',        '6.90',       '1097',     '1703',     ],

        71 :  [ 'Lutetium',       'Lu',  3,   6,   'd',  'Solid',   'Primordial',  'Lanthanide',              '174.96675',     '174.96685',       '9.841',      '1925',     '3675',     ],
        72 :  [ 'Hafnium',        'Hf',  4,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        '178.48',        '178.50',          '13.31',      '2506',     '4876',     ],
        73 :  [ 'Tantalum',       'Ta',  5,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        '180.94787',     '180.94789',       '16.69',      '3290',     '5731',     ],
        74 :  [ 'Tungsten',       'W',   6,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        '183.835',       '183.845',         '19.25',      '3695',     '6203',     ],
        75 :  [ 'Rhenium',        'Re',  7,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        '186.2065',      '186.2075',        '21.02',      '3459',     '5869',     ],
        76 :  [ 'Osmium',         'Os',  8,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        '190.215',       '190.245',         '22.59',      '3306',     '5285',     ],
        77 :  [ 'Iridium',        'Ir',  9,   6,   'd',  'Solid',   'Primordial',  'Transition metal',        '192.2155',      '192.2185',        '22.56',      '2719',     '4403',     ],
        78 :  [ 'Platinum',       'Pt',  10,  6,   'd',  'Solid',   'Primordial',  'Transition metal',        '195.0795',      '195.0885',        '21.45',      '2041.4',   '4098',     ],
        79 :  [ 'Gold',           'Au',  11,  6,   'd',  'Solid',   'Primordial',  'Transition metal',        '196.9665665',   '196.9665715',     '19.3',       '1337.33',  '3243',     ],
        80 :  [ 'Mercury',        'Hg',  12,  6,   'd',  'Liquid',  'Primordial',  'Transition metal',        '200.5905',      '200.5935',        '13.534',     '234.32',   '629.88',   ],

        81 :  [ 'Thallium',       'Tl',  13,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '204.382',       '204.385',         '11.85',      '577',      '1746',     ],
        82 :  [ 'Lead',           'Pb',  14,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '207.15',        '207.25',          '11.34',      '600.61',   '2022',     ],
        83 :  [ 'Bismuth',        'Bi',  15,  6,   'p',  'Solid',   'Primordial',  'Post-transition metal',   '208.980395',    '208.980405',      '9.78',       '544.7',    '1837',     ],
        84 :  [ 'Polonium',       'Po',  16,  6,   'p',  'Solid',   'Transient',   'Post-transition metal',   '209',           '209',             '9.398',      '527',      '1235',     ],
        85 :  [ 'Astatine',       'At',  17,  6,   'p',  'Solid',   'Transient',   'Metalloid',               '210',           '210',             '0',          '575',      '610',      ],
        86 :  [ 'Radon',          'Rn',  18,  6,   'p',  'Gas',     'Transient',   'Noble gas',               '222',           '222',             '0.00973',    '202',      '211.5',    ],
        87 :  [ 'Francium',       'Fr',  1,   7,   's',  'Solid',   'Transient',   'Alkali metal',            '223',           '223',             '1.87',       '300',      '950',      ],
        88 :  [ 'Radium',         'Ra',  2,   7,   's',  'Solid',   'Transient',   'Alkaline earth metal',    '226',           '226',             '5.5',        '973',      '2010',     ],
        89 :  [ 'Actinium',       'Ac',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                '227',           '227',             '10.0',       '1323',     '3471',     ],
        90 :  [ 'Thorium',        'Th',  3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                '232.0375',      '232.0379',        '11.7',       '2115',     '5061',     ],

        91 :  [ 'Protactinium',   'Pa',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                '231.03587',     '231.03589',       '15.37',      '1841',     '4300',     ],
        92 :  [ 'Uranium',        'U',   3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                '238.028895',    '238.028925',      '19.1',       '1405.3',   '4404',     ],
        93 :  [ 'Neptunium',      'Np',  3,   7,   'f',  'Solid',   'Transient',   'Actinide',                '237',           '237',             '20.2',       '917',      '4273',     ],
        94 :  [ 'Plutonium',      'Pu',  3,   7,   'f',  'Solid',   'Primordial',  'Actinide',                '244',           '244',             '19.816',     '912.5',    '3501',     ],
        95 :  [ 'Americium',      'Am',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                '243',           '243',             '12.0',       '1449',     '2880',     ],
        96 :  [ 'Curium',         'Cm',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                '247',           '247',             '13.51',      '1613',     '3383',     ],
        97 :  [ 'Berkelium',      'Bk',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                '247',           '247',             '14.78',      '1323',     'nan',      ],
        98 :  [ 'Californium',    'Cf',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                '251',           '251',             '15.1',       '1173',     'nan',      ],
        99 :  [ 'Einsteinium',    'Es',  3,   7,   'f',  'Solid',   'Synthetic',   'Actinide',                '252',           '252',             '8.84',       '1133',     'nan',      ],
        100 : [ 'Fermium',        'Fm',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                '257',           '257',             '0',          '1800',     'nan',      ],

        101 : [ 'Mendelevium',    'Md',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                '258',           '258',             'nan',        '1100',     'nan',      ],
        102 : [ 'Nobelium',       'No',  3,   7,   'f',  'unknown', 'Synthetic',   'Actinide',                '259',           '259',             'nan',        '1100',     'nan',      ],
        103 : [ 'Lawrencium',     'Lr',  3,   7,   'd',  'unknown', 'Synthetic',   'Actinide',                '262',           '262',             'nan',        '1900',     'nan',      ],
        104 : [ 'Rutherfordium',  'Rf',  4,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        '267',           '267',             'nan',        'nan',      'nan',      ],
        105 : [ 'Dubnium',        'Db',  5,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        '268',           '268',             'nan',        'nan',      'nan',      ],
        106 : [ 'Seaborgium',     'Sg',  6,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        '271',           '271',             'nan',        'nan',      'nan',      ],
        107 : [ 'Bohrium',        'Bh',  7,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        '272',           '272',             'nan',        'nan',      'nan',      ],
        108 : [ 'Hassium',        'Hs',  8,   7,   'd',  'unknown', 'Synthetic',   'Transition metal',        '270',           '270',             'nan',        'nan',      'nan',      ],
        109 : [ 'Meitnerium',     'Mt',  9,   7,   'd',  'unknown', 'Synthetic',   'unknown',                 '276',           '276',             'nan',        'nan',      'nan',      ],
        110 : [ 'Darmstadtium',   'Ds',  10,  7,   'd',  'unknown', 'Synthetic',   'unknown',                 '281',           '281',             'nan',        'nan',      'nan',      ],

        111 : [ 'Roentgenium',    'Rg',  11,  7,   'd',  'unknown', 'Synthetic',   'unknown',                 '280',           '280',             'nan',        'nan',      'nan',      ],
        112 : [ 'Copernicium',    'Cn',  12,  7,   'd',  'unknown', 'Synthetic',   'Transition metal',        '285',           '285',             'nan',        'nan',      'nan',      ],
        113 : [ 'Nihonium',       'Nh',  13,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 '284',           '284',             'nan',        'nan',      'nan',      ],
        114 : [ 'Flerovium',      'Fl',  14,  7,   'p',  'unknown', 'Synthetic',   'Post-transition metal',   '289',           '289',             'nan',        'nan',      'nan',      ],
        115 : [ 'Moscovium',      'Mc',  15,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 '288',           '288',             'nan',        'nan',      'nan',      ],
        116 : [ 'Livermorium',    'Lv',  16,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 '293',           '293',             'nan',        'nan',      'nan',      ],
        117 : [ 'Tennessine',     'Ts',  17,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 '294',           '294',             'nan',        'nan',      'nan',      ],
        118 : [ 'Oganesson',      'Og',  18,  7,   'p',  'unknown', 'Synthetic',   'unknown',                 '294',           '294',             'nan',        'nan',      'nan',      ],
    }

    g.atomic_numbers = { }

    for k, v in g.elements.items( ):
        g.atomic_numbers[ v[ 0 ] ] = k
        g.atomic_numbers[ v[ 1 ] ] = k


# //******************************************************************************
# //
# //  splitAtoms
# //
# //******************************************************************************

def splitAtoms( expression ):
    atom = ''

    for c in expression:
        if c in string.ascii_uppercase:
            if atom:
                yield atom

            atom = c
        else:
            atom += c

    yield atom


# //******************************************************************************
# //
# //  parseAtom
# //
# //******************************************************************************

def parseAtom( expression ):
    atom = expression[ 0 ]
    count = 1

    if expression[ 0 ] not in string.ascii_uppercase:
        raise ValueError( 'atom expression is invalid' )

    index = 1

    while index < len( expression ) and expression[ index ] in string.ascii_lowercase:
        atom += expression[ index ]
        index += 1

    if expression[ index : ]:
        count = int( expression[ index : ] )

    return atom, count


# //******************************************************************************
# //
# //  class RPNMolecule
# //
# //******************************************************************************

class RPNMolecule( collections.Counter ):
    '''This class represents a collection of atoms.'''
    def __init__( self, arg = '' ):
        if isinstance( arg, str ) and arg:
            self.update( self.parseMoleculeString( arg ) )
        elif isinstance( arg, RPNMolecule ):
            self.update( arg )

    @staticmethod
    def parseMoleculeString( expression ):
        result = RPNMolecule( )

        if expression.count( '(' ) != expression.count( ')' ):
            raise ValueError( 'molecule expression \'' + expression + '\' has mismatched parentheses' )

        atoms = splitAtoms( expression )

        for atom in atoms:
            element, count = parseAtom( atom )
            result[ element ] += count

        return result


# //******************************************************************************
# //
# //  getElementAttribute
# //
# //******************************************************************************

def getElementAttribute( n, k ):
    if isinstance( n, RPNMeasurement ):
        n = convertMeasurementToAtomicSymbol( n )

    if isinstance( n, str ):
        n = getAtomicNumber( n )

    if int( n ) < 1 or n > 118:
        raise ValueError( 'invalid atomic number' )

    if ( 0 > k > 7 ):
        raise ValueError( 'invalid element attribute' )

    if g.elements is None:
        loadChemistryTables( )

    return g.elements[ int( n ) ][ k ]


# //******************************************************************************
# //
# //  convertMeasurementToAtomicSymbol
# //
# //******************************************************************************

def convertMeasurementToAtomicSymbol( n ):
    # If there is a value other than the default 1, then let's just bail, because
    # something more complicated is going on.
    if n.getValue( ) != 1:
        return n

    if n.getUnits( ) == RPNMeasurement( 1, 'henry' ).getUnits( ):
        return 'H'

    if n.getUnits( ) == RPNMeasurement( 1, 'henry' ).getUnits( ):
        return 'H'

    if n.getUnits( ) == RPNMeasurement( 1, 'byte' ).getUnits( ):
        return 'B'

    if n.getUnits( ) == RPNMeasurement( 1, 'coulomb' ).getUnits( ):
        return 'C'

    if n.getUnits( ) == RPNMeasurement( 1, 'newton' ).getUnits( ):
        return 'N'

    if n.getUnits( ) == RPNMeasurement( 1, 'ohm' ).getUnits( ):
        return 'O'

    if n.getUnits( ) == RPNMeasurement( 1, 'farad' ).getUnits( ):
        return 'F'

    if n.getUnits( ) == RPNMeasurement( 1, 'megagram' ).getUnits( ):
        return 'Mg'

    if n.getUnits( ) == RPNMeasurement( 1, 'siemens' ).getUnits( ):
        return 'S'

    if n.getUnits( ) == RPNMeasurement( 1, 'kelvin' ).getUnits( ):
        return 'K'

    if n.getUnits( ) == RPNMeasurement( 1, 'volt' ).getUnits( ):
        return 'V'

    if n.getUnits( ) == RPNMeasurement( 1, 'gigare' ).getUnits( ):
        return 'Ga'

    if n.getUnits( ) == RPNMeasurement( 1, 'ampere-second' ).getUnits( ):
        return 'As'

    if n.getUnits( ) == RPNMeasurement( 1, 'barye' ).getUnits( ):
        return 'Ba'

    if n.getUnits( ) == RPNMeasurement( 1, 'petameter' ).getUnits( ):
        return 'Pm'

    if n.getUnits( ) == RPNMeasurement( 1, 'terabit' ).getUnits( ):
        return 'Tb'

    if n.getUnits( ) == RPNMeasurement( 1, 'terameter' ).getUnits( ):
        return 'Tm'

    if n.getUnits( ) == RPNMeasurement( 1, 'yottabit' ).getUnits( ):
        return 'Yb'

    if n.getUnits( ) == RPNMeasurement( 1, 'terare' ).getUnits( ):
        return 'Te'

    if n.getUnits( ) == RPNMeasurement( 1, 'watt' ).getUnits( ):
        return 'W'

    if n.getUnits( ) == RPNMeasurement( 1, 'reaumur' ).getUnits( ):
        return 'Re'

    if n.getUnits( ) == RPNMeasurement( 1, 'petabit' ).getUnits( ):
        return 'Pb'

    if n.getUnits( ) == RPNMeasurement( 1, 'franklin' ).getUnits( ):
        return 'Fr'

    if n.getUnits( ) == RPNMeasurement( 1, 'petare' ).getUnits( ):
        return 'Pa'

    if n.getUnits( ) == RPNMeasurement( 1, 'ampere-minute' ).getUnits( ):
        return 'Am'

    if n.getUnits( ) == RPNMeasurement( 1, 'exasecond' ).getUnits( ):
        return 'Es'

    if n.getUnits( ) == RPNMeasurement( 1, 'terasecond' ).getUnits( ):
        return 'Ts'

    # No matches?  Then let an exception be thrown.
    return n


# //******************************************************************************
# //
# //  getAtomicNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getAtomicNumber( n ):
    if g.elements is None:
        loadChemistryTables( )

    if isinstance( n, RPNMeasurement ):
        n = convertMeasurementToAtomicSymbol( n )

    if n not in g.atomic_numbers:
        raise ValueError( 'invalid atomic symbol' )

    return g.atomic_numbers[ n ]


# //******************************************************************************
# //
# //  getAtomicWeight
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getAtomicWeight( n ):
    if isinstance( n, RPNMeasurement ):
        n = convertMeasurementToAtomicSymbol( n )

    return fdiv( fadd( mpmathify( getElementAttribute( n, 9 ) ),
                       mpmathify( getElementAttribute( n, 8 ) ) ), 2 )


# //******************************************************************************
# //
# //  getElementDensity
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getElementDensity( n ):
    return RPNMeasurement( mpmathify( getElementAttribute( n, 10 ) ), 'g/cm^3' )


# //******************************************************************************
# //
# //  getElementMeltingPoint
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getElementMeltingPoint( n ):
    return RPNMeasurement( mpmathify( getElementAttribute( n, 11 ) ), 'kelvin' )


# //******************************************************************************
# //
# //  getElementBoilingPoint
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getElementBoilingPoint( n ):
    return RPNMeasurement( mpmathify( getElementAttribute( n, 12 ) ), 'kelvin' )


# //******************************************************************************
# //
# //  calculateMolarMass
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateMolarMass( n ):
    result = 0

    for atom in n:
        result = fadd( result, fmul( getAtomicWeight( atom ), n[ atom ] ) )

    return RPNMeasurement( result, 'gram' )


@oneArgFunctionEvaluator( )
def getAtomicSymbol( n ):
    return getElementAttribute( n, 1 )

@oneArgFunctionEvaluator( )
def getElementBlock( n ):
    return getElementAttribute( n, 4 )

@oneArgFunctionEvaluator( )
def getElementDescription( n ):
    return getElementAttribute( n, 7 )

@oneArgFunctionEvaluator( )
def getElementGroup( n ):
    return getElementAttribute( n, 2 )

@oneArgFunctionEvaluator( )
def getElementName( n ):
    return getElementAttribute( n, 0 )

@oneArgFunctionEvaluator( )
def getElementOccurrence( n ):
    return getElementAttribute( n, 6 )

@oneArgFunctionEvaluator( )
def getElementPeriod( n ):
    return getElementAttribute( n, 3 )

@oneArgFunctionEvaluator( )
def getElementState( n ):
    return getElementAttribute( n, 5 )

@oneArgFunctionEvaluator( )
def getMolarMass( n ):
    if isinstance( n, RPNMeasurement ):
        n = convertMeasurementToAtomicSymbol( n )

    return calculateMolarMass( RPNMolecule( n ) )

