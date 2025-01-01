import pytest

#from collections import ChainMap
#from simulator import *
from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from antlr4 import *
#from Source.quantumCode.AST_Scripts.SpecExpParser import *
#from Source.quantumCode.AST_Scripts.SpecExpVisitor import *
#from Source.quantumCode.AST_ScriptsSpecGen import *
#from VarCollector import *
from Source.quantumCode.AST_Scripts.ProgramTransformer import *
from Source.quantumCode.AST_Scripts.XMLPrinter import *

####################
## What is input ###

# st : state
# Both inital program and initial values


# env : environment
# How many qubits are in the array


#######################
## What is expected out

# st : state
# assert that get_state() is equal to the state we expect via oracle


# Write a series of tests HERE
class Test_Simulator(object):
 #   @pytest.fixture
  #  def test_result(self, spec: SpecExpParser.ProgramContext, st: dict):
   #     specVisitor = SpecGen(st)
    #    return specVisitor.visitProgram(spec).getResult()

  #  @pytest.fixture
   # def test_pattern(self, spec: SpecExpParser.ProgramContext):
    #    varVisitor = VarCollector()
     #   st = varVisitor.visitProgram(spec)
        # need to use random testing generator to generate values in st
      #  return self.test_result(spec, st)

    #test_pattern above is rewritten for the usage of pytest.
    #pytest will call test_pattern to test a spec
    #it can also call test_result by inputing a state, and then get
    #the resulting state and check
    # the result state is a list of nat numbers
    #user are responsible to turn the nat numbers to Nvals, then check if
    #the quantum component satisfies with the output
    def test_init(self):
        # //We first turn x array to QFT type, and we apply SR gate to rotate the phase of x for 2 pi i * (1/2^10). It will make sense if 10 < rmax, RQFT is the inverse of QFT.
        str = "<pexp gate = 'QFT' id = 'x' > <vexp op = 'num' > 0 </vexp> </pexp> <app id = 'f' > <vexp op = 'id' type = 'Nat' > na </vexp> <vexp op = 'id' type = 'Nat' > size </vexp> <vexp op = '-' > <vexp op = 'id' > size </vexp> <vexp op = 'id' > m </vexp> </vexp> <vexp op = 'id' type = 'Phi(size, size)' > x </vexp> </app> <pexp gate = 'RQFT' id = 'x' > </pexp> </root>"
        i_stream = InputStream(str)
        print("abc")
        lexer = XMLExpLexer(i_stream)
        t_stream = CommonTokenStream(lexer)
        parser = XMLExpParser(t_stream)
        tree = parser.program()
        aaa = ProgramTransformer()
        printer = XMLPrinter()
        st = printer.visitProgram(tree)
        newTree = aaa.visitProgram(tree)
        print(tree.toStringTree(recog=parser))

        # the following shows an example of using 1 variable state. You can have a 10 variable state
        # see that a variable is a string.
        #num = 16 # Number of Qubits
        #val = 100 #init value
        #valArray = to_binary_arr(val, num) #conver value to array
        #val = [False]*num # state for x
        #state = dict({"x" : CoqNVal(valArray, 0)}) #initial a chainMap having variable "x" to be 0 (list of False)
        #environment = dict({"x" : num}) #env has the same variables as state, but here, variable is initiliazed to its qubit num
        #y = Simulator(state, environment) # Environment is same, initial state varies by pyTest
        #y.visitProgram(tree)
        #newState = y.get_state()
        #assert(132 == bit_array_to_int(newState.get('x').getBits(), num))

        # Do assertion check that state is as expected
        # Add function to do state (binary-> int ) conversion  #TODO#
        # int n = calInt(arrayQuBits, sizeArray)
        #assert newState == state

def test_trivial():
    Test_Simulator()
    assert True

str = "<root> <pexp gate = 'QFT' id = 'x' > <vexp op = 'num' > 0 </vexp> </pexp> <app id = 'f' > <vexp op = '-' > <vexp op = 'id' > size </vexp> <vexp op = 'id' > m </vexp> </vexp> <vexp op = 'id' type = 'Nat' > size </vexp> <vexp op = 'id' type = 'Nat' > m </vexp> <vexp op = 'id' type = 'Phi(size, size)' > x </vexp> </app> <pexp gate = 'RQFT' id = 'x' > </pexp> </root>"
i_stream = InputStream(str)
lexer = XMLExpLexer(i_stream)
t_stream = CommonTokenStream(lexer)
parser = XMLExpParser(t_stream)
tree = parser.root()
aaa = ProgramTransformer()
#printer = XMLPrinter()
#st = printer.visitProgram(tree)
newTree = aaa.visitRoot(tree)
print(newTree)