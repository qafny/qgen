import pytest
import xml.etree.ElementTree as ET
from ingredient_generator import IngredientGenerator
from Source.quantumCode.AST_Scripts.XMLProgrammer import Qty, Nat


@pytest.fixture
def type_environment():
    return {
        'x': Qty(16),
        'na': Nat(),
        'size': Nat(),
        'm': Nat()
    }


@pytest.fixture
def generator(type_environment):
    return IngredientGenerator(type_environment)


def test_generate_vexp(generator):
    vexp = generator.vexp_factory.create_vexp()
    assert vexp is not None
    assert vexp.tag == 'vexp'
    assert vexp.get('op') in ['id', 'num', '+', '-', '*', '/', '%', '^', '$']


def test_generate_if(generator):
    if_block = generator.generate_if(None, None)
    assert if_block.tag == 'Ifa'
    assert len(if_block) == 3  # One vexp and two nextexp elements


def test_generate_app(generator):
    app_block = generator.generate_app()
    assert app_block.tag == 'App'
    assert len(app_block) == 1  # One vexp element


def test_generate_pexp(generator):
    pexp_block = generator.generate_pexp()
    assert pexp_block.tag == 'pexp'
    assert pexp_block.get('gate') in ["SKIP", "X", "SR", "QFT", "CU", "Lshift", "Rshift", "Rev", "RQFT"]
    if pexp_block.get('gate') in ["SKIP", "X", "SR", "QFT", "CU"]:
        assert len(pexp_block) >= 1  # Should have at least one vexp
    if pexp_block.get('gate') == "CU":
        assert len(pexp_block) == 2  # Should have exactly two elements (vexp and nextexp)


def test_generate_ingredients(generator):
    ingredient_block = generator.generate_ingredients(None)
    assert ingredient_block is not None
    assert ingredient_block.tag in ['Ifa', 'App', 'pexp']
