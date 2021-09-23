import math
def solve(input):
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