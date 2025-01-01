TODO: is _i_ related to m or n?

Input of the program:

    x: Qubit array of length na (CoqNVal),
    ex: Qubit array of length na, initialized as zeroes (CoqNVal)
    na: Natural number representing the length of x and ex (int)
    m: Modulo divisor, natural number (int)
    i: Natural number related to m, such that 2^{n−2} ≤ 2^i <2^{n-1} (int)


All the numbers must be in the range of 0 to 2^{n-1}, so n bit nat number here can only store n-1 bit because the highest bit needs to be used for storing overflow indicator
i must be a value that is associated with m. i can be find by the findnum function below.

(* Example Circuits that are definable by OQASM. *)
(* find a number that is great-equal than 2^(n-1), assume that the number is less than 2^n *)
Fixpoint findnum' (size:nat) (x:nat) (y:nat) (i:nat) := 
       match size with 0 => i
              | S n => if y <=? x then i else findnum' n (2 * x) y (i+1)
       end.

Definition findnum (x:nat) (n:nat) := findnum' n x (2^(n-1)) 0.

Output of the program:

    x: old(x) % m (CoqNVal)
    ex: old(x)/m  natural number division (int)
    na: Unchanged
    m: Unchanged
    i: Unchanged

<pexp gate = 'QFT' > <id> x </id> <vexp> 0 </vexp> </pexp> 
< app > <id> f </id> <vexp op = 'plus' > <id> i </id> <vexp> 1 </vexp> <id> x </id> <id> ex </id> <id> na </id> <id> m </id> </app> 
<pexp gate = 'RQFT' > <id> x </id> </pexp>


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


