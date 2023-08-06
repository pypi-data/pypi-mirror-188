# 102197018 Gaurav Gupta 3CS8

import sys
import pandas as pd
import numpy as np

# ERROR HANDLING

# File Path Handling
try:
    t=open(sys.argv[1])
except:
        raise Exception("Wrong file or file path")

file1=pd.read_csv(sys.argv[1])
file2=pd.read_csv(sys.argv[1])

# Checking number of columns in the dataset
if(len(file1.columns)<2):
    raise Exception('Atleast 3 columns must be there')

# Checking data types of the columns in the dataset
f1=file1.dtypes
print(f1)
if(list(f1).count('float64')==file1.shape[1]):
    raise Exception('There must be only numeric values')

# Checking length of weight input from the user through cmd
w=[]
for i in sys.argv[2].replace('"','').split(','):
    w.append(int(i))
if(len(file1.columns[1:])!=len(w)):
    raise Exception('Length of weight must be equal to number of numeric columns')

# Checking length of the impact input from the user through cmd
impt=[]
for i in sys.argv[3].replace('"','').split(','):
    impt.append(i)
if(len(file1.columns[1:])!=len(w)):
    raise Exception('Length of the impact must be equal to number of numeric columns')
print(impt)

# Checking whether impact values are '+' and '-' only
for i in impt:
    if(i!='+' and i!='-'):
        raise Exception('the impact should consist of + and -')
print(w)

# Chained_assignment is set None to not check the further index reference or double indexing
pd.set_option('mode.chained_assignment', None)
y=0


# Topsis Calculation
for i in file1.columns[1:]:
    np_1 = np.square(file1[i])
    sum_1 = sum(np_1)
    for j in file1.index:
        file1.loc[j, i] = file1.loc[j, i] / sum_1 ** 0.5
for i in file1.columns[1:]:
    for j in file1.index:
        file1.loc[j,i]=file1.loc[j,i]*w[y]
    y+=1
val_p=[]
val_m=[]
y=0

# Checking impact on Topsis Score
for i in file1.columns[1:]:
    if(impt[y]=='+'):
        val_p.append(file1[i].max())
        val_m.append(file1[i].min())
    else:
        val_m.append(file1[i].max())
        val_p.append(file1[i].min())
    y+=1
t_p=[]
t_m=[]
y=0


for i in file1.index:
    temp_1=0
    temp_2=0
    y=0
    for j in file1.columns[1:]:
        temp_1+=(file1[j][i]-val_p[y])**2
        temp_2+=(file1[j][i]-val_m[y])**2
        y+=1
    t_p.append(temp_1**0.5)
    t_m.append(temp_2**0.5)


# Performance Calculation
performance=[]

for i in range(len(file1.index)):
    performance.append(t_m[i]/(t_m[i]+t_p[i]))
print(performance)

# Calculating Rank 

file2[' Topsis score ']=performance
list_f=list(sorted(performance,reverse=True).index(x)+1 for x in performance)
file2[' Rank ']=list_f

# CSV generation
file2.to_csv('102197018-result.csv', index=False)