import numpy as np
import math

result_values = []
result_nodes = []
result_matrix = []


def backtrack(explored, assignment, ass_mat, domain, matrix, shapes):
    print('-----------------------------------')
    print(explored)
    print(assignment)
    if len(explored) == V:
        result_nodes = explored
        result_values = assignment
        result_matrix = ass_mat
        return True

    domain_size = [len(domain[r]) for r in range(0, V)]
    min_domain_size = min(domain_size)
    min_domain_size_index = domain_size.index(min_domain_size)

    while len(domain_size) > 1:

        min_domain_size = min(domain_size)
        min_domain_size_index = domain_size.index(min_domain_size)

        if min_domain_size_index in explored:
            domain_size[min_domain_size_index] = 100
        else:
            break

    var = min_domain_size_index

    expl = explored[:]
    for value in domain[var]:
        assgmnt = assignment[:]
        ass_mat2 = ass_mat[:]

        if is_safe(explored, var, value, matrix, ass_mat, shapes):
            expl.append(var)
            assgmnt.append(value)
            ass_mat2[var] = value
            new_domain = forward_checking(expl, var, matrix, ass_mat2, shapes, domain)

            flag = backtrack(expl, assgmnt, ass_mat2, new_domain, matrix, shapes)
            if flag:
                return True
            else:
                expl = explored[:]
                print('backtrack failed come up')
        else:
            print('not safe')
    return False


def check_consistency(explored, var, matrix, ass_mat, shapes):
    if ass_mat[var] < 1:
        print('check consistency for node ', var, ' not valued')
        return True
    if shapes[var] == 'C':
        print('check consistency for node ', var, 'but C')
        return True

    all_neighbours_explored = True
    neighbours = []
    for i in range(0, V):
        if matrix[var][i] == 1:
            neighbours.append(i)
            if i not in explored:
                all_neighbours_explored = False

    print('check consistency for node ', var, 'with neighbours:', neighbours)
    if not all_neighbours_explored:
        print('all neighbours of ', var, 'are not explored')
        return True

    if shapes[var] == 'T':
        print('T')
        p = 1
        for neighbour in neighbours:
            p = p * ass_mat[neighbour]
        log = math.log10(p)
        log = math.floor(log)
        p = p / (10 ** log)
        p = math.floor(p)
        return ass_mat[var] == p

    if shapes[var] == 'S':
        print('S')
        p = 1
        for neighbour in neighbours:
            p = p * ass_mat[neighbour]
        p = p % 10
        return ass_mat[var] == p

    if shapes[var] == 'P':
        print('P')
        p = 0
        for neighbour in neighbours:
            p = p + ass_mat[neighbour]
        log = math.log10(p)
        log = math.floor(log)
        p = p / (10 ** log)
        p = math.floor(p)
        return ass_mat[var] == p

    if shapes[var] == 'H':
        print('H')
        p = 0
        for neighbour in neighbours:
            p = p + ass_mat[neighbour]
        p = p % 10
        return ass_mat[var] == p


def is_safe(explored, var, value, matrix, ass_mat, shapes):
    neighbours = []
    explor = explored[:]
    explor.append(var)
    ass_m = ass_mat[:]
    ass_m[var] = value

    for i in range(0, V):
        if matrix[var][i] == 1:
            neighbours.append(i)

    print('is safe for node ', var, 'with neighbours:', neighbours, 'with value: ', value)

    if not check_consistency(explor, var, matrix, ass_m, shapes):
        return False

    for neighbour in neighbours:
        if not check_consistency(explor, neighbour, matrix, ass_m, shapes):
            return False
    return True


def forward_checking(explored, var, matrix, ass_mat, shapes, domain):
    if shapes[var] == 'C':
        print('forward checking for node ', var, 'but C')
        return domain

    new_domain = domain[:]
    unexplored_neighbours = []
    explored_neighbours = []
    for i in range(0, V):
        if matrix[var][i] == 1:
            if i not in explored:
                unexplored_neighbours.append(i)
            else:
                explored_neighbours.append(i)

    if len(unexplored_neighbours) != 1:
        return new_domain
    print('forward checking for node ', var, 'with neighbours:', unexplored_neighbours)
    if shapes[var] == 'T':
        print('T')
        p = 1
        for neighbour in explored_neighbours:
            p = p * ass_mat[neighbour]
        tt = p
        for neighbour in unexplored_neighbours:
            for d in domain[neighbour]:
                tt = tt * d
                log = math.log10(tt)
                log = math.floor(log)
                tt = tt / (10 ** log)
                tt = math.floor(tt)
                if ass_mat[var] != tt:
                    new_domain[neighbour].remove(d)

    if shapes[var] == 'S':
        print('S')
        p = 1
        for neighbour in explored_neighbours:
            p = p * ass_mat[neighbour]
        tt = p
        for neighbour in unexplored_neighbours:
            for d in domain[neighbour]:
                tt = d * tt
                tt = tt % 10
                if ass_mat[var] != tt:
                    new_domain[neighbour].remove(d)

    if shapes[var] == 'P':
        print('P')
        p = 0
        for neighbour in explored_neighbours:
            p = p + ass_mat[neighbour]
        tt = p
        for neighbour in unexplored_neighbours:
            for d in domain[neighbour]:
                tt = tt + d
                log = math.log10(tt)
                log = math.floor(log)
                tt = tt / (10 ** log)
                tt = math.floor(tt)
                if ass_mat[var] != tt:
                    print('forward checking for node', var, ' domain of ', neighbour, 'removed', d)
                    new_domain[neighbour].remove(d)

    if shapes[var] == 'H':
        print('H')
        p = 0
        for neighbour in explored_neighbours:
            p = p + ass_mat[neighbour]
        tt = p
        for neighbour in unexplored_neighbours:
            for d in domain[neighbour]:
                tt = d + tt
                tt = tt % 10
                if ass_mat[var] != tt:
                    new_domain[neighbour].remove(d)

    return new_domain


V = input()
V = int(V)
E = input()
E = int(E)
shapes = input().split(" ")
# print(shapes)

C = []
for i in range(0, E):
    t = input()
    t = t.split()
    t = [int(u) for u in t]
    C.append(t)

matrix = np.zeros((V, V))
for c in C:
    matrix[c[0]][c[1]] = 1
    matrix[c[1]][c[0]] = 1
print(matrix)
constraints = []
D = [[i for i in range(1, 10)] for j in range(0, V)]


assignment_mat = [-1 for j in range(0, V)]
backtrack([], [], assignment_mat, D, matrix, shapes)
print(result_matrix)
# for node, value in result_nodes, result_values:
#     print(node, ' -> ', value)
print(len(result_values))
print(len(result_nodes))



