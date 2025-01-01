SKIP_XML = """
<let> <id> f </id> <id type = 'qubits' > x </id> <id type = 'qubits' > y </id> <id type = 'qubits' > c </id> <id type = 'nat' > n </id>
   <match> <id> n </id>
          <pair> <vexp> 0 </vexp> <pexp gate = 'SKIP' > <id> x </id> <vexp> 0 </vexp> </pexp> </pair>
          <pair> <vexp op = '+'> <id> m </id> <vexp>  1 </vexp> </vexp> <pexp gate = 'SKIP' > <id> x </id> <vexp> 0 </vexp> </pexp> </pair>
   </match>
</let>
<app> <id> f </id> <id> xa </id> <id> ya </id> <id> ca </id> <id> na </id> </app>
        """

# applying X gate, and then a CCX gate controlling at (x,0) and (x,1) and flip of (y,1)
X_CCV = '''
    <pexp gate="X" type="Nor">
    <id>x</id>
    <vexp>0</vexp>
</pexp>
<pexp gate="CU" type="Nor">
    <id>x</id>
    <vexp>0</vexp>
    <pexp gate="CU" type="Nor">
        <id>x</id>
        <vexp>1</vexp>
        <pexp gate="X" type="Nor">
            <id>y</id>
            <vexp>1</vexp>
        </pexp>
    </pexp>
</pexp>
<app> <id> f </id> <id> xa </id> <id> ya </id> <id> ca </id> <id> na </id> </app>
'''

FLIP_X_ZERO_ROTATE_PHASE = """
<pexp gate = 'X' type = 'Nor' > <id> x </id>  <vexp> 0 </vexp> </pexp> <pexp gate = 'CU' type = 'Nor' > <id> x </id> < vexp> 0 </vexp>  <pexp gate = 'RZ' type = 'Nor' > <vexp> 10 </vexp> <id> y </id>  <vexp> 1 </vexp> </pexp>  </pexp>
<app> <id> f </id> <id> xa </id> <id> ya </id> <id> ca </id> <id> na </id> </app>
"""

CNOT = """
<pexp gate = 'CU' > <id> x </id>  <vexp> 1 </vexp> <pexp gate = 'X' > <id> y </id>  <vexp> 1 </vexp> </pexp>
<app> <id> f </id> <id> xa </id> <id> ya </id> <id> ca </id> <id> na </id> </app>
"""

CCX = """
<pexp gate = 'CU' > <id> x </id>  <vexp> 1 </vexp> <pexp gate = 'CU' > <id> y </id>  <vexp> 1 </vexp> <pexp gate = 'X' > <id> z </id>  <vexp> 1 </vexp> </pexp> </pexp>
<app> <id> f </id> <id> xa </id> <id> ya </id> <id> ca </id> <id> na </id> </app>
"""
