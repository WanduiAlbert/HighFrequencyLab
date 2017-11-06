#! /usr/bin/env python3

import numpy as np
import sys

data_dir = './Spar_BFU730F'
save_dir = './LAB DATA/'
I = 1j 

def loaddata(filename):
    datatype = [("freq", np.float64),   ("S11-mag", np.float64),  ("S11-arg", np.float64),   ("S21-mag", np.float64),\
     ("S21-arg", np.float64),   ("S12-mag", np.float64),  ("S12-arg", np.float64),   ("S22-mag", np.float64),  ("S22-arg", np.float64)]
    data = np.loadtxt(filename, dtype=datatype, comments='! ', skiprows=18)

    data['freq'] /= 1e3 # Convert frequencies to GHz
    return data

def converter(freq, S11, S12, S21, S22):
    eps = S11 + S12 + S21 + S22
    D = 4-eps
    D11 = 1 - S11 - S12
    D12 = 1 - S11 - S21
    D21 = 1 - S12 - S22
    D22 = 1 - S21 - S22

    # New 3 port S parameters
    S11p = S11 + (D11 * D12)/D
    S12p = S12 + (D11 * D21)/D
    S13p = 2 * D11/D
    S21p = S21 + D22*D12/D
    S22p = S22 + D22*D21/D
    S23p = 2* D22/D
    S31p = 2*D12/D
    S32p = 2*D21/D
    S33p = eps/D

    return list(zip(freq, S11p,  S12p, S13p, S21p, S22p, S23p, S31p, S32p, S33p))

def convertdata(data):
    # Converting from 2 port to 3 port S parameters
    final_dtype = [("freq", np.float64),   ("S11", np.complex128),    ("S12", np.complex128), ("S13", np.complex128),\
       ("S21", np.complex128),   ("S22", np.complex128), ("S23", np.complex128),\
       ("S31", np.complex128), ("S32", np.complex128), ("S33", np.complex128)] # data type for the intermediate files
    
    freq = data['freq']
    S11 = data["S11-mag"] * np.exp(I * data["S11-arg"])
    S12 = data["S12-mag"] * np.exp(I * data["S12-arg"])
    S21 = data["S21-mag"] * np.exp(I * data["S21-arg"])
    S22 = data["S22-mag"] * np.exp(I * data["S22-arg"])



    final = np.array(converter(freq, S11, S12, S21, S22), dtype = final_dtype)

    # Still incomplete but let's return the result we got for now
    return final

if __name__ == "__main__":
    initial_file = sys.argv[1] # We pass in the file name as an argument
    
    data = loaddata(initial_file)

    print (data['freq'][-1])
    print ("Data correctly loaded")
    final_data = convertdata(data)

    print("Data converted correctly")

    # save_name = initial_file.split('/')[-1].split('.')[0]
    # savedata(final_data, save_dir, save_name)