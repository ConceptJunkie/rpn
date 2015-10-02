# //******************************************************************************
# //
# //  testRPN
# //
# //  main test script for RPN
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn import rpn



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
# //  runHelpTests
# //
# //******************************************************************************

def runHelpTests( ):
    testRPN( 'rpn help about' )
    testRPN( 'rpn help arguments' )
    testRPN( 'rpn help bugs' )
    testRPN( 'rpn help examples' )
    testRPN( 'rpn help input' )
    testRPN( 'rpn help interactive_mode' )
    testRPN( 'rpn help license' )
    testRPN( 'rpn help metric' )
    testRPN( 'rpn help notes' )
    testRPN( 'rpn help options' )
    testRPN( 'rpn help output' )
    testRPN( 'rpn help release_notes' )
    testRPN( 'rpn help release_notes_5' )
    testRPN( 'rpn help time_features' )
    testRPN( 'rpn help unit_conversion' )
    testRPN( 'rpn help unit_types' )
    testRPN( 'rpn help user_functions' )

    testRPN( 'rpn help algebra' )
    testRPN( 'rpn help arithmetic' )
    testRPN( 'rpn help astronomy' )
    testRPN( 'rpn help bitwise' )
    testRPN( 'rpn help calendar' )
    testRPN( 'rpn help combinatorics' )
    testRPN( 'rpn help complex_math' )
    testRPN( 'rpn help constants' )
    testRPN( 'rpn help conversion' )
    testRPN( 'rpn help date-time' )
    testRPN( 'rpn help function' )
    testRPN( 'rpn help geometry' )
    testRPN( 'rpn help internal' )
    testRPN( 'rpn help lexicographic' )
    testRPN( 'rpn help list_operators' )
    testRPN( 'rpn help logarithms' )
    testRPN( 'rpn help modifiers' )
    testRPN( 'rpn help number_theory' )
    testRPN( 'rpn help polygonal_numbers' )
    testRPN( 'rpn help polyhedral_numbers' )
    testRPN( 'rpn help powers_and_roots' )
    testRPN( 'rpn help prime_numbers' )
    testRPN( 'rpn help settings' )
    testRPN( 'rpn help special' )
    testRPN( 'rpn help trigonometry' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runHelpTests( )

