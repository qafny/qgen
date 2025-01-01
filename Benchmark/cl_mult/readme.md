Input of the program:

    xa: qubit array of length na (CoqNVal),
    ya: qubit array of length na (CoqNVal),
    result: qubit array of length na, initialized to zero (CoqNVal),
    ca: carry qubit register of length one. ca is required to be initialized as zero (CoqNVal),
    na: length of xa, ya, and result (int)

Output of the program:

    xa: unchanged, 
    ya: unchanged,
    result: (xa * ya) % 2^na, 
    ca: unchanged, 
    na: unchanged

xa and ya and re have the same length of na
If the values of xa (ya) is greater than 2^na, than it will be reduced to xa % 2^na (ya % 2^na).


//(x,y,re,c) -> (x,y, re xor (x*y) %2^n,c)
//x and y and re are n-length while c is 1 qubit

//f should call g

//Definition one_cu_cl_full_adder_i (c2:posi) (x:var) (re:var) (c1:posi) (n:nat) (i:nat) := 
 // CU c2 (adder_i n x re c1 i).
//Fixpoint cl_full_mult' (n:nat) (size:nat) (x:var) (y:var) (re:var) (c:posi) :=
//   match n with 
//   | 0 => SKIP (re,0)
//   | S m => cl_full_mult' m size x y re c;
//           one_cu_cl_full_adder_i (y,m) x re c (size-m) m
//   end.

// Here x and y are in nor_mode and re in phi_mode. 
//      [x][y][phi(re)] ->[x][y][phi(x*y mod 2^n)], re is supposed to be zero, 
//    ex is in nor_mode. *)
//Definition cl_full_mult (size:nat) (x y:var) (re:var) (c:posi) :=
//   (cl_full_mult' size size x y re c).
