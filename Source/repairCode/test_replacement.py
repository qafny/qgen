import pytest
from lxml import etree
from repairCode.operators import QGateReplacement
from pyggi.tree import XmlEngine

class Program:
    def __init__(self):
        self.engines = {'test.xml': XmlEngine()}
        self.contents = {}
        self.modification_points = {}

@pytest.fixture
def setup_xml():
    original_xml = """
    <root>
        <let id='f'>
            <vexp op='id'>x</vexp>
            <vexp op='id'>n</vexp>
            <vexp op='id'>size</vexp>
            <vexp op='id'>M</vexp>
            <match id='n'>
                <pair case='0'>
                    <pexp gate='SKIP' id='x'>
                        <vexp op='num'>0</vexp>
                    </pexp>
                </pair>
                <pair case='m'>
                    <pexp gate='CU' id='x'>
                        <vexp op='num'>1</vexp>
                    </pexp>
                </pair>
            </match>
        </let>
        <pexp gate='QFT' id='x'>
            <vexp op='num'>0</vexp>
        </pexp>
        <app id='f'>
            <vexp op='id'>x</vexp>
            <vexp op='id'>na</vexp>
            <vexp op='id'>na</vexp>
            <vexp op='id'>m</vexp>
        </app>
        <pexp gate='RQFT' id='x'></pexp>
    </root>
    """
    return original_xml

def normalize_xml(xml_str):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(xml_str, parser)
    return etree.tostring(tree, pretty_print=True).decode('utf-8')

def test_qgate_replacement(setup_xml):
    program = Program()
    target_file = 'test.xml'
    new_contents = {target_file: setup_xml}
    modification_points = {target_file: ['./let[1]/match[1]/pair[2]/pexp[1]']}

    # Setting up the program contents and modification points for the ingredient
    program.contents = {target_file: etree.fromstring(setup_xml)}
    program.modification_points = modification_points

    # Create the QGateReplacement operation
    qgate_replacement = QGateReplacement(target=(target_file, 0), ingredient=(target_file, 0), target_tag='pexp')

    # Apply the replacement
    result = qgate_replacement.apply(program, new_contents, modification_points)

    assert result is not None

    print("Actual XML:")
    print(new_contents[target_file])

    expected_xml = """
    <root>
        <let id='f'>
            <vexp op='id'>x</vexp>
            <vexp op='id'>n</vexp>
            <vexp op='id'>size</vexp>
            <vexp op='id'>M</vexp>
            <match id='n'>
                <pair case='0'>
                    <pexp gate='SKIP' id='x'>
                        <vexp op='num'>0</vexp>
                    </pexp>
                </pair>
                <pair case='m'>
                    <pexp gate='X' id='x'>
                        <vexp op='num'>1</vexp>
                    </pexp>
                </pair>
            </match>
        </let>
        <pexp gate='QFT' id='x'>
            <vexp op='num'>0</vexp>
        </pexp>
        <app id='f'>
            <vexp op='id'>x</vexp>
            <vexp op='id'>na</vexp>
            <vexp op='id'>na</vexp>
            <vexp op='id'>m</vexp>
        </app>
        <pexp gate='RQFT' id='x'></pexp>
    </root>
    """

    normalized_expected = normalize_xml(expected_xml)
    normalized_actual = normalize_xml(new_contents[target_file])

    print("Normalized Expected XML:")
    print(normalized_expected)
    print("Normalized Actual XML:")
    print(normalized_actual)

    assert normalized_expected == normalized_actual

if __name__ == "__main__":
    pytest.main()
