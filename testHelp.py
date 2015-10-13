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
    testRPN( 'help about' )
    testRPN( 'help arguments' )
    testRPN( 'help bugs' )
    testRPN( 'help examples' )
    testRPN( 'help input' )
    testRPN( 'help interactive_mode' )
    testRPN( 'help license' )
    testRPN( 'help metric' )
    testRPN( 'help notes' )
    testRPN( 'help options' )
    testRPN( 'help output' )
    testRPN( 'help release_notes' )
    testRPN( 'help release_notes_5' )
    testRPN( 'help time_features' )
    testRPN( 'help unit_conversion' )
    testRPN( 'help unit_types' )
    testRPN( 'help user_functions' )

    testRPN( 'help algebra' )
    testRPN( 'help arithmetic' )
    testRPN( 'help astronomy' )
    testRPN( 'help bitwise' )
    testRPN( 'help calendar' )
    testRPN( 'help combinatorics' )
    testRPN( 'help complex_math' )
    testRPN( 'help constants' )
    testRPN( 'help conversion' )
    testRPN( 'help datetime' )
    testRPN( 'help function' )
    testRPN( 'help geometry' )
    testRPN( 'help internal' )
    testRPN( 'help lexicographic' )
    testRPN( 'help list_operators' )
    testRPN( 'help logarithms' )
    testRPN( 'help modifiers' )
    testRPN( 'help number_theory' )
    testRPN( 'help polygonal_numbers' )
    testRPN( 'help polyhedral_numbers' )
    testRPN( 'help powers_and_roots' )
    testRPN( 'help prime_numbers' )
    testRPN( 'help settings' )
    testRPN( 'help special' )
    testRPN( 'help trigonometry' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runHelpTests( )

