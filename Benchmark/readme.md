Quantum arithmetic circuit basic assumptions:

The arithmetic is performing natural number module arithmetic, such that there is a bit-size n defined for each circuit, and the arithmetic is performed in the range from 0 to 2^n. Every nat number that is used in arithemtic in a qubit array is required to be in the range, if not, we first modulo it and the make it by 2^n in the range.

Type information:

qubits(n): length n quantum qubit array.

nat: natural number


inv_exp: is a lib function to inverse the circuit of an input circuit program.
