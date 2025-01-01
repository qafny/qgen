"""
Possible Edit Operators
"""
import copy
import random
import xml.etree.ElementTree as ET

from lxml import etree

from Source.quantumCode.AST_Scripts.Retrievers import RPFRetriever
from Source.quantumCode.AST_Scripts.TypeDetector import TypeDetector
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.tree.xml_engine import XmlEngine
from Source.quantumCode.AST_Scripts.TypeChecker import TypeChecker
from Source.quantumCode.AST_Scripts.XMLExpParser import XMLExpParser
from repairCode.configs.type_env import type_envs
from repairCode.utils.ingredient_generator import IngredientGenerator
from repairCode.utils.operator_utils import convert_xml_element_to_ast, convert_xml_element_to_string, pretty_print_element, delete_block


class QGateReplacement(StmtReplacement):
    def __init__(self, target, ingredient, target_tag):
        super(QGateReplacement, self).__init__(target, ingredient)
        self.target_tag = target_tag

    def apply(self, program, new_contents, modification_points):
        print(" Qgate replacement, apply")
        engine = program.engines[self.target[0]]
        result = self.__class__.do_replace(self, program, new_contents, modification_points)
        return result

    def _get_xml_for_root_element(self, contents):
        return contents[self.target[0]].find('.')

    def _get_ast_for_root_element(self, contents):
        root = contents[self.target[0]].find('.')
        return convert_xml_element_to_ast(root)

    def check_type_environment(self, contents, initial_type_environment):
        root = self._get_ast_for_root_element(contents)
        type_checker = TypeChecker(initial_type_environment)
        type_checker.visit(root)
        return type_checker.type_environment

    @staticmethod
    def insert_adjacent_to_parent(parent_of_parent, parent, ingredient):
        for i, elem in enumerate(parent_of_parent):
            if elem == parent:
                tmp = copy.deepcopy(ingredient)
                tmp.tail = None
                parent_of_parent.insert(i, tmp)
                break

    @staticmethod
    def _replace_vexp_ingredient(parent, target, ingredient):
        for i, child in enumerate(parent):
            if child == target:
                tmp = copy.deepcopy(ingredient)
                parent.insert(i, tmp)
                parent.remove(child)
                break

    @staticmethod
    def _generate_vexp_replacement_ingredient(detected_type_environment, rpf_retr, target, parent, pop, popop):
        # Detect if vexp is RPF
        def compare_vexp_to_target(elem: ET.Element):
            for k, v in elem.attrib.items():
                if k not in target.attrib:
                    return False
                if v != target.attrib[k]:
                    return False

            return elem.tag == target.tag and elem.text == target.text

        flag_rpf = False
        if parent.tag == "app":
            if pop.tag == "pair" and popop.tag == "match":
                flag_rpf = True
            elif pop.tag == "match":
                flag_rpf = True

        if flag_rpf:
            flag_rpf = False
            for i, p_vexp_el in enumerate(parent):
                flag_rpf = i == rpf_retr.get_rpf_index() and compare_vexp_to_target(p_vexp_el)
                if flag_rpf:
                    break

        ingr_gen = IngredientGenerator(detected_type_environment, rpf_retr)
        ingr_vexp = ingr_gen.generate_vexp(target, flag_rpf)

        return ingr_vexp

    def do_replace(self, program, contents, modification_points):
        target_file, target_idx = self.target

        # Replace using "insertion"-like approach
        target = contents[target_file].find(modification_points[target_file][target_idx])
        parent = contents[target_file].find(modification_points[target_file][target_idx] + '..')
        pop = contents[target_file].find(modification_points[target_file][target_idx] + '....')
        popop = contents[target_file].find(modification_points[target_file][target_idx] + '......')

        initial_type_environment = type_envs[target_file]
        checked_type_environment = self.check_type_environment(contents, initial_type_environment)
        print("env before", checked_type_environment)

        # block_el = ET.Element("block")
        # parent_map = {c: p for p in contents[target_file].iter() for c in p}
        # self.insert_adjacent_to_parent(parent_map[parent], parent, block_el)
        # print("XML with Block", ET.tostring(contents[target_file], "unicode"))
        # print(ET.tostring(contents["rz_adder.xml"], "unicode"))
        root_ast_element: XMLExpParser.RootContext = self._get_ast_for_root_element(contents)
        type_detector = TypeDetector(checked_type_environment)
        type_detector.visit(root_ast_element)
        # delete_block(parent_map[parent])
        print("env after", type_detector.type_environment)

        if target is None:
            return False

        rpf_retr = RPFRetriever()
        rpf_retr.visit(root_ast_element)

        ingr_vexp = self._generate_vexp_replacement_ingredient(type_detector.type_environment, rpf_retr, target, parent, pop, popop)
        if ingr_vexp is None:
            return False

        self._replace_vexp_ingredient(parent, target, ingr_vexp)

        return True

    @classmethod
    def create(cls, program, target_file=None, ingr_file=None, target_tag=None, method='random'):
        if target_file is None:
            target_file = program.random_file(XmlEngine)
        if ingr_file is None:
            ingr_file = program.random_file(engine=program.engines[target_file])
        assert program.engines[target_file] == program.engines[ingr_file]
        return cls(program.replace_target(target_file, method), program.replace_target(ingr_file, 'random'), target_tag)


