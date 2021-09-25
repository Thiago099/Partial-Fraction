import math
import re
def solve_matrix(input):
    def normalize(value, line):
        for i in range(len(line)):
            line[i] /= value

    def nullify(value, source, target):
        for i in range(len(source)):
            target[i] -= source[i] * value

    i = 0
    done_lines = []
    while(i < len(input[0])):
        min_zeros = math.inf
        min_line = 0
        for j in range(len(input)):
            for k in range(i, len(input[j])):
                if(input[j][k] != 0):
                    break
            if(k < min_zeros and j not in done_lines):
                min_zeros = k
                min_line = j
        
        done_lines.append(min_line)

        i = min_zeros
        if(min_zeros == math.inf): break
        if(input[min_line][i] == 0):
            continue
        normalize(input[min_line][i], input[min_line])
        for j in range(len(input)):
            if(j != min_line):
                nullify(input[j][i], input[min_line], input[j])
        i += 1

def solve(input):
    def split(str):
        for i in range(len(str)):
            if str[i] == '=':
                break
        return str[0:i], str[i+1::]

    a = []
    b = []

    index = []

    for i in input:
        current_a, current_b = split(i)
        current = []
        for j in re.finditer(r'(-?\d+)?(\w+)', current_a):
            key = j.group(2)
            if(not key in index):
                index.append(key)
            key = index.index(key)
            value = float(j.group(1)) if j.group(1) else 1.0
            current.append([key, value])
        a.append(current)
        b.append(float(current_b))
    matrix = []
    for i in range(len(a)):
        current_line = [0.0 for j in range(len(index))]
        for j in a[i]:
            current_line[j[0]] = j[1]
        current_line += [b[i]]
        matrix.append(current_line) 

    solve_matrix(matrix)

    def float_str(input):
        if(input.is_integer()):
            return str(int(input))
        return str(input)

    output = []
    for line in matrix:
        output_line = []
        for i in range(len(line)-1):
            if(line[i] != 0):
                if(line[i] == 1):
                    output_line.append(index[i])
                else:
                    output_line.append(float_str(line[i]) + index[i])
        output.append(' + '.join(output_line) + ' = ' + float_str(line[-1]))
    
    return output