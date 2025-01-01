input of the program:

x: qubit array of size 'na' 
size: number of qubits
na: natural number, the current iteration. Each function call is iterated through [1,size), so na <= size
m : natural number, the number to be added to the array 'x' (int)

output of the program:

x: (old(x) + m) % 2^na, (no new array is created, the array 'x' is updated in place)
size: unchanged
na: unchanged
m : unchanged 


Initial version, x is run on Phi type, meaning that you can only apply SR or RQFT on x, only allow to modify the terms after "=>"

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => SKIP (x,0)
  end.


Not good version, type incorrect:

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => X (x,0)
  end.
  

OK Progressing:

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SR x 1
  | S m => SKIP (x,0)
  end.

OK Progressing, with a recursion call rz_adder' on m, we need to restrict how recursive call can be performed, like always - 1

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SR x 1
  | S m => rz_adder' x m size M 
  end.
  

OK Progressing, since quantum computation is reversible, the following will just be the same as the initial version

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; rz_adder' x m size M 
  end.

  
OK Progressing, but this operation will add 2^n - 1 to x, no matter what the M is.

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; SR x m
  end.

OK Progressing, but this operation will add 2^n - 1 +- 2^10 to x, depending on the number of 1 in M.

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; if M m then SR x 10 else SKIP (x,m)
  end.
  
Not good version, the following will never happen, since the flip of the two seq operations will flip the resulting bits, therefore, making the adder completely wrong

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => if M m then SR x (size - n) else SKIP (x,m); rz_adder' x m size M 
  end.

Good version, but ineffective

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; rz_adder' x m size M ; rz_adder' x m size M ; if M m then SR x (size - n) else SKIP (x,m)
  end.

Good version, but ineffective

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; if M m then SR x (size - n) else SKIP (x,m); if M m then SR x (size - n) else SKIP (x,m); if M m then SR x (size - n) else SKIP (x,m)
  end.

Good version, but ineffective

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; if M m then SR x (size - n) else SKIP (x,m); RQFT x; QFT x 0
  end.
  
Final version:

Fixpoint rz_adder' (x:var) (na:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_adder' x m size M ; if M m then SR x (size - n) else SKIP (x,m)
  end.
  
This is the main function, not allowed to change:

Definition rz_adder (x:var) (na:nat) (M:nat -> bool) := rz_adder' x n n M.



