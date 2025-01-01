Input of the program:

    xa: qubit array of length na to be added to ya (CoqNVal),
    ya: qubit array of length na (CoqNVal), 
    ca: qubit array of length 1, initialized as 0 (CoqNVal),
    na: Natural number representing the length of xa and ya (int)

Output of the program:

    xa: unchanged, 
    ya: (xa + ya) % 2^na (modified in place),
    ca: unchanged, 
    na: unchanged

xa and ya have the same length of na

x y c are arrays in Nor type, so allowed gates are CU, X, and QFT

For this generation, we can setup the system to only generate gates with respect to MAJ, and UMA, no others

These are assumed circuits:

Definition MAJ a b c := CNOT c b ; CNOT c a ; CCX a b c.
Definition UMA a b c := CCX a b c ; CNOT c a ; CNOT a b.

Assumed initialization:

Fixpoint MAJseq' n x y c : exp :=
  match n with
  | 0 => SKIP (x,0)
  | S m => SKIP (x,0)
  end.
  
Assumed generation:

Fixpoint UMAseq' n x y c : exp :=
  match n with
  | 0 => SKIP (x,0)
  | S m => SKIP (x,0)
  end.
  

Need generation:

Fixpoint MAJseq' n x y c : exp :=
  match n with
  | 0 => MAJ c (y,0) (x,0)
  | S m => MAJseq' m x y c; MAJ (x, m) (y, n) (x, n)
  end.
  
Main function:

Definition MAJseq n x y c := MAJseq' (n - 1) x y c.


Need generation:

Fixpoint UMAseq' n x y c : exp :=
  match n with
  | 0 => UMA c (y,0) (x,0)
  | S m => UMA (x, m) (y,n) (x, n); UMAseq' m x y c
  end.

Main function:

Definition UMAseq n x y c := UMAseq' (n - 1) x y c.


Main function, not change:
Definition adder01 n x y c: exp := MAJseq n x y c; UMAseq n x y c.
