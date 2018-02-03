#!/usr/bin/env python

# //******************************************************************************
# //
# //  testHelp
# //
# //  test script for RPN help
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
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
    testOperator( 'help about' )
    testOperator( 'help arguments' )
    testOperator( 'help bugs' )
    testOperator( 'help examples' )
    testOperator( 'help input' )
    testOperator( 'help interactive_mode' )
    testOperator( 'help license' )
    testOperator( 'help metric' )
    testOperator( 'help notes' )
    testOperator( 'help options' )
    testOperator( 'help output' )
    testOperator( 'help release_notes' )
    testOperator( 'help release_notes_5' )
    testOperator( 'help time_features' )
    testOperator( 'help unit_conversion' )
    testOperator( 'help unit_types' )
    testOperator( 'help user_functions' )

    testOperator( 'help algebra' )
    testOperator( 'help arithmetic' )
    testOperator( 'help astronomy' )
    testOperator( 'help bitwise' )
    testOperator( 'help calendars' )
    testOperator( 'help combinatorics' )
    testOperator( 'help complex_math' )
    testOperator( 'help constants' )
    testOperator( 'help conversion' )
    testOperator( 'help date_time' )
    testOperator( 'help function' )
    testOperator( 'help geometry' )
    testOperator( 'help geography' )
    testOperator( 'help internal' )
    testOperator( 'help lexicographic' )
    testOperator( 'help list_operators' )
    testOperator( 'help logarithms' )
    testOperator( 'help modifiers' )
    testOperator( 'help number_theory' )
    testOperator( 'help polygonal_numbers' )
    testOperator( 'help polyhedral_numbers' )
    testOperator( 'help powers_and_roots' )
    testOperator( 'help prime_numbers' )
    testOperator( 'help settings' )
    testOperator( 'help special' )
    testOperator( 'help trigonometry' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runHelpTests( )

