import time
import pytest
from lxml import etree

# Fixture to measure runtime
@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)

# Function to parse the XML content
def parse_xml(xml_content):
    return etree.fromstring(xml_content)

# Function to check the structure of the XML content
def check_structure(root):
    assert root.tag == "let"
    ids = root.findall('id')
    assert len(ids) == 5
    assert ids[0].text.strip() == 'f'
    assert ids[1].text.strip() == 'x'
    assert ids[2].text.strip() == 'n'
    assert ids[3].text.strip() == 'size'
    assert ids[4].text.strip() == 'M'

# Example XML content to test
xml_content = """
<let>
    <id> f </id>
    <id type='qubits'> x </id>
    <id type='nat'> n </id>
    <id type='nat'> size </id>
    <id type='bits'> M </id>
    <match>
        <id> n </id>
        <pair>
            <vexp> 0 </vexp>
            <pexp gate='SKIP'>
                <id> x </id>
                <vexp> 0 </vexp>
            </pexp>
        </pair>
        <pair>
            <vexp op='plus'>
                <id> m </id>
                <vexp> 1 </vexp>
            </vexp>
            <pexp gate='SKIP'>
                <id> x </id>
                <vexp> 0 </vexp>
            </pexp>
        </pair>
    </match>
</let>
"""

def check_pair_structure(pair, vexp_text, id_text, vexp_gate_text):
    assert pair.find('vexp').text.strip() == vexp_text
    pexp = pair.find('pexp')
    assert pexp.get('gate') == 'SKIP'
    assert pexp.find('id').text.strip() == id_text
    assert pexp.find('vexp').text.strip() == vexp_gate_text

# Test cases
def test_check_structure():
    root = parse_xml(xml_content)
    check_structure(root)

def test_check_match_structure():
    root = parse_xml(xml_content)
    match = root.find('match')
    assert match is not None
    ids = match.findall('id')
    assert len(ids) == 1
    assert ids[0].text.strip() == 'n'

def test_check_pairs_structure():
    root = parse_xml(xml_content)
    match = root.find('match')
    pairs = match.findall('pair')
    assert len(pairs) == 2
    check_pair_structure(pairs[0], '0', 'x', '0')
    assert pairs[1].find('vexp').find('vexp').text.strip() == '1'
    check_pair_structure(pairs[1], 'm', 'x', '0')

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)

# Run the tests
if __name__ == "__main__":
    pytest.main()
