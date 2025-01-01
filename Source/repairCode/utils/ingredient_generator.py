import random
import xml.etree.ElementTree as ET
import string

from Source.pyggi.utils import Logger
from Source.quantumCode.AST_Scripts.Retrievers import RPFRetriever
from Source.quantumCode.AST_Scripts.XMLProgrammer import Nat, QXType, Qty, Fun, QXIDExp


# Temporary upper bound and a lower bound for default x
def random_num(lbound=-100, ubound=100):
    return random.randint(lbound, ubound)


def get_random_op():
    operators = ['+', '-', '*', '/', '%', '^', '$']
    return random.choice(operators)


class IngredientGenerator:
    APP_IDENTIFIER = 'f'

    def __init__(self, type_environment, rpf_retriever: RPFRetriever):
        self.type_environment: dict = type_environment
        self.rpf_retriever = rpf_retriever
        self.vexp_factory = self.create_vexp_factory()

    def get_identifier(self, element, check_type=QXType):
        if element.tag.lower() == 'app':
            return 'f'
        type_environment_identifiers = [var_type for var_type, var_value in self.type_environment.items() if isinstance(var_value, check_type)]
        identifier = random.choice(type_environment_identifiers)
        return identifier

    def get_associated_class(self, identifier):
        # print(identifier)
        return self.type_environment[identifier]

    def generate_let(self):
        let_el = ET.Element("Let")
        let_el.set("id", self.get_identifier(let_el))
        return let_el

    def generate_cuexp(self):
        cuexp_el = ET.Element("pexp")
        cuexp_el.set("gate", "CU")
        cuexp_el.set("id", self.get_identifier(cuexp_el))
        cuexp_el.append(self.vexp_factory.create_vexp())
        cuexp_el.append(self.create_nextexp())
        return cuexp_el

    def generate_match(self):
        match_el = ET.Element("match")
        match_el.set("id", self.get_identifier(match_el))
        return match_el

    def generate_skipexp(self):
        skipexp_el = ET.Element("pexp")
        skipexp_el.set("gate", "SKIP")
        skipexp_el.set("id", self.get_identifier(skipexp_el))
        skipexp_el.append(self.vexp_factory.create_vexp())
        return skipexp_el

    def generate_xexp(self):
        xexp_el = ET.Element("pexp")
        xexp_el.set("gate", "X")
        xexp_el.set("id", self.get_identifier(xexp_el))
        xexp_el.append(self.vexp_factory.create_vexp())
        return xexp_el

    def generate_srexp(self):
        srexp_el = ET.Element("pexp")
        srexp_el.set("gate", "SR")
        srexp_el.set("id", self.get_identifier(srexp_el))
        srexp_el.append(self.vexp_factory.create_vexp())
        return srexp_el

    def generate_qftexp(self):
        qftexp_el = ET.Element("pexp")
        qftexp_el.set("gate", "QFT")
        qftexp_el.set("id", self.get_identifier(qftexp_el))
        qftexp_el.append(self.vexp_factory.create_vexp())
        return qftexp_el

    def generate_lshiftexp(self):
        lshiftexp_el = ET.Element("pexp")
        lshiftexp_el.set("gate", "Lshift")
        lshiftexp_el.set("id", self.get_identifier(lshiftexp_el))
        return lshiftexp_el

    def generate_rshiftexp(self):
        rshiftexp_el = ET.Element("pexp")
        rshiftexp_el.set("gate", "Rshift")
        rshiftexp_el.set("id", self.get_identifier(rshiftexp_el))
        return rshiftexp_el

    def generate_revexp(self):
        revexp_el = ET.Element("pexp")
        revexp_el.set("gate", "Rev")
        revexp_el.set("id", self.get_identifier(revexp_el))
        return revexp_el

    def generate_rqftexp(self):
        rqftexp_el = ET.Element("pexp")
        rqftexp_el.set("gate", "RQFT")
        rqftexp_el.set("id", self.get_identifier(rqftexp_el))
        return rqftexp_el

    def create_exp(self):
        exp_types = [
            self.generate_let,
            self.generate_app,
            self.generate_cuexp,
            self.generate_if,
            self.generate_match,
            self.generate_skipexp,
            self.generate_xexp,
            self.generate_srexp,
            self.generate_qftexp,
            self.generate_lshiftexp,
            self.generate_rshiftexp,
            self.generate_revexp,
            self.generate_rqftexp
        ]

        random_exp_generator = random.choice(exp_types)
        return random_exp_generator()

    def create_program(self):
        return self.create_exp()

    def create_nextexp(self, inner_element=None):
        next_el = ET.Element('next')
        if inner_element:
            next_el.append(inner_element)
        else:
            next_el.append(self.create_program())
        return next_el

    def generate_if(self):
        if_el = ET.Element("if")
        # insert true
        if_el.append(self.vexp_factory.create_if_gnum_vexp())
        if_el.append(self.create_nextexp(self.generate_skipexp()))
        if_el.append(self.create_nextexp(self.generate_skipexp()))
        return if_el

    def generate_app(self):
        app_el = ET.Element("app")
        identifier = self.get_identifier(app_el)
        function_mapping = self.get_associated_class(identifier)
        vars_in_function = function_mapping.args()
        type_mapping_before_function = function_mapping.pre()

        # get f from type_env
        # body of app should be a list of vexp. type args of Fun determine what vexp
        app_el.set("id", identifier)
        for i, var in enumerate(vars_in_function):
            type_inst_of_var = type_mapping_before_function[var]
            qvexp_factory = self.QVexpFactory(self)
            vexp_factory = self.VexpFactory(self)
            if isinstance(type_inst_of_var, Nat):
                if i == self.rpf_retriever.get_rpf_index():
                    # TODO: Try to see whether this can be achieved without the use of RPFRetriever, at least the step variable fetching.
                    exp = vexp_factory.et_vexp_element()
                    exp.set('op', 'id')
                    exp.text = self.rpf_retriever.get_rps_var_id()
                else:
                    exp = vexp_factory.create_vexp_idexp()
            else:
                if type_inst_of_var.type() == "Q":
                    exp = qvexp_factory.create_q_typed_qvexp()
                elif type_inst_of_var.type() == "Nor":
                    exp = qvexp_factory.create_nor_typed_qvexp(type_inst_of_var.get_num())
                else:
                    exp = qvexp_factory.create_phi_typed_qvexp(type_inst_of_var.get_num(), type_inst_of_var.get_anum())
            app_el.append(exp)
        return app_el

    def generate_pexp(self, *args):
        gate_types_with_vexp = ["X", "QFT", "CU"]
        gate_types_without_vexp = ["SR"]
        # done
        # find type of x
        # if x is Nor, then you can generate X, CU, QFT
        # if x is Phi, then you can do SR and RQFT
        pexp_el = ET.Element("pexp")
        identifier = self.get_identifier(pexp_el, check_type=Qty)

        var_type = self.get_associated_class(identifier).type()
        assert var_type in {'Nor', 'Phi'}
        if var_type == 'Nor':
            gate = random.choice(gate_types_with_vexp)
        else:
            gate = random.choice(gate_types_without_vexp)

        pexp_el.set("gate", gate)
        pexp_el.set("id", identifier)
        if gate in gate_types_with_vexp:
            pexp_el.append(self.vexp_factory.create_vexp())
            if gate == "CU":
                pexp_el.append(self.create_nextexp())
        else:
            if gate == "SR":
                # Changed to use only num type without idexps based on Dr. Li's suggestion on 10/26.
                pexp_el.append(self.vexp_factory.create_vexp_num())
            elif gate == "RQFT":
                pexp_el.text = ""

        return pexp_el

    # Generate variables, natural num, binary op
    # TODO: Change to support vexp recursive attribute
    def generate_vexp(self, target: ET.Element, is_rpf: bool):
        def choose_new_vexp_type(_target: ET.Element, _is_rpf: bool):
            if not _is_rpf:
                if _target.attrib["op"] == "id" or _target.attrib["op"] == "num":
                    opr_opts = ["VAR", "CONST"]
                else:
                    opr_opts = ["BIN"]
            else:
                opr_opts = ["VAR", "BIN"]

            return random.choice(opr_opts)

        def get_vexp_var(type_environment: dict, op_type: str, _target: ET.Element, _is_rpf: bool, *args):
            vexp_el = ET.Element("vexp")

            # Set op
            vexp_el.set("op", "id")
            vexp_el.set("type", op_type)

            if not _is_rpf:
                # Not the RPF
                # Get the allowed type variables and choose one randomly
                allowed_types = [var_type for var_type, var_value in type_environment.items() if isinstance(var_value, Nat)]
                opr = random.choice(allowed_types)
                vexp_el.text = str(opr)
            else:
                vexp_el.text = "m"

            return vexp_el

        def get_vexp_num(num_range = (0, 100), *args):
            vexp_el = ET.Element("vexp")

            # Set op
            vexp_el.set("op", "num")

            opr = random.choice(range(*num_range))  # A constant between 0 and 100
            vexp_el.text = str(opr)

            return vexp_el

        def get_vexp_bin(type_environment: dict, _target: ET.Element, _is_rpf: bool, *args):
            vexp_el = ET.Element("vexp")

            if not _is_rpf:
                # op_types = ["+", "-", "*", "/", "%", "^", "$"]
                op_types = ["+", "-"]
                if _target.attrib["op"] in op_types:
                    op_types.remove(_target.attrib["op"])
                op = random.choice(op_types)
                vexp_el.set("op", op)

                vexp1, vexp2 = list(_target)

                vexp_el.append(vexp1)
                vexp_el.append(vexp2)
            else:
                op_types = ["-", "/"]
                if _target.attrib["op"] == "id":
                    op = random.choice(op_types)
                    vexp_el.set("op", op)

                    def create_rpf_complex_expr(is_first: bool = True):
                        vexp_cet = ET.Element("vexp")

                        if is_first:
                            vexp_cet.set("op", "id")
                            vexp_cet.text = "m"
                        else:
                            # TODO: Try to see whether with which variables we can replace in the type env.
                            vexp_cet.set("op", "num")
                            if op == "-":
                                vexp_cet.text = str(1)
                            else:
                                vexp_cet.text = str(2)

                        return vexp_cet

                    vexp1 = create_rpf_complex_expr(True)
                    vexp2 = create_rpf_complex_expr(False)

                    vexp_el.append(vexp1)
                    vexp_el.append(vexp2)
                else:
                    # TODO: Add support for deeper expressions, Find whether there is a more elegant way to do this.
                    # IMPORTANT: Currently we only consider expressions not deeper than 2 terms

                    vexp1, vexp2 = list(_target)

                    alter_choice = random.choice(["OPRT", "OPRN"])
                    if alter_choice == "OPRT":
                        if _target.attrib["op"] in op_types:
                            op_types.remove(_target.attrib["op"])

                        op = random.choice(op_types)
                        vexp_el.set("op", op)
                    else:
                        vexp_el.set("op", _target.attrib["op"])

                        vexp2_o_oprn2 = int(vexp2.text)
                        vexp2_n_oprn2 = vexp2_o_oprn2
                        while vexp2_n_oprn2 == vexp2_o_oprn2:
                            vexp2_n_oprn2 = random_num(1 if _target.attrib["op"] == "-" else 2, 100)  # 100 for now

                        vexp2.text = str(vexp2_n_oprn2)

                    vexp_el.append(vexp1)
                    vexp_el.append(vexp2)

            return vexp_el

        def _generate_vexp(type_environment: dict, _target: ET.Element, _is_rpf: bool, *args):
            in_opr_opt = choose_new_vexp_type(_target, _is_rpf)
            if in_opr_opt == "VAR":
                return get_vexp_var(type_environment, "Nat", _target, _is_rpf)
            elif in_opr_opt == "CONST":
                return get_vexp_num()
            elif in_opr_opt == "BIN":
                return get_vexp_bin(type_environment, _target, _is_rpf)
            else:
                return ET.Element("vexp")

        return _generate_vexp(self.type_environment, target, is_rpf)

    def do_generate_ingredients(self, target_element):
        element_functions = [self.generate_pexp, self.generate_app, self.generate_if]
        random_element_function = random.choice(element_functions)
        return random_element_function()

    def create_qvexp_factory(self):
        return self.QVexpFactory(self)

    def create_vexp_factory(self):
        return self.VexpFactory(self)

    class QVexpFactory:

        def __init__(self, ingredient_generator):
            self.ingredient_generator = ingredient_generator

        @staticmethod
        def et_qvexp_element():
            return ET.Element("qvexp")

        def get_random_nor_phi_param(self):
            allowed_param_types = [int, Nat]
            opt = random.choice(allowed_param_types)

            if opt == int:
                return random_num()
            else:
                allowed_q_type_types = [var_type for var_type, var_value in self.ingredient_generator.type_environment.items() if isinstance(var_value, Nat)]
                return random.choice(allowed_q_type_types)

        def get_single_param(self, param_class_inst = None):
            if param_class_inst is None:
                return self.get_random_nor_phi_param()
            else:
                if isinstance(param_class_inst, QXIDExp):
                    allowed_q_type_types = [var_type for var_type, var_value in self.ingredient_generator.type_environment.items() if isinstance(var_value, Nat)]
                    return random.choice(allowed_q_type_types)
                else:
                    return random_num()

        def get_phi_param(self, param1_class_inst = None, param2_class_inst = None):
            param1, param2 = None, None
            if param1_class_inst is None:
                param1 = self.get_random_nor_phi_param()
            else:
                param1 = self.get_single_param(param1_class_inst)

            if param2_class_inst is None:
                param2 = self.get_random_nor_phi_param()
            else:
                param2 = self.get_single_param(param1_class_inst)

            return param1, param2

        def create_q_typed_qvexp(self):
            op_qvexp = self.et_qvexp_element()
            op_qvexp.set("op", "id")

            allowed_types = [var_type for var_type, var_value in self.ingredient_generator.type_environment.items() if isinstance(var_value, Qty)]
            opr = random.choice(allowed_types)
            op_qvexp.text = opr

            return op_qvexp

        def create_nor_typed_qvexp(self, param1_class_inst):
            op_qvexp = self.et_qvexp_element()
            op_qvexp.set("op", "id")

            opr_q_type_type = self.get_single_param(param1_class_inst)
            op_qvexp.set("type", f"Nor({opr_q_type_type})")

            allowed_types = [var_type for var_type, var_value in self.ingredient_generator.type_environment.items() if isinstance(var_value, Qty)]
            opr = random.choice(allowed_types)
            op_qvexp.text = opr

            return op_qvexp

        def create_phi_typed_qvexp(self, param1_type_inst, param2_type_inst):
            op_qvexp = self.et_qvexp_element()
            op_qvexp.set("op", "id")

            opr1_q_type_type, opr2_q_type_type = self.get_phi_param(param1_type_inst, param2_type_inst)
            op_qvexp.set("type", f"Phi({opr1_q_type_type}, {opr2_q_type_type})")

            allowed_types = [var_type for var_type, var_value in self.ingredient_generator.type_environment.items() if isinstance(var_value, Qty)]
            opr = random.choice(allowed_types)
            op_qvexp.text = opr

            return op_qvexp

        def create_random_typed_qvexp(self):
            qvexp_gen_functions = [self.create_q_typed_qvexp, self.create_nor_typed_qvexp, self.create_phi_typed_qvexp]
            random_qvexp_gen_function = random.choice(qvexp_gen_functions)
            return random_qvexp_gen_function()

    class VexpFactory:
        def __init__(self, ingredient_generator):
            self.ingredient_generator = ingredient_generator
            self.vexp_types_not_nested = [self.create_vexp_num, self.create_vexp_idexp]
            self.vexp_types = self.vexp_types_not_nested + [self.create_vexp_nested]

        @staticmethod
        def et_vexp_element():
            return ET.Element('vexp')

        def create_if_gnum_vexp(self):
            op_vexp = self.et_vexp_element()
            op_vexp.set("op", "$")

            def create_operand():
                allowed_types = [var_type for var_type, var_value in self.ingredient_generator.type_environment.items() if isinstance(var_value, Nat)]

                opr_vexp = self.et_vexp_element()
                opr = random.choice(allowed_types)
                opr_vexp.set("op", "id")
                opr_vexp.text = opr

                return opr_vexp

            opr1_vexp = create_operand()
            opr2_vexp = create_operand()

            op_vexp.append(opr1_vexp)
            op_vexp.append(opr2_vexp)

            return op_vexp

        def create_vexp_idexp(self):
            idexp = self.et_vexp_element()
            idexp.set('op', 'id')
            idexp.text = self.ingredient_generator.get_identifier(idexp, Nat)
            return idexp

        def create_vexp_num(self):
            vexp = self.et_vexp_element()
            vexp.set('op', 'num')
            vexp.text = str(random_num())
            return vexp

        def create_vexp_nested(self):
            vexp = self.et_vexp_element()
            vexp.set('op', get_random_op())
            vexp.append(self.create_vexp(self.vexp_types_not_nested))
            vexp.append(self.create_vexp(self.vexp_types_not_nested))
            return vexp

        def create_vexp(self):
            possible_vexp_types = self.vexp_types_not_nested
            function = random.choice(possible_vexp_types)
            return function()

        def vexp_quantum(self, identifier, el_type):
            vexp = self.et_vexp_element()
            vexp.set('op', 'id')
            vexp.set('type', el_type)
            vexp.text = identifier
            return vexp

        def vexp_arithmetic(self):
            # only numexp
            pass

    def generate_ingredients(self):
        generator = IngredientGenerator(self.type_environment, self.rpf_retriever)
        ingredient = generator.do_generate_ingredients(None)
        return ingredient
