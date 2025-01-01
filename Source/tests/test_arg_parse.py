import argparse
import re
import sys
from io import StringIO

import pytest


def arg_generator():
    parser = argparse.ArgumentParser(description='PYGGI Bug Repair Example')
    parser.add_argument('--project_path', type=str, default='../Benchmark/Triangle')
    parser.add_argument('--algorithm', type=str, default='ga')
    parser.add_argument('--epoch', type=int, default=1, help='total epoch(default: 1)')
    parser.add_argument('--iter', type=int, default=8, help='total iterations per epoch(default: 100)')
    parser.add_argument('--pop', type=int, default=8, help='population size(default: 10)')
    parser.add_argument('--mutation', type=float, default=1, help='mutation rate(default: 0.1)')
    parser.add_argument('--crossover', type=float, default=1, help='crossover rate(default: 0.9)')
    parser.add_argument('--sel', type=str, default='tournament', help='selection operator(default: tournament)')
    parser.add_argument('--tags', type=str, default='[]', help='XML tags (default: [])')
    parser.add_argument('--operators', type=str, default='[]', help='Operators (default: [])')
    return parser


@pytest.fixture
def parser():
    return arg_generator()


class TestParseHasArguments:

    def test_algorithm(self, parser):
        args = parser.parse_args()
        assert args.algorithm

    def test_description(self, parser):
        assert parser.description

    def test_epoch(self, parser):
        args = parser.parse_args()
        assert args.epoch

    def test_iter(self, parser):
        args = parser.parse_args()
        assert args.iter

    def test_pop(self, parser):
        args = parser.parse_args()
        assert args.pop

    def test_mutation(self, parser):
        args = parser.parse_args()
        assert args.mutation

    def test_crossover(self, parser):
        args = parser.parse_args()
        assert args.crossover

    def test_sel(self, parser):
        args = parser.parse_args()
        assert args.sel

    def test_tags(self, parser):
        args = parser.parse_args()
        assert args.tags

    def test_operators(self, parser):
        args = parser.parse_args()
        assert args.operators


class TestHelpMatchDefault:

    @pytest.fixture
    def capture_stdout(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        yield captured_output
        sys.stdout = sys.__stdout__

    @pytest.fixture
    def help_message(self, capture_stdout, parser):
        parser.print_help()
        return capture_stdout.getvalue().strip()

    def test_default_iter_in_help_message(self, help_message, parser):
        match = re.search(r'--iter .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('iter')
        assert help_default[:-1] == str(
            default_value), f"Default iter value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"

    def test_default_epoch_in_help_message(self, help_message, parser):
        match = re.search(r'--epoch .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('epoch')
        assert help_default[:-1] == str(
            default_value), f"Default epoch value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"

    def test_default_pop_in_help_message(self, help_message, parser):
        match = re.search(r'--pop .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('pop')
        assert help_default[:-1] == str(
            default_value), f"Default pop value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"

    def test_default_mutation_in_help_message(self, help_message, parser):
        match = re.search(r'--mutation .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('mutation')
        assert help_default[:-1] == str(
            default_value), f"Default mutation value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"

    def test_default_sel_in_help_message(self, help_message, parser):
        match = re.search(r'--sel .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('sel')
        assert help_default[:-1] == str(
            default_value), f"Default sel value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"

    def test_default_tags_in_help_message(self, help_message, parser):
        match = re.search(r'--tags .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('tags')
        assert help_default[:-1] == str(
            default_value), f"Default tags value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"

    def test_default_crossover_in_help_message(self, help_message, parser):
        match = re.search(r'\(default: (\S+)\)', help_message)  # Adjusted regular expression
        help_default = match.group(1)
        default_value = parser.get_default('crossover')
        assert help_default == str(
            default_value), f"Default crossover value in help message '{help_default}' doesn't match the set default value '{default_value}'"

    def test_default_operators_in_help_message(self, help_message, parser):
        match = re.search(r'--tags .*default: (\S+)', help_message)
        help_default = match.group(1)
        default_value = parser.get_default('operators')
        assert help_default[:-1] == str(
            default_value), f"Default operators value in help message '{help_default[:-1]}' doesn't match the set default value '{default_value}'"
