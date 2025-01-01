import time
import pytest
from antlr4 import InputStream, CommonTokenStream

from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from Source.quantumCode.AST_Scripts.simulator import to_binary_arr, CoqNVal, Simulator, bit_array_to_int


def simulate_ghz(qubit_array, num_qubits):
    with open("Benchmark/ghz/ghz_good.xml", 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    tree = parser.program()

    state = dict(
        {"x": [CoqNVal(qubit_array, 0)],
         "n": num_qubits,
         })
    environment = dict(
        {"x": num_qubits,
         })
    simulator = Simulator(state, environment)
    simulator.visitProgram(tree)
    new_state = simulator.get_state()
    return new_state


def test_ghz_state_generation():
    test_cases = [
        {"num_qubits": 5, "initial_values": [0, 1, 0, 1, 0], "expected_result": [0, 1, 1, 0, 0], "description": "Alternating initial values"},
        {"num_qubits": 6, "initial_values": [1, 1, 1, 1, 1, 1], "expected_result": [1, 0, 0, 0, 0, 0], "description": "All ones"},
        {"num_qubits": 4, "initial_values": [0, 0, 0, 0], "expected_result": [0, 0, 0, 0], "description": "All zeros"},
        {"num_qubits": 8, "initial_values": [1, 0, 1, 0, 1, 0, 1, 0], "expected_result": [1, 1, 0, 0, 1, 1, 0, 0], "description": "Alternating pattern"},
        {"num_qubits": 3, "initial_values": [1, 1, 0], "expected_result": [1, 0, 0], "description": "Small number of qubits"},
        {"num_qubits": 7, "initial_values": [1, 1, 1, 0, 0, 0, 1], "expected_result": [1, 0, 0, 1, 1, 1, 0], "description": "Mixed values"},
        {"num_qubits": 9, "initial_values": [0, 1, 0, 1, 1, 0, 1, 0, 1], "expected_result": [0, 1, 1, 0, 1, 1, 0, 1, 0], "description": "Complex alternating pattern"},
        {"num_qubits": 1, "initial_values": [1], "expected_result": [1], "description": "Single qubit"},
        {"num_qubits": 2, "initial_values": [1, 0], "expected_result": [1, 1], "description": "Two qubits"},
]

    for case in test_cases:
        new_state = simulate_ghz(case["initial_values"], case["num_qubits"])
        print(new_state)
        assert (case["expected_result"] == new_state.get('x')[0].getBits(), ), f"Test failed for case: {case['description']}. Expected {case['expected_result']}, got {new_state.get('x')}"


def test_large_ghz_state_generation():
    test_cases = [
        {"num_qubits": 50, "initial_values": [0, 1] * 25, "expected_result": [0, 1] * 25, "description": "Large alternating pattern"},
        {"num_qubits": 64, "initial_values": [1] * 64, "expected_result": [1] + [0] * 63, "description": "Large all ones"},
        {"num_qubits": 78, "initial_values": [0] * 78, "expected_result": [0] * 78, "description": "Large all zeros"},
        {"num_qubits": 40, "initial_values": [1, 0, 1, 0] * 10, "expected_result": [1, 1, 0, 0] * 10, "description": "Very large complex alternating pattern"},
        {"num_qubits": 72, "initial_values": [0, 1, 0, 1, 1, 0, 1, 0] * 9, "expected_result": [0, 1, 1, 0, 1, 1, 0, 1] * 9, "description": "Large complex pattern"}
    ]

    for case in test_cases:
        new_state = simulate_ghz(case["initial_values"], case["num_qubits"])
        print(new_state)
        assert (case["expected_result"] == new_state.get('x')[0].getBits(), ), f"Test failed for case: {case['description']}. Expected {case['expected_result']}, got {new_state.get('x')}"

