Input of the program:

    x: Qubit array of length na (CoqNVal)
    na: Natural number representing the length of x (int)
    m: Natural to subtract from x (int)

Output of the program:

    x: (old(x) − m) % 2^na, where % is natural number modulo, e.g., 7−9 mod 2^4 =14 
    na: Unchanged
    m: Unchanged
    
//sub, subtracting natural number n to qubit array x
// main: QFT x 0; f x n size M; RQFT x
//SRR x i means SR x (-i), 
//spec: x -> (x+m) % (2^na),  the subtrahend is natural number modulo, meaning that no negative number will be produce. 1 - 10 in a four bit situation will be -9+16 = 7


Initial version, x is run on Phi type, meaning that you can only apply SR or RQFT on x, only allow to modify the terms after "=>"

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => SKIP (x,0)
  end.
  
Not good version, type incorrect:

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => X (x,0)
  end.
  

OK Progressing:

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SR x 1
  | S m => SKIP (x,0)
  end.

OK Progressing, with a recursion call rz_sub' on m, we need to restrict how recursive call can be performed, like always - 1

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SR x 1
  | S m => rz_sub' x m size M 
  end.


Not good, this will be adder rather than rz_sub

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_sub' x m size M ; if M m then SR x (size - n) else SKIP (x,m)
  end.

Not good, this will be adder rather than rz_sub

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_sub' x m size M ; if M m then SKIP (x,m) else SRR x (size - n)
  end.
  
Not good, this will be completely off, because this will sub the complement of M

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_sub' x m size M ; rz_sub' x m size M ; rz_sub' x m size M ; if M m then SRR x (size - n) else SKIP (x,m)
  end.

Good version, but ineffective

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_sub' x m size M ; if M m then SR x (size - n) ; SR x (size - n);  SRR x (size - n) else SKIP (x,m)
  end.

Good version, but ineffective

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_sub' x m size M ; if M m then SRR x (size - n) else SKIP (x,m); if M m then SRR x (size - n) else SKIP (x,m); if M m then SRR x (size - n) else SKIP (x,m)
  end.


Good version, but ineffective

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0); RQFT x;  QFT x 0
  | S m => rz_sub' x m size M ; if M m then SRR x (size - n) else SKIP (x,m)
  end.


Final version:

Fixpoint rz_sub' (x:var) (n:nat) (size:nat) (M: nat -> bool) :=
  match n with 
  | 0 => SKIP (x,0)
  | S m => rz_sub' x m size M ; if M m then SRR x (size - n) else SKIP (x,m)
  end.

This is the main function, not allowed to change:

Definition rz_sub (x:var) (n:nat) (M:nat -> bool) := rz_sub' x n n M.
