import os
import time
from logging import exception

import pytest
import random
import json
from antlr4 import InputStream, CommonTokenStream
#from scipy.special import expected

from Source.quantumCode.AST_Scripts.Retrievers import RPFRetriever, MatchCounterRetriever
from Source.quantumCode.AST_Scripts.ValidatorProgramVisitors import SimulatorValidator, AppRPFValidator
from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from Source.quantumCode.AST_Scripts.simulator import CoqNVal, Simulator, bit_array_to_int, to_binary_arr
from Source.quantumCode.AST_Scripts.ProgramTransformer import ProgramTransformer
from Source.quantumCode.AST_Scripts.SpecExpLexer import SpecExpLexer
from Source.quantumCode.AST_Scripts.SpecExpParser import SpecExpParser
from Source.quantumCode.AST_Scripts.SpecExpVisitor import SpecExpVisitor


@pytest.fixture(scope="module")
def parse_tree():
    test_file_path = f"{os.path.dirname(os.path.realpath(__file__))}/rz_adder_u.xml"
    with open(test_file_path, 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    tree = parser.root()
    transform = ProgramTransformer()
    new_tree = transform.visitRoot(tree)

    valid_tree = True

    try:
        # Validation of the Constraints.
        # Added per Dr. Li's suggestion on 11/16 to scoop out the validator behaviour out of the simulator as there can be
        # programs which does not always need to follow constraints like only having 1 app tag.
        validator = SimulatorValidator()
        validator.visitRoot(new_tree)

        # Non-Decreasing Recursive Fixed Point Factor Check
        rpf_retriever = RPFRetriever()
        rpf_retriever.visitRoot(new_tree)
        rpf_validator = AppRPFValidator(rpf_retriever)
        rpf_validator.visitRoot(new_tree)
    except Exception as e:
        print('\n ==============',e,'==============')
        valid_tree= False

    retriever = MatchCounterRetriever()
    retriever.visitRoot(new_tree)
    return new_tree, retriever, valid_tree


def run_simulator(n, i, X, M, parseTree):
    val_array = to_binary_arr(X, n)  # Convert value to array
    state = dict({"x": [CoqNVal(val_array, 0)],
                  "size": n,
                  "na": i,
                  "m": M})  # Initial state
    environment = dict({"x": n})  # Environment for simulation

    # Run the Simulator
    y = Simulator(state, environment)
    y.visitRoot(parseTree)
    new_state = y.get_state()
    return bit_array_to_int(new_state.get('x')[0].getBits(), n)


# Function to parse TSL file
def parse_tsl_file(file_path):
    test_cases = []
    current_case = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            if line.startswith("Test Case"):
                if current_case:
                    test_cases.append(current_case)
                current_case = {}  # Reset current case for next one
                continue  # Move to the next line

            # Split the line into key and value based on ':'
            if ':' in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()  # Normalize key to lowercase
                value = value.strip()

                # Assign the value to the appropriate key in the current case
                if key == 'n':
                    current_case['n'] = value
                elif key == 'i':
                    current_case['i'] = value
                elif key == 'm':
                    current_case['M'] = value
                elif key == 'x':
                    current_case['X'] = value

    # Append the last case if it exists
    if current_case:
        test_cases.append(current_case)

    return test_cases


# Mapping TSL inputs to actual values
def map_tsl_to_values(term, parameter_type):
    mappings = {
        'n': {  # Size of the qubit array
            'small': (1, 4),
            'medium': (4, 8),
            'large': (8, 16),
        },
        'i': {
            'small': (1, 4),  # Small iteration range
            'medium': (5, 8),
            'large': (9, 16)
        },
        'M': {  # Natural number 'm' to be added in rz_adder
            'small': (1, 10),
            'medium': (11, 100),
            'large': (101, 1000),
            'zero': (0, 0),
            'max_value': (10001, 65535)
        },
        'X': {  # Initial state of the qubit array 'x'
            'zero_state': (0, 0),
            'random_state': (101, 1000),
            'max_state': (10001, 65535),

        }
    }
    return mappings[parameter_type].get(term, (0, 0))


# Function to apply the constraint that 'na' should not exceed 'size'
def apply_constraints(mapped_case):
    # Ensure 'na' is less than or equal to 'size'
    if mapped_case['i'] > mapped_case['n']:
        mapped_case['i'] = random.randint(1, mapped_case['n'])

    max_val_represent_with_n_bit = ((2 ** mapped_case['n']) - 1)

    # ensure 'X' < 2^n
    if mapped_case['X'] > max_val_represent_with_n_bit:
        mapped_case['X'] = random.randint(1, max_val_represent_with_n_bit)

    # ensure 'M' < 2^n
    if mapped_case['M'] > max_val_represent_with_n_bit:
        mapped_case['M'] = random.randint(1, max_val_represent_with_n_bit)

    return mapped_case


# Save the mapped TSL values to a JSON file so they can be reused
def save_mapped_tsl_to_file(test_cases, output_file):
    # If the file already exists, load it instead of generating new values
    if os.path.exists(output_file):
        print(f"Mapped TSL file {output_file} already exists. Loading existing values.")
        return
    mapped_test_cases = []

    for case in test_cases:
        print(f"Current case: {case}")  # Debugging output

        if 'M' not in case:  # Check if 'M' is missing
            print("Skipping test case due to missing 'M'")  # Handle missing M
            continue  # Skip the test case if 'M' is missing
    for case in test_cases:
        mapped_case = {
            'n': random.randint(*map_tsl_to_values(case['n'], 'n')),
            'i': random.randint(*map_tsl_to_values(case['i'], 'i')),
            'X': random.randint(*map_tsl_to_values(case['X'], 'X')),
            'M': random.randint(*map_tsl_to_values(case['M'], 'M')),
        }
        mapped_case = apply_constraints(mapped_case)
        mapped_test_cases.append(mapped_case)

    # Save the mapped values to a JSON file
    with open(output_file, 'w') as f:
        json.dump(mapped_test_cases, f, indent=4)

    print(f"Mapped TSL values saved to {output_file}")


# Load mapped values from JSON file
def load_mapped_tsl_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found. Ensure the values are saved first.")

    with open(file_path, 'r') as f:
        return json.load(f)


# Usage: First, parse and save the mapped TSL values to a JSON file
test_cases = parse_tsl_file(f"{os.path.dirname(os.path.realpath(__file__))}/rz_adder.tsl.tsl")
save_mapped_tsl_to_file(test_cases, f"{os.path.dirname(os.path.realpath(__file__))}/mapped_tsl_values_new.json")

# Load the mapped values from the JSON file
mapped_test_cases = load_mapped_tsl_from_file(
    f"{os.path.dirname(os.path.realpath(__file__))}/mapped_tsl_values_new.json")



''' tests checks the correctness of the final or computed result/state of the rz_adder'''

# Generate pytest parameterization from the loaded values
@pytest.mark.parametrize("n ,i , X, M", [
    (case['n'], case['i'], case['X'], case['M'])
    for case in mapped_test_cases
])
def test_addition_random(n, i, X, M, parse_tree):
    if parse_tree[2]:
        expected = (X + (M % (2 ** i))) % 2 ** n
        assert run_simulator(n, i, X, M, parse_tree[0]) == expected
    else:
        assert False


@pytest.mark.parametrize("n ,i , X, M", [
    (case['n'], case['i'], case['X'], case['M'])
    for case in [{'n': 10, 'i': 5, 'X': 30, 'M': 0},{'n': 16, 'i': 5, 'X': 100, 'M': 0}]
])
def test_addition_with_edge_case_M(n, i, X, M, parse_tree):
    if parse_tree[2]:
        expected = (X + (M % (2 ** i))) % 2 ** n
        assert run_simulator(n, i, X, M, parse_tree[0]) == expected
    else:
        assert False

@pytest.mark.parametrize("n ,i , X, M", [
    (case['n'], case['i'], case['X'], case['M'])
    for case in [{'n': 8, 'i': 1, 'X': 30, 'M': 10},{'n': 16, 'i': 1, 'X': 30, 'M': 50},
                 {'n': 32, 'i': 2, 'X': 30, 'M': 1000}]
])
def test_addition_with_small_i(n, i, X, M, parse_tree):
    if parse_tree[2]:
        expected = (X + (M % (2 ** i))) % 2 ** n
        assert run_simulator(n, i, X, M, parse_tree[0]) == expected
    else:
        assert False

@pytest.mark.parametrize("n ,i , X, M", [
    (case['n'], case['i'], case['X'], case['M'])
    for case in [{'n': 8, 'i': 5, 'X': 30, 'M': 10},{'n': 16, 'i': 16, 'X': 30, 'M': 50},
                 {'n': 32, 'i': 16, 'X': 30, 'M': 999}]
])
def test_addition_with_med_i(n, i, X, M, parse_tree):
    if parse_tree[2]:
        expected = (X + (M % (2 ** i))) % 2 ** n
        assert run_simulator(n, i, X, M, parse_tree[0]) == expected
    else:
        assert False


# tests the bit manipulation or addition at bit level
@pytest.mark.parametrize("n ,i , X, M", [
    (case['n'], case['i'], case['X'], case['M'])
    for case in [{'n': 8, 'i': 5, 'X': 30, 'M': 10}]
])
def test_bit_add(n, i, X, M,parse_tree):
    j=0
    if i>1:
        j = i - 2

    bin_arr = to_binary_arr(M, n)
    #value contributed by jth bit
    val = bin_arr[j] * (2**j)

    if parse_tree[2]:
        expected =  (X + val) % 2 ** n
        assert run_simulator(n,i,X,val,parse_tree[0])==expected

        '''run_simulator(n,i,X,val,parse_tree[0]) - run_simulator(n,i-1,X,val,parse_tree[0]) 
           equivalent to the value contributed by ith bit'''
    else:
        assert False



''' tests check the generated program correctness with reference to the rz_adder_good program; 
     where the tests check fot the presence of certain components like app, if, and other 
     tags or expressions as present in the good program'''

def test_to_ensure_at_most_one_app_func(parse_tree):
   app_count= parse_tree[1].get_app_counter()
   assert app_count <= 1

def test_to_check_at_least_one_app_func(parse_tree):
    app_count= parse_tree[1].get_app_counter()
    assert app_count >= 1

def test_to_ensure_at_most_one_if_exp(parse_tree):
   if_count= parse_tree[1].get_if_counter()
   assert if_count <= 1

def test_to_check_at_least_if_exp(parse_tree):
    if_count = parse_tree[1].get_if_counter()
    assert if_count >= 1



''' Property based tests'''

#To tests the adder always results in a value greater than input (or equal when M is 0).
def test_to_check_result_greater_than_input(parse_tree):
    n,i,X,M= 8,3,20,30

    if parse_tree[2]:
        assert run_simulator(n, i, X, M, parse_tree[0]) > X
    else:
        assert False





# Fixture to track the runtime of tests
@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("\n runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)





'''
# Test function to initialize and run the rz_adder simulation
def run_rz_adder_test(n, i, X, M):
    #test_file_path = "Benchmark/rz_adder/rz_adder_good.xml"
    test_file_path =f"{os.path.dirname(os.path.realpath(__file__))}/rz_adder_good.xml"
    with open(test_file_path, 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    tree = parser.root()
    transform = ProgramTransformer()
    newTree = transform.visitRoot(tree)

    # Validation of the Constraints.
    # Added per Dr. Li's suggestion on 11/16 to scoop out the validator behaviour out of the simulator as there can be
    # programs which does not always need to follow constraints like only having 1 app tag.
    validator = SimulatorValidator()
    validator.visitRoot(newTree)

    # Non-Decreasing Recursive Fixed Point Factor Check
    rpf_validator = AppRPFValidator()
    rpf_validator.visitRoot(newTree)

    val_array = to_binary_arr(X, n)  # Convert value to array
    state = dict({"x": [CoqNVal(val_array, 0)],
                  "size": n,
                  "na": i,
                  "m": M})  # Initial state
    environment = dict({"x": n})  # Environment for simulation

    # Run the Simulator
    y = Simulator(state, environment)
    y.visitRoot(newTree)
    new_state = y.get_state()
    return bit_array_to_int(new_state.get('x')[0].getBits(), n)'''

# def test_basic_addition(n, i ,X , M):
#     expected = ((X) + (M % (2 ** i))) % 2 ** n
#     assert run_rz_adder_test(n ,i ,X , M) == expected

# def test_basic_addition(n, i, X, M):
#     exp = "E size : nat . E m : nat . E x : Q(size) . A i : i < size . nor(x, i) -> nor(x+ m, i)"
#     #exp = "E size : nat . E x : Q(size) . nor(x, 1) -> nor(x + 1, 2)"
#     lexer = SpecExpLexer(InputStream(exp))
#     stream = CommonTokenStream(lexer)
#     parser = SpecExpParser(stream)
#     tree = parser.program()  # Parse the arithmetic expression
#     visitor = SpecExpVisitor()
#     expected = visitor.visit(tree)  # Evaluate the expression using the visitor
#     print("Expected value from visitor:", expected,visitor)
#     assert run_rz_adder_test(n, i, X, M) == expected


'''# Generate pytest parameterization from the loaded values
@pytest.mark.parametrize("n ,i , X, M", [
    (case['n'], case['i'], case['X'], case['M'])
    for case in mapped_test_cases
])
def test_addition_random(n, i, X, M, get_tree):
    global _prev_rec_error
    try:
        if _prev_rec_error:
            raise RecursionError("Previous Recursion Error.")

        expected = ((X) + (M % (2 ** i))) % 2 ** n
        assert run_simulator(n, i, X, M, get_tree[0]) == expected

    except RecursionError as err_rec:
        print(err_rec)
        _prev_rec_error = True
        # pytest.fail(str(err_rec))
        assert True == False'''