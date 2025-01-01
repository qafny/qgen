import xml.etree.ElementTree as ET
from xml.dom import minidom

from antlr4 import InputStream, CommonTokenStream
from antlr4.tree.Trees import Trees

from Source.quantumCode.AST_Scripts.ProgramTransformer import ProgramTransformer
from Source.quantumCode.AST_Scripts.XMLExpLexer import XMLExpLexer
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from Source.quantumCode.AST_Scripts.XMLExpPrinter import XMLExpPrinter
from Source.quantumCode.AST_Scripts.XMLProgrammer import *


def pretty_print_element(element):
    def print_xml_exp():
        printer = XMLExpPrinter({})
        printer.visitRoot(element)
        return printer.xml_output

    pretty_string = ""
    if isinstance(element, XMLExpParser.RootContext):
        pretty_string = Trees.toStringTree(element, None, XMLExpParser)
    elif isinstance(element, QXTop):
        pretty_string = print_xml_exp()
    else:
        raw_str = ET.tostring(element, 'utf-8')
        parsed = minidom.parseString(raw_str)
        pretty_string = parsed.toprettyxml(indent="  ")
    return pretty_string


def parse_string_to_ast(xml_string):
    input_stream = InputStream(xml_string)
    lexer = XMLExpLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(token_stream)
    target_top_node = parser.root()
    transformer = ProgramTransformer()
    new_tree = transformer.visit(target_top_node)
    return new_tree


def convert_xml_element_to_ast(element):
    xml_string = ET.tostring(element, encoding='unicode')
    ast_root = parse_string_to_ast(xml_string)
    return ast_root


def convert_xml_element_to_string(element):
    xml_string = ET.tostring(element, encoding='unicode')
    return xml_string


def delete_block(parent):
    for child in parent.findall("block"):
        parent.remove(child)
