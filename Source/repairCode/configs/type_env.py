from Source.quantumCode.AST_Scripts.XMLProgrammer import Qty, Nat

type_envs = {
    'rz_adder.xml': {
        'x': Qty('size'),
        'na': Nat(),
        'size': Nat(),
        'm': Nat()
    },
    'cl_adder.xml': {
        'xa': Nat(),
        'ya': Nat(),
        'ca': Nat(),
        'na': Nat()
    },
    'cl_mult.xml': {
        'x': Nat(),
        'y': Nat(),
        're': Nat(),
        'c': Nat(),
        'size': Nat(),
        'n': Nat()
    },
    'ghz.xml': {
        'x': Nat(),
        'n': Nat()
    },
    'rz_mod_adder.xml': {
        'x': Qty(16),
        'na': Nat(),
        'c': Nat(),
        'a': Nat(),
        'm': Nat()
    },
    'rz_mod_div.xml': {
        'x': Qty(16),
        'i': Nat(),
        'ex': Nat(),
        'na': Nat(),
        'm': Nat()
    }
    ,
    'rz_sub.xml': {
        'x': Qty(16),
        'na': Nat(),
        'm': Nat()
    }
}
