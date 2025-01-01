Input of the program:

    x: qubit array of length na (CoqNVal),
    na: Natural number representing the length of x (int) 
    c: qubits array of length one, used as carry register. c must be initialized to zero (CoqNVal),
    a: addend to be added to x (int), 
    m : modulo divisor (int)
    
All the numbers, x, na, a and m are required to be less than 2^{na - 1}, and na is greater than or equal to 1, and m must be greater than 1.
In addition, a and x are both less than m.

x,a, and m <= 2^{na - 1}

na >= 1

m > 1

Output of the program:
    
    x: (old(x) + a) % m,
    c: unchanged,
    na: unchanged,
    a: unchanged,
    m : unchanged 
    
//x is na qubit array, c is one qubit, a and m are two numbers
//m is between 0 and 2^na, b is between 0 and m, c is initialally bit 0 (coq_nval 0) and its result will remain the same.
//result will produce x --> (x + a) % m 

//Definition rz_compare_half (x:var) (n:nat) (c:posi) (M:nat) := 
//   (rz_sub x n (nat2fb M)) ; RQFT x n; (CNOT (x,0) c).

//Definition rz_compare (x:var) (n:nat) (c:posi) (M:nat) := 
// rz_compare_half x n c M ; (inv_exp ( (rz_sub x n (nat2fb M)) ; RQFT x n)).

//Definition qft_cu (x:var) (c:posi) (n:nat) := 
//  RQFT x n;  (CNOT (x,0) c) ; QFT x n.

//Definition qft_acu (x:var) (c:posi) (n:nat) := 
//  RQFT x n;  (X (x,0); CNOT (x,0) c; X (x,0)) ; QFT x n.

//Definition one_cu_adder (x:var) (n:nat) (c:posi) (M:nat -> bool) := CU c (rz_adder x n M).

//Definition mod_adder_half (x:var) (n:nat) (c:posi) (A:nat -> bool) (M:nat -> bool) :=
//   (rz_adder x n A; (rz_sub x n M)) ; qft_cu x c n;  (one_cu_adder x n c M).

//Definition clean_hbit (x:var) (n:nat) (c:posi) (M:nat -> bool) := 
//   (rz_sub x n M) ; qft_acu x c n; ( inv_exp (rz_sub x n M)).

//Definition mod_adder (x:var) (n:nat) (c:posi) (A:nat -> bool) (M:nat -> bool) :=
//  mod_adder_half x n c A M ; clean_hbit x n c A.