class QGateInsertion(StmtInsertion):
    def __init__(self, target, ingredient, direction='before'):
        super(QGateInsertion, self).__init__(target, ingredient, direction)

    def apply(self, program, new_contents, modification_points):
        engine = program.engines[self.target[0]]
        result = self.do_insert(self, program, self, new_contents, modification_points, engine)
        return result

    def insert_adjacent_to_target(self, parent, target, ingredient):
        print(ingredient)
        for i, child in enumerate(parent):
            if child == target:
                try:
                    tmp = copy.deepcopy(ingredient)
                except Exception as e:
                    print("qahh")

                if self.direction == 'after':
                    tmp.tail = child.tail
                    child.tail = None
                    i += 1
                else:
                    tmp.tail = None
                parent.insert(i, tmp)
                break

    def do_insert(self, cls, program, op, new_contents, modification_points, engine):
        def choose_ingredient():
            return IngredientGenerator(checked_type_env, rpf_retr).generate_ingredients()
        def check_type(init_type_env):
            root = new_contents[op.target[0]].find('.')
            converted_root = convert_xml_element_to_ast(root)
            type_checker = TypeChecker(init_type_env)
            type_checker.visit(converted_root)
            return type_checker.type_environment

        def print_env(prefix: str, tenv: dict):
            print(prefix, [f"{var}: {str(var_obj.type())}" for var, var_obj in tenv.items()])

        # get elements
        target = new_contents[op.target[0]].find(modification_points[op.target[0]][op.target[1]])
        parent = new_contents[op.target[0]].find(modification_points[op.target[0]][op.target[1]] + '..')
        initial_type_env = type_envs[op.target[0]]
        checked_type_env = check_type(initial_type_env)
        # block_el = ET.Element("block")
        # self.insert_adjacent_to_target(parent, target, block_el)
        root_element: ET.Element = new_contents[op.target[0]].find('.')
        root_ast_element: XMLExpParser.RootContext = convert_xml_element_to_ast(root_element)
        print_env("env before", checked_type_env)
        type_detector = TypeDetector(checked_type_env)
        type_detector.visit(root_ast_element)
        print_env("env after", type_detector.type_environment)
        # ingredient = program.contents[op.ingredient[0]].find(
        #     program.modification_points[op.ingredient[0]][op.ingredient[1]])

        rpf_retr = RPFRetriever()
        rpf_retr.visit(root_ast_element)

        ingredient = choose_ingredient()
        print(type(ingredient))
        if target is None or ingredient is None:
            return False

        # delete_block(parent)
        self.insert_adjacent_to_target(parent, target, ingredient)

        def update_modification_points():
            head, tag, pos, _ = engine.split_xpath(modification_points[op.target[0]][op.target[1]])
            for i, xpath in enumerate(modification_points[op.target[0]]):
                if i < op.target[1]:
                    continue
                h, t, p, s = engine.split_xpath(xpath, head)
                if h != head and xpath != 'deleted':
                    break
                if t == tag and p == pos:
                    continue
                if t  == ingredient.tag and op.direction == 'before':
                    if s:
                        new_pos = '{}/{}[{}]/{}'.format(h, t, p + 1, s)
                    else:
                        new_pos = '{}/{}[{}]'.format(h, t, p + 1)
                    modification_points[op.target[0]][i] = new_pos
        update_modification_points()
        return True

    @classmethod
    def create(cls, program, target_file=None, ingr_file=None, direction=None, method='random'):
        if target_file is None:
            target_file = program.random_file(XmlEngine)
        if ingr_file is None:
            ingr_file = program.random_file(engine=program.engines[target_file])
        assert program.engines[target_file] == program.engines[ingr_file]
        if direction is None:
            direction = random.choice(['before', 'after'])
        return cls(program.app_target(target_file, method), program.app_target(ingr_file, 'random'), direction)
    #modify here
    #1. program.app_target(target_file, method)
    #2. program.app_target(ingr_file, 'random')
    #3. you will be able to see candidates here.
    # app/if/pexp
    # if see app, then only allowed if, and pexp
    #if see if/pexp.
    # choose a variable, will have the env to tell you what variables are aviable
    # perform if/pexp on the variable
    #look at the type of the variable in env, if it is Phi, then use SR/RQFT gate only
    #if it is Nor, then use X, CU,
    #if it is nat, can only use if with two branching

