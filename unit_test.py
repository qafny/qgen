import os
from Source.quantumCode.AST_Scripts.XMLVisitor import XMLVisitor
from Source.quantumCode.AST_Scripts.ExpParser import ExpParser
from Source.repairCode.qprogram import QProblem

# Specify the folder path
folder_path = 'Benchmark/vqo_small_circuit_ex'

# List text files in the current folder
txt_files = [f for f in os.listdir(current_folder) if f.endswith('.txt')]

# Iterate through each text file
for txt_file in txt_files:
    file_path = os.path.join(current_folder, txt_file)

    # Read the file as a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Pass the file content to ExpParser to get the program
    exp_parser = ExpParser()
    program = exp_parser.parse(file_content)

    # Pass the program to XMLVisitor to get XML format
    xml_engine = XMLVisitor()
    xml_format = xml_engine.visit(program)

    # Print out the XML format
    print("XML Format for {file_name}:\n{xml_format}")

    # Pass the XML to QProgram
    qprogram = QProblem(xml_format)

    # qprogram.apply_some_transformations()
