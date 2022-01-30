import numpy as np
from qiskit import QuantumCircuit, Aer, execute
import time
from IPython.display import clear_output
# from azure.quantum.qiskit import AzureQuantumProvider 
'''
provider = AzureQuantumProvider(
    subscription_id = "",
    resource_group = "",
    name = "",
    location = ""
)
'''

# GETTING THE QUBIT POSITIONS FOR EACH PLAYER

def Get_qubits(n_qubits=10,mode="single_player"):
    #n_qubits = 10
    Qubit_list = range(n_qubits)
    
    Player1_list = []
    Player2_list = []
    used_qubits = []
    
    if mode == "single_player":
        
        for i in range(int(n_qubits/2)):
                        
            while True:
                val1 = int(input("Qubit "+str(i)+" to initialize"))
                if val1 in used_qubits or val1 not in range(10):
                    print("Qubit not available")
                    continue
                else:
                    Player1_list.append(val1)
                    used_qubits.append(val1)
                    break

            while True:
                val2 = np.random.randint(n_qubits)
                if val2 in used_qubits:
                    continue
                else:
                    Player2_list.append(val2)
                    used_qubits.append(val2)
                    break
        
        print("")
        print("PLAYER QUBITS :",Player1_list)

    
    elif mode == "two_player":
        
        for i in range(int(n_qubits/2)):
            num = np.random.randint(2)
            if num==0:
                while True:
                    val1 = int(input("Player ONE qubit "+str(i)+" to initialize"))
                    if val1 in used_qubits or val1 not in range(10):
                        print("Qubit not available")
                        continue
                    else:
                        Player1_list.append(val1)
                        used_qubits.append(val1)
                        break

                while True:
                    val2 = int(input("Player TWO qubit "+str(i)+" to initialize"))
                    if val2 in used_qubits or val2 not in range(10):
                        print("Qubit not available")
                        continue

                    else:
                        Player2_list.append(val2)
                        used_qubits.append(val2)
                        break


            else:
                while True:
                    val2 = int(input("Player TWO qubit "+str(i)+" to initialize"))
                    if val2 in used_qubits or val2 not in range(10):
                        print("Qubit not available")
                        continue

                    else:
                        Player2_list.append(val2)
                        used_qubits.append(val2)
                        break

                while True:
                    val1 = int(input("Player ONE qubit "+str(i)+" to initialize"))
                    if val1 in used_qubits or val1 not in range(10):
                        print("Qubit not available")
                        continue
                    else:
                        Player1_list.append(val1)
                        used_qubits.append(val1)
                        break        
        print("")
        print("PLAYER ONE QUBITS :",Player1_list)
        print("PLAYER TWO QUBITS :",Player2_list) 
        
    return Player1_list,Player2_list


# INITIAL CIRCUIT OF EACH PLAYER

def Player_circuits(Lists,n_qubits=10,mode="single_player"):
    
    First_player_list,Second_player_list = Lists
       
    if mode == "single_player":
        
        Player_circuit = QuantumCircuit(n_qubits)

        for index in First_player_list:
            while True:
                val = int(input("Value of qubit "+str(index)))
                if val==1:
                    Player_circuit.x(index)
                    break
                elif val==0:
                    Player_circuit.id(index)
                    break
                else:
                    print("Not a possible value") 

       

        for index in Second_player_list:
            val = np.random.randint(2)
            if val==1:
                Player_circuit.x(index)
                
            elif val==0:
                Player_circuit.id(index)
                
                
    
    elif mode == "two_player":
        
        Player_circuit = QuantumCircuit(n_qubits)

        for index in First_player_list:
            while True:
                val = int(input("Value of Player ONE qubit "+str(index)))
                if val==1:
                    Player_circuit.x(index)
                    break
                elif val==0:
                    Player_circuit.id(index)
                    break
                else:
                    print("Not a possible value") 

       
        print("")
        
        for index in Second_player_list:
            while True:
                val = int(input("Value of Player TWO qubit "+str(index)))
                if val==1:
                    Player_circuit.x(index)
                    break
                elif val==0:
                    Player_circuit.id(index)
                    break
                else:
                    print("Not a possible value")

                    
    return Player_circuit


# DISPLAY THE CIRCUIT AND CLEAR THE OUTPUT
def Show_Circuit(qc,secs=10):
    print("YOU ONLY HAVE "+str(secs)+" SECONDS TO SEE THIS CIRCUIT")
    display(qc.draw("mpl",style={'name':'iqx'}))
    time.sleep(secs)
    clear_output()
    
# DETERMINE THE NUMBER OF 1 IN THE MOST FREQUENT MEASUREMENT    
def Number_of_alive_cells(counts):
    player_res = counts.most_frequent()
    alive_cells = 0
    dead_cells = 0
    for i in player_res:
        if i == '1':
            alive_cells += 1
        else:
            dead_cells += 1
            
          
    return alive_cells,dead_cells    


# TYPE 1 OPERATION
def Operation1(qc,q0,q1,q2):
    qc.ccx(q0,q2,q1)

    
# TYPE 2 OPERATION    
def Operation2(qc,q0,q1,q2):
    qc.x(q1)
    qc.cx(q0,q1)
    qc.cx(q2,q1)
       
# LOAD ROTATIONS
def load_rotations(qc):
    n_qubits = qc.num_qubits
    for i in range(n_qubits):
        num = np.random.randint(10)
        if num<3:
            qc.ry(np.pi/2.5,i)
        
# RANDOM CIRCUIT
def Create_random_circuit(qc,load_rots=False):
    n_qubits = qc.num_qubits
    
    if load_rots==True:
        load_rotations(qc)
    
    for i in range(int(n_qubits/2)):
        qubit = 1 + np.random.randint(n_qubits-2)
        num = np.random.randint(2)
        if num==0:
            Operation1(qc,qubit-1,qubit,qubit+1)
        else:
            Operation2(qc,qubit-1,qubit,qubit+1)    
        
        
# RUN THE CIRCUITS
def Run_circuit(qc): 
    #sim = provider.get_backend('ionq.simulator')
    #qpu = provider.get_backend('ionq.qpu')
    sim = Aer.get_backend('qasm_simulator')
    counts = execute(qc,backend=sim,shots=8192).result().get_counts()
    return counts         


# DETERMINE THE WINNER 
def who_wins(alive_cells,dead_cells):
    if alive_cells>dead_cells:
        print("Player 1 wins")
    elif alive_cells<dead_cells:
        print("Player 2 wins")
    else:
        print("It's a tie!")