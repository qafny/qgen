# Quantum Genetic Programming

#program Execution

Dependencies :

Before running Qgen, ensure that the following dependencies are installed:

Python: Make sure you have Python 3.10+ installed.

Required Python Libraries:
jmetalpy - 1.6.0
antlr4-python3-runtime 4.9.2
astor -0.8.1
pytest
lxml

# Running Qgen :

python Qgen.py

# Running Qgen with options :

python Qgen.py [OPTIONS]

Available options:

--project_path=Benchmark/rz_adder
--algorithm=ga
--epoch=5  (default :1)
--iter=100 (total iterations ,default :50)
--pop=10   (population , default :10)
--mutation=0.1 (mutation ,default :1)
--crossover=0.9 (crossover ,default :1)
--sel=tournament (selection ,default :tournament)
--tags='["gate"]' (XMl tags,default :[])
--operators='["QGateInsertion"]' (Operators ,default :[])
--targetfitness=0.01 (Target Fitness ,default :0)

# Example command :
python Qgen.py --project_path=Benchmark/rz_adder --algorithm=ga --epoch=3 --iter=100 --pop=20 --mutation=0.2 --crossover=0.8 --sel=tournament --tags='["gate"]' --operators='["QGateInsertion"]' --targetfitness=0.01
