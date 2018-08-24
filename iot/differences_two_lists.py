''' From https://stackoverflow.com/a/46316556/3990960
    This a method to determine the positions where to lists vary'''

A = [True,True,False,True]
B = [True,False,False,False]

differences = [
    (inner_idx)
    for inner_idx, (a_element, b_element) in enumerate(zip(A, B))
    if a_element != b_element
]

print(differences)