#!/usr/bin/env python

# //******************************************************************************
# //
# //  testHelp
# //
# //  test script for RPN help
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn.rpnTestUtils import testOperator


# //******************************************************************************
# //
# //  runHelpTests
# //
# //******************************************************************************

def runHelpTests( ):
    testOperator( 'help about', False )
    testOperator( 'help arguments', False )
    testOperator( 'help bugs', False )
    testOperator( 'help examples', False )
    testOperator( 'help input', False )
    testOperator( 'help interactive_mode', False )
    testOperator( 'help license', False )
    testOperator( 'help metric', False )
    testOperator( 'help notes', False )
    testOperator( 'help options', False )
    testOperator( 'help output', False )
    testOperator( 'help release_notes', False )
    testOperator( 'help release_notes_5', False )
    testOperator( 'help time_features', False )
    testOperator( 'help unit_conversion', False )
    testOperator( 'help unit_types', False )
    testOperator( 'help user_functions', False )

    testOperator( 'help algebra', False )
    testOperator( 'help arithmetic', False )
    testOperator( 'help astronomy', False )
    testOperator( 'help bitwise', False )
    testOperator( 'help calendars', False )
    testOperator( 'help combinatorics', False )
    testOperator( 'help complex_math', False )
    testOperator( 'help constants', False )
    testOperator( 'help conversion', False )
    testOperator( 'help date_time', False )
    testOperator( 'help function', False )
    testOperator( 'help geometry', False )
    testOperator( 'help geography', False )
    testOperator( 'help internal', False )
    testOperator( 'help lexicographic', False )
    testOperator( 'help list_operators', False )
    testOperator( 'help logarithms', False )
    testOperator( 'help modifiers', False )
    testOperator( 'help number_theory', False )
    testOperator( 'help polygonal_numbers', False )
    testOperator( 'help polyhedral_numbers', False )
    testOperator( 'help powers_and_roots', False )
    testOperator( 'help prime_numbers', False )
    testOperator( 'help settings', False )
    testOperator( 'help special', False )
    testOperator( 'help trigonometry', False )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runHelpTests( )

