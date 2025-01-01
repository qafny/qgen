
import os
import time
import pytest
import random
import json
from antlr4 import InputStream, CommonTokenStream
from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from Source.quantumCode.AST_Scripts.simulator import CoqNVal, Simulator, bit_array_to_int, to_binary_arr
from Source.quantumCode.AST_Scripts.ProgramTransformer import ProgramTransformer
from Source.quantumCode.AST_Scripts.SpecExpLexer import SpecExpLexer  
from Source.quantumCode.AST_Scripts.SpecExpParser import SpecExpParser  
from Source.quantumCode.AST_Scripts.SpecExpVisitor import SpecExpVisitor 

# Test function to initialize and run the rz_adder simulation
def new_function():
    test_file_path = ""
    with open(test_file_path, 'r') as f:
        str = f.read()
    i_stream = InputStream(str)
    lexer = XMLExpLexer(i_stream)
    t_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(t_stream)
    tree = parser.root()
    transform = ProgramTransformer()
    newTree = transform.visitRoot(tree)
    
    # Customizable `state` initialization
    val_array = to_binary_arr( )  # Convert value to array
    state = dict({})  # Initial state
    
    # Customizable `environment` initialization
    environment = dict({})  # Environment for simulation

    y = Simulator(state, environment)
    y.visitRoot(newTree)
    new_state = y.get_state()
    return bit_array_to_int()


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
                #code here 
    
    # Append the last case if it exists
    if current_case:
        test_cases.append(current_case)
    
    return test_cases

    
# Mapping TSL inputs to actual values
def map_tsl_to_values(term, parameter_type):
    #write code for mappings
        
    return mappings[parameter_type].get(term, (0,0))


def apply_constraints(mapped_case):
    #code for constraints

    return mapped_case

# Save the mapped TSL values to a JSON file so they can be reused
def save_mapped_tsl_to_file(test_cases, output_file):
     # If the file already exists, load it instead of generating new values
    if os.path.exists(output_file):
        print(f"Mapped TSL file {output_file} already exists. Loading existing values.")
        return
    mapped_test_cases = []

    for case in test_cases:
        mapped_case = {
            #Map tsl to values
        }
        mapped_case = apply_constraints(mapped_case)
        mapped_test_cases.append(mapped_case)

    # Save the mapped values to a JSON file
    with open(output_file, 'w') as f:
        json.dump(mapped_test_cases, f ,indent=4) 

    print(f"Mapped TSL values saved to {output_file}")

# Load mapped values from JSON file
def load_mapped_tsl_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found. Ensure the values are saved first.")
    
    with open(file_path, 'r') as f:
        return json.load(f)

# Usage: First, parse and save the mapped TSL values to a JSON file
test_cases = parse_tsl_file("tsl_filename")
save_mapped_tsl_to_file(test_cases, "file_path.json")

# Load the mapped values from the JSON file
mapped_test_cases = load_mapped_tsl_from_file("file.json")

#Generate pytest parameterization from the loaded values
@pytest.mark.parametrize( [
   
])
def test_function():
    expected = ""
    assert new_function() == expected
        
# Fixture to track the runtime of tests
@pytest.fixture(scope="session", autouse=True)
def starter(request):
        start_time = time.time()

        def finalizer():
            print("runtime: {}".format(str(time.time() - start_time)))

        request.addfinalizer(finalizer)
         

    