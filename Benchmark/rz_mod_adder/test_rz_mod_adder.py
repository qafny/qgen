import pytest
from antlr4 import InputStream, CommonTokenStream

from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from Source.quantumCode.AST_Scripts.simulator import to_binary_arr, CoqNVal, Simulator, bit_array_to_int


def simulate_rz_mod_adder(val_array_x, addend, modulo, num_qubits, val_array_carry=0):
    with open("Benchmark/rz_mod_adder/rz_mod_adder_good.xml", 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    tree = parser.root()
    #print(tree.toStringTree(recog=parser))

    x_array = to_binary_arr(val_array_x, num_qubits)
    carry_array = to_binary_arr(val_array_carry, 1)
    state = dict(
        {"x": [CoqNVal(x_array, 0)],
         "c": [CoqNVal(carry_array, 0)],
         "na": num_qubits,
         "a": addend,
         "m": modulo,
         })
    environment = dict(
        {"x": num_qubits,
         "c": 1,
         })
    simulator = Simulator(state, environment)
    simulator.visitRoot(tree)
    new_state = simulator.state
    return new_state


def test_in_range_addition():
    test_cases = [
        {"num_qubits": 16, "val_x": 22, "val_a": 971, "modulo": 1024, "expected_result": (22 + 971) % 1024, "description": "Small Even, Large Odd"},
        {"num_qubits": 16, "val_x": 150, "val_a": 25, "modulo": 256, "expected_result": (150 + 25) % 256, "description": "Medium Even, Small Odd"},
        {"num_qubits": 16, "val_x": 999, "val_a": 1025, "modulo": 2048, "expected_result": (999 + 1025) % 2048, "description": "Large Odd, Medium Odd"},
        {"num_qubits": 16, "val_x": 0, "val_a": 1, "modulo": 16, "expected_result": (0 + 1) % 16, "description": "Small Even, Small Odd"},
        {"num_qubits": 32, "val_x": 500000, "val_a": 1000000, "modulo": 1048576, "expected_result": (500000 + 1000000) % 1048576, "description": "Medium Even, Large Odd"}
    ]

    for case in test_cases:
        assert case["val_x"] < 2**(case["num_qubits"] - 1), f"val_x exceeds limit for {case['description']}"
        assert case["val_a"] < 2**(case["num_qubits"] - 1), f"val_a exceeds limit for {case['description']}"
        new_state = simulate_rz_mod_adder(case["val_x"], case["val_a"], case["modulo"], case["num_qubits"])
        assert case["expected_result"] == bit_array_to_int(new_state.get('x')[0].getBits(), case["num_qubits"]), f"Test failed for case: {case['description']}. Expected {case['expected_result']}, got {bit_array_to_int(new_state.get('x')[0].getBits(), case['num_qubits'])}"


def test_large_numbers_addition():
    test_cases = [
        {"num_qubits": 24, "val_x": 1000000, "val_a": 1000000, "modulo": 16777216, "expected_result": (1000000 + 1000000) % 16777216, "description": "Large numbers with large modulo"},
        {"num_qubits": 48, "val_x": 200000000000, "val_a": 300000000000, "modulo": 281474976710656, "expected_result": (200000000000 + 300000000000) % 281474976710656, "description": "Very large numbers with large modulo"},
        {"num_qubits": 64, "val_x": 2**63 - 1, "val_a": 1, "modulo": 2**64, "expected_result": (2**63 - 1 + 1) % 2**64, "description": "Edge case with max 64-bit integer"},
        {"num_qubits": 24, "val_x": 500000, "val_a": 2000000, "modulo": 8388608, "expected_result": (500000 + 2000000) % 8388608, "description": "Large number addition with 24-bit modulo"},
        {"num_qubits": 32, "val_x": 12345678, "val_a": 98765432, "modulo": 494967295, "expected_result": (12345678 + 98765432) % 494967295, "description": "Arbitrary large numbers with 32-bit modulo"}
    ]

    for case in test_cases:
        assert case["val_x"] < 2**(case["num_qubits"] - 1), f"val_x exceeds limit for {case['description']}"
        assert case["val_a"] < 2**(case["num_qubits"] - 1), f"val_a exceeds limit for {case['description']}"
        new_state = simulate_rz_mod_adder(case["val_x"], case["val_a"], case["modulo"], case["num_qubits"])
        assert case["expected_result"] == bit_array_to_int(new_state.get('x')[0].getBits(), case["num_qubits"]), f"Test failed for case: {case['description']}. Expected {case['expected_result']}, got {bit_array_to_int(new_state.get('x')[0].getBits(), case['num_qubits'])}"


def test_zero_addition():
    test_cases = [
        {"num_qubits": 16, "val_x": 1234, "val_a": 0, "modulo": 27160, "expected_result": 1234 % 27160, "description": "Adding zero"}
    ]

    for case in test_cases:
        assert case["val_x"] < 2**(case["num_qubits"] - 1), f"val_x exceeds limit for {case['description']}"
        new_state = simulate_rz_mod_adder(case["val_x"], case["val_a"], case["modulo"], case["num_qubits"])
        assert case["expected_result"] == bit_array_to_int(new_state.get('x')[0].getBits(), case["num_qubits"]), f"Test failed for case: {case['description']}. Expected {case['expected_result']}, got {bit_array_to_int(new_state.get('x')[0].getBits(), case['num_qubits'])}"


def test_overflow_addition():
    test_cases = [
        {"num_qubits": 16, "val_x": 2**15 - 2, "val_a": 1, "modulo": 2**15-1, "expected_result": (2**15 - 2 + 1) % (2**15-1), "description": "Overflow case 1"},
        {"num_qubits": 32, "val_x": 2**31 - 2, "val_a": 1, "modulo": 2**31-1, "expected_result": (2**31 - 2 + 1) % (2**31-1), "description": "Overflow case 2"}
    ]

    for case in test_cases:
        assert case["val_x"] < 2**(case["num_qubits"] - 1), f"val_x exceeds limit for {case['description']}"
        assert case["val_a"] < 2**(case["num_qubits"] - 1), f"val_a exceeds limit for {case['description']}"
        new_state = simulate_rz_mod_adder(case["val_x"], case["val_a"], case["modulo"], case["num_qubits"])
        assert case["expected_result"] == bit_array_to_int(new_state.get('x')[0].getBits(), case["num_qubits"]), f"Test failed for case: {case['description']}. Expected {case['expected_result']}, got {bit_array_to_int(new_state.get('x')[0].getBits(), case['num_qubits'])}"
