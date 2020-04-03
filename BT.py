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
    var = 0
    for i in range(0, V):
        if i not in explored:
            var = i
            break

    expl = explored[:]
    for value in domain[var]:
        assgmnt = assignment[:]
        ass_mat2 = ass_mat[:]

        if is_safe(explored, var, value, matrix, ass_mat, shapes):
            expl.append(var)
            assgmnt.append(value)
            ass_mat2[var] = value

            flag = backtrack(expl, assgmnt, ass_mat2, domain, matrix, shapes)
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



