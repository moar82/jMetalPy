import csv

def fitem(item):
    item=item.strip()
    try:
        item=float(item)
    except ValueError:
        pass
    return item
'''by columns:'''
print ('By columns')
with open('USR.csv', 'r') as csvin:
    reader=csv.DictReader(csvin)
    data={k.strip():[fitem(v)] for k,v in next (reader).items()}
    for line in reader:
        for k,v in line.items():
            k=k.strip()
            data[k].append(fitem(v))
    print (data)
    #print (data['memory_capacity'])
    for val in data['memory_capacity']:
        print (val)
    print("devices read from USR file:%d" % len(data['device_id']))

    '''by rows'''
print ('By rows')
with open('USR.csv') as f:
    data = [tuple(line) for line in csv.reader(f)]
    data.pop(0) #to skip the header
print(data)
print ('Number of devices %d' %len(data))

for val in data:
    print ('Memory %f , Storage %f , Val %f' %(float(val[2]),float(val[3]),float(val[6])))