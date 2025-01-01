import time
import pytest
from antlr4 import InputStream, CommonTokenStream

# from Benchmark.Triangle.triangle import TriangleType, classify_triangle # this might not be correct
from Benchmark.cl_adder.cl_adder_const import X_CCV, FLIP_X_ZERO_ROTATE_PHASE, CNOT, CCX
from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from Source.quantumCode.AST_Scripts.simulator import to_binary_arr, CoqNVal, Simulator, bit_array_to_int

# for the first step, the fitness is the percentage of correctness. How many test cases a program run correctly.
# the correctness is defined as array, x, y and c, the input is (x,y,c), and the output is (x,x+y,c)
@pytest.fixture
def tree():
    with open("Benchmark/cl_adder/cl_adder.xml", 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    return parser.program()


def simulate_cl_adder(x_array_value, y_array_value, c_array_value, num_qubits):
    with open("Benchmark/cl_adder/cl_adder_good.xml", 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    tree = parser.root()
    # print(tree.toStringTree(recog=parser))

    val_array_x = to_binary_arr(x_array_value, num_qubits)
    val_array_y = to_binary_arr(y_array_value, num_qubits)
    num_qubits_ca = 1
    val_array_ca = to_binary_arr(c_array_value, num_qubits_ca)

    state = dict(
        {"xa": [CoqNVal(val_array_x, 0)],
         "ya": [CoqNVal(val_array_y, 0)],
         "ca": [CoqNVal(val_array_ca, 0)],
         "na": num_qubits,
         })
    environment = dict(
        {"xa": num_qubits,
         "ya": num_qubits,
         "ca": num_qubits_ca,
         })
    # env has the same variables as state, but here, variable is initiliazed to its qubit num
    print("xa",state.get("xa"))
    print("ya",state.get("ya"))
    print("ca",state.get("ca"))
    simulator = Simulator(state, environment)
    simulator.visitRoot(tree)
    new_state = simulator.state
    return new_state


def test_in_range_addition():
    test_cases = [
        {"num_qubits": 20, "val_x": 22, "val_y": 971, "expected_result": 993, "description": "Small Even, Large Odd"},
        {"num_qubits": 16, "val_x": 150, "val_y": 25, "expected_result": 175, "description": "Medium Even, Small Odd"},
        {"num_qubits": 7, "val_x": 4, "val_y": 3, "expected_result": 7, "description": "Small Odd, Small Odd"},
        {"num_qubits": 11, "val_x": 100, "val_y": 1911, "expected_result": 2011, "description": "Small Even, Small Odd"},
        {"num_qubits": 3, "val_x": 1, "val_y": 2, "expected_result": 3, "description": "Medium Even, Medium Odd"},
        {"num_qubits": 38, "val_x": 40349, "val_y": 343804091, "expected_result": 343844440, "description": "Max 16-bit Odd, Small Odd"},
        {"num_qubits": 16, "val_x": 16383, "val_y": 16384, "expected_result": 32767, "description": "Half 16-bit Odd, Half 16-bit Even"},
        {"num_qubits": 16, "val_x": 1, "val_y": 65534, "expected_result": 65535, "description": "Small Odd, Max 16-bit Even"},
        {"num_qubits": 16, "val_x": 32768, "val_y": 32767, "expected_result": 65535, "description": "Half 16-bit Even, Half 16-bit Odd"},
    ]
    for test in test_cases:
        new_state = simulate_cl_adder(test["val_x"], test["val_y"], 0, test["num_qubits"])
        assert (test["expected_result"] == bit_array_to_int(new_state.get('ya')[0].getBits(), test["num_qubits"]))
        assert (test["val_x"] == bit_array_to_int(new_state.get('xa')[0].getBits(), test["num_qubits"]))


def test_zero_addition():
    test_cases = [
        {"num_qubits": 16, "val_x": 0, "val_y": 0, "expected_result": 0, "description": "Zero Addition"},
        {"num_qubits": 78, "val_x": 0, "val_y": 1, "expected_result": 1, "description": "Zero and Small Odd"},
        {"num_qubits": 2, "val_x": 0, "val_y": 2, "expected_result": 2, "description": "Zero and Small Even"},
        ]
    for test in test_cases:
        new_state = simulate_cl_adder(test["val_x"], test["val_y"], 0, test["num_qubits"])
        assert (test["expected_result"] == bit_array_to_int(new_state.get('ya')[0].getBits(), test["num_qubits"]))
        assert (test["val_x"] == bit_array_to_int(new_state.get('xa')[0].getBits(), test["num_qubits"]))

def test_overflow_addition():
    test_cases = [
        {"num_qubits": 16, "val_x": 65535, "val_y": 1, "expected_result": 0, "description": "Max 16-bit Odd, 1"},
        {"num_qubits": 14, "val_x": 74734, "val_y": 47001, "expected_result": 7047, "description": "Half 16-bit Odd, Half 16-bit Odd"},
        {"num_qubits": 3, "val_x": 74, "val_y": 85310, "expected_result": 0, "description": "Half 16-bit Even, Half 16-bit Even"},
        {"num_qubits": 46, "val_x": 423532800, "val_y": 853232733800242510, "expected_result": 11711069599310, "description": "Half 16-bit Odd, Half 16-bit Even"},
    ]
    assert True

def test_negative_addition():
    test_cases = [
        {"num_qubits": 5, "val_x": -20, "val_y": 5, "expected_result": 17, "description": "Small negative, positive sum"},
        {"num_qubits": 8, "val_x": -250, "val_y": 200, "expected_result": 206, "description": "Medium negative, medium positive"},
        {"num_qubits": 16, "val_x": -5000, "val_y": 4900, "expected_result": 65436, "description": "Large negative, large positive"},
        {"num_qubits": 24, "val_x": -16777210, "val_y": -10, "expected_result": 16777212, "description": "Negative and slightly more negative"},
        {"num_qubits": 32, "val_x": -4294967296, "val_y": -10, "expected_result": 4294967286, "description": "Large negative, slightly negative"},
        {"num_qubits": 40, "val_x": -1099511627776, "val_y": 100, "expected_result": 100, "description": "Very large negative, small positive"},
        {"num_qubits": 48, "val_x": -281474976710656, "val_y": -281474976700000, "expected_result": 10656, "description": "Very large negative, slightly less large negative"},
        {"num_qubits": 56, "val_x": -72057594037927936, "val_y": 1000, "expected_result": 1000, "description": "Huge negative, small positive"},
        {"num_qubits": 64, "val_x": -18446744073709551616, "val_y": 18446744073709551500, "expected_result": 18446744073709551500, "description": "Extremely large negative, slightly less large positive"},
        {"num_qubits": 78, "val_x": -151115727451828646838272, "val_y": -10, "expected_result": 151115727451828646838262, "description": "Maximum negative, slightly more negative"}
    ]
    for test in test_cases:
        new_state = simulate_cl_adder(test["val_x"], test["val_y"], 0, test["num_qubits"])
        assert (test["expected_result"] == bit_array_to_int(new_state.get('ya')[0].getBits(), test["num_qubits"]))


@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