#todo
# separate out pexp and vexp insertion functions

class QGateDeletion(StmtDeletion):
    def __init__(self, target):
        super(QGateDeletion, self).__init__(target)

    def apply(self, program, new_contents, modification_points):
        print("Qgate deletion apply")
        result = self.do_delete(program, new_contents, modification_points)
        return result

    def _get_xml_for_root_element(self, contents):
        return contents[self.target[0]].find('.')

    def _get_ast_for_root_element(self, contents):
        root = contents[self.target[0]].find('.')
        return convert_xml_element_to_ast(root)

    def check_type_environment(self, contents, initial_type_environment):
        root = self._get_ast_for_root_element(contents)
        type_checker = TypeChecker(initial_type_environment)
        type_checker.visit(root)
        return type_checker.type_environment

    @staticmethod
    def _delete_with_ingredient(parent, target, ingredient):
        for i, child in enumerate(parent):
            if child == target:
                tmp = copy.deepcopy(ingredient)
                parent.insert(i, tmp)
                parent.remove(child)
                break

    def do_delete(self, program, contents, modification_points):
        target_file, target_idx = self.target

        # Delete using "replacement"-like approach with SKIP
        target = contents[target_file].find(modification_points[target_file][target_idx])
        parent = contents[target_file].find(modification_points[target_file][target_idx] + '..')

        # Note: Type checker is not needed here but added to comply with Ingredient Generator requirements.
        initial_type_environment = type_envs[target_file]
        checked_type_environment = self.check_type_environment(contents, initial_type_environment)
        print("env before", checked_type_environment)

        # We do not need RPF retriever for deletions, so add if needed.
        ingr_vexp = IngredientGenerator(checked_type_environment, None).generate_skipexp()

        if target is None or ingr_vexp is None:
            return False

        self._delete_with_ingredient(parent, target, ingr_vexp)

        return True

    @classmethod
    def create(cls, program, target_file=None, method='random'):
        if target_file is None:
            target_file = program.random_file(XmlEngine)
        return cls(program.delete_target(target_file, method))
