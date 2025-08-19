MAX = 1000

def challenger(seed = 2006):

    r = [0]*MAX

    tmp    = []
    # import random
    r[0] = seed

    tmp.append(r[0])
    for i in range(1,31):
        r[i] = (16807 * r[i-1]) % 2147483647
        if r[i] < 0:
            r[i] += 2147483647
        tmp.append(r[i])

    for i in range(31,34):
        r[i] = r[i-31]
        tmp.append(r[i])
    
    for i in range(34,344):
        r[i] = r[i-31] + r[i-3] 
        r[i] = r[i] % 2**32
        tmp.append(r[i])
    output = []
    for i in range(344,MAX):
        r[i] = r[i-31] + r[i-3]
        r[i] = r[i] % 2**32
        output.append(r[i]>>1)
        tmp.append(r[i])
    """
    i-3   i-31     i 
    00    00        00 == 00    01        01
    00    01        01 == 00    00        00 <-------
    00    10        10 == 00    11        11 
    00    11        11 == 00    10        10 <-------
    01    00        01 == 00    00        00 <-------
    01    01        10
    01    10        11 == 00    10        10 <-------
    01    11        00  
    10    00        10 == 10    01        11
    10    01        11 == 10    00        10 <-------
    10    10        00 == 10    11        01
    10    11        01 == 10    10        00 <-------
    11    00        11 == 10    00        10 <-------
    11    01        00
    11    10        01 == 10    10        00 <-------
    11    11        00
    
    """
    return output,tmp



output,tmp = challenger()
output = [0]*344 + output
index  = MAX -1 
check  = 1

fre = [0]* MAX
############### PHASE 1 ########################

"""
    i-3   i-31      i
    01    01        10
    01    11        00  
    11    01        00
"""
while index -31 >= 344 : 

    if fre[index] == 0:

        x = output[ index - 3  ]
        y = output[ index - 31 ]
        z = output[ index      ]
        xbit = bin(x)[-1]
        ybit = bin(y)[-1]
        zbit = bin(z)[-1]
        if ( xbit == '0' and ybit == '0' and zbit =='1' and 
            fre[index]==0 and fre[index-3]==0 and fre[index - 31]==0 ):
                    if fre[index]==0:
                        output[index]   = (output[index] * 2) % 2**32
                        fre[index]=1
                        
                    
                    if fre[index-3]  ==0 :
                        output[index-3] = (output[index - 3]* 2 + 1) %2**32
                        fre[index-3] = 1

                    if fre[index-31] ==0 :
                        output[index-31]= (output[index - 31]* 2 + 1) % 2**32
                        fre[index-31]= 1

                    fre[index] = 1
                    # print(output[index],tmp[index])
                    
                    assert output[index   ] == tmp[index]
                    assert output[index-3 ] == tmp[index-3]
                    assert output[index-31] == tmp[index-31]

        if ( xbit == '0' and ybit == '1' and zbit =='0' 
            and fre[index]==0 and fre[index-3]==0 and fre[index - 31]==0 ):
                    if fre[index]==0:
                        output[index]   = (output[index] * 2) % 2**32
                        fre[index]=1
                        
                    
                    if fre[index-3]  ==0 :
                        output[index-3] = (output[index - 3]* 2 + 1) %2**32
                        fre[index-3] = 1

                    if fre[index-31] ==0 :
                        output[index-31]= (output[index - 31]* 2 + 1) % 2**32
                        fre[index-31]= 1
                        
                    fre[index] = 1
                    
                    assert output[index   ] == tmp[index]
                    assert output[index-3 ] == tmp[index-3]
                    assert output[index-31] == tmp[index-31]
        
        if ( xbit == '1' and ybit == '0' and zbit =='0' 
            and fre[index]==0 and fre[index-3]==0 and fre[index - 31]==0 ):
                    if fre[index] == 0:
                        output[index]   = (output[index] * 2) % 2**32
                        fre[index]=1

                    if fre[index-3]  ==0 :
                        output[index-3] = (output[index - 3]* 2 + 1) %2**32
                        fre[index-3] = 1

                    if fre[index-31] ==0 :
                        output[index-31]= (output[index - 31]* 2 + 1) % 2**32
                        fre[index-31]= 1
                        
                    fre[index] = 1

                    assert output[index   ] == tmp[index]
                    assert output[index-3 ] == tmp[index-3]
                    assert output[index-31] == tmp[index-31]


                    
    index -= 1     
        
check = 1 
while check: 
    check = 0
    for i in range(344,MAX):
        if fre[ i - 31 ] and fre[ i - 3 ]==0 and fre[i]  :
            fre[i - 3]= 1 
            check = 1 
            output[i-3] = (output[i]-output[i - 31]) % 2**32
            assert output[i-3]==tmp[i-3]
        
        if fre[ i - 31 ]==0 and fre[ i - 3 ] and fre[i]  :
            fre[i - 31]= 1 
            check = 1 
            output[i-31] = (output[i]-output[i - 3]) % 2**32
            assert output[i - 31]==tmp[i-31]
        
        if fre[ i - 31 ] and fre[ i - 3 ] and fre[i] == 0 :
            fre[i] = 1 
            check = 1
            output[i] = (output[i - 3] + output[i - 31])  % 2**32
            assert output[i] == tmp[i]


############### PHASE 2 ######################### 

from z3 import * 



x = [BitVec(f'x_{i}',32) for i in range(31)]
u = x 
for i in range(31,34):
    x.append(x[i-31])

for i in range(34,344):
        x.append(x[i-31] + x[i-3]) 

s = Solver()
for i in range(344,344+80):
        x.append( x[i-31] + x[i-3])
        s.add(x[i] == int(output[i]) )
assert s.check() == sat
m = s.model()

print(m[u[0]].as_long())