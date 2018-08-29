import itertools
'''we test population (Mu), CXPB, MUPB'''
counter =0
for element in itertools.product([10,20],[0.9, 0.8, 0.7, 0.6],[0.1, 0.15, 0.2, 0.25]):
    print(element)
    counter = counter+1
print ('Number of options %d' %counter)