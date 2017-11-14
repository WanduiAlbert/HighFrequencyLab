#! /usr/bin/env python3

import numpy as np
import sys
from math import pi

data_dir = './Spar_BFU730F'
save_dir = './LAB DATA/'
I = 1j 

def loaddata(filename):
    datatype = [("freq", np.float64),   ("S11-mag", np.float64),  ("S11-arg", np.float64),   ("S21-mag", np.float64),\
     ("S21-arg", np.float64),   ("S12-mag", np.float64),  ("S12-arg", np.float64),   ("S22-mag", np.float64),  ("S22-arg", np.float64)]
    data = np.loadtxt(filename, dtype=datatype, comments='! ', skiprows=18)

    data['freq'] /= 1e3 # Convert frequencies to GHz
    return data

def parameter_converter(freq, S11, S12, S21, S22):
    """
    Converts from 2 port to 3 port parameters for a transistor. Returns the data as a list that can be used to construct a structured array
    """
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
    
    # Recall the angles are in degrees. Need to convert back to radians.
    freq = data['freq']
    S11 = data["S11-mag"] * np.exp(I * data["S11-arg"] * pi/180)
    S12 = data["S12-mag"] * np.exp(I * data["S12-arg"] * pi/180)
    S21 = data["S21-mag"] * np.exp(I * data["S21-arg"] * pi/180)
    S22 = data["S22-mag"] * np.exp(I * data["S22-arg"] * pi/180)



    final = np.array(parameter_converter(freq, S11, S12, S21, S22), dtype = final_dtype)

    # Still incomplete but let's return the result we got for now
    return final

def splitter(c_array):
    # Splits an array of complex values into the magnitude and phase parts
    return [np.abs(c_array), np.angle(c_array) * 180/pi]

def reformatter(data):
    final = [data['freq']]
    categories = ['S11', 'S12','S13','S21','S22','S23','S31','S32','S33']
    for cat in categories:
        final += splitter(data[cat])
    return np.vstack(final).T


def savedata(final_data, save_dir, save_name, initial_file):
    save_data = reformatter(final_data)
    N = save_data.shape[0]
    with open(save_dir + save_name, 'w') as save_f:

        with open(initial_file) as read_f:
            line = read_f.readline()
            while (line.startswith('!')):
                save_f.write(line)
                line = read_f.readline()

        save_f.write("!3-port S-parameters\n")
        save_f.write('# GHz S MA R 50\n')
        save_f.write('!  Freq-GHz   S11-mag  S11-arg   S12-mag  S12-arg   S13-mag  S13-arg   S21-mag  S21-arg   S22-mag  S22-arg   S23-mag  S23-arg   S31-mag  S31-arg   S32-mag  S32-arg   S33-mag  S33-arg\n')

        for i in range(N):
            save_f.write("{0: 6.3f}  {1: 6.3f}  {2: 6.3f}  {3: 6.3f}  {4: 6.3f}  {5: 6.3f}  {6: 6.3f}\n".format(save_data[i, 0], save_data[i, 1],\
             save_data[i, 2], save_data[i, 3], save_data[i, 4], save_data[i, 5], save_data[i, 6]))

            save_f.write("      {0: 6.3f}  {1: 6.3f}  {2: 6.3f}  {3: 6.3f}  {4: 6.3f}  {5: 6.3f}\n".format(save_data[i, 7], save_data[i, 8],\
             save_data[i, 9], save_data[i, 10], save_data[i, 11], save_data[i, 12]))

            save_f.write("      {0: 6.3f}  {1: 6.3f}  {2: 6.3f}  {3: 6.3f}  {4: 6.3f}  {5: 6.3f}\n".format(save_data[i, 13], save_data[i, 14],\
             save_data[i, 15], save_data[i, 16], save_data[i, 17], save_data[i, 18]))
        

     

if __name__ == "__main__":
    initial_file = sys.argv[1] # We pass in the file name as an argument
    
    data = loaddata(initial_file)

    print ("Data correctly loaded")
    final_data = convertdata(data)

    print("Data converted correctly")

    save_name = initial_file.split('/')[-1].split('.')[0] + '.s3p'

    

    savedata(final_data, save_dir, save_name, initial_file)