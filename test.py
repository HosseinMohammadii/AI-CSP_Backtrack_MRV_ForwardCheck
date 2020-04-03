ls = [3 ,6 , 8, 9 , 14 , 1,  11, 4]
print(ls)
# ls.remove(5)
# print(ls)
ls.remove(11)
print(ls)
min_domain_size = min(ls)
min_domain_size_index = ls.index(min_domain_size)
print(min_domain_size_index)